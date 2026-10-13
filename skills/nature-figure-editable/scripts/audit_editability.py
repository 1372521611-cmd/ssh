#!/usr/bin/env python3
"""Structural SVG/PPTX audit. No graphics libraries, rendering or data alteration."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
FACTORS = {"": 1 / 96, "px": 1 / 96, "pt": 1 / 72, "pc": 1 / 6,
           "in": 1, "cm": 1 / 2.54, "mm": 1 / 25.4, "q": 1 / 101.6}


def inches(value):
    match = re.fullmatch(r"\s*([+\-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?)\s*([a-zA-Z]*)\s*", value or "")
    if not match or match[2].lower() not in FACTORS:
        raise ValueError(f"SVG needs an explicit absolute width/height, got {value!r}")
    number = float(match[1]) * FACTORS[match[2].lower()]
    if not math.isfinite(number) or number <= 0:
        raise ValueError("SVG dimensions must be finite and positive")
    return number


def count(root, name):
    return len(root.findall(".//" + name, NS))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inspect_pair(svg_path, pptx_path, slide_index=1):
    problems = []
    svg = ET.parse(svg_path).getroot()
    if svg.tag.rsplit("}", 1)[-1] != "svg":
        raise ValueError("Input is not an SVG root")
    dimensions = [inches(svg.get("width")), inches(svg.get("height"))]
    svg_tags = [node.tag.rsplit("}", 1)[-1] for node in svg.iter()]
    svg_text = sum(1 for node in svg.iter()
                   if node.tag.rsplit("}", 1)[-1] == "text" and "".join(node.itertext()).strip())
    if not svg_text:
        problems.append("SVG has no nonempty editable text nodes; check for outlined labels")
    for tag in ("image", "foreignObject"):
        if tag in svg_tags:
            problems.append(f"SVG contains {svg_tags.count(tag)} {tag} nodes")
    for node in svg.iter():
        for key, value in node.attrib.items():
            if key.rsplit("}", 1)[-1] == "href" and not value.startswith("#"):
                # Hyperlinks do not place graphics, but external use/image resources do.
                if node.tag.rsplit("}", 1)[-1] != "a":
                    problems.append("SVG depends on a non-local graphic resource")

    with ZipFile(pptx_path) as archive:
        names = archive.namelist()
        pres = ET.fromstring(archive.read("ppt/presentation.xml"))
        size = pres.find("p:sldSz", NS)
        if size is None:
            raise ValueError("PPTX has no slide size")
        ppt_dims = [int(size.get(k)) / 914400 for k in ("cx", "cy")]
        if any(abs(a - b) > 0.0001 for a, b in zip(dimensions, ppt_dims)):
            problems.append("PPT slide size does not match the emitted SVG canvas")
        rels = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
        target_map = {item.get("Id"): item.get("Target") for item in rels}
        ids = pres.findall("p:sldIdLst/p:sldId", NS)
        if not 1 <= slide_index <= len(ids):
            raise ValueError(f"slide-index must be in 1..{len(ids)}")
        target = target_map[ids[slide_index - 1].get("{" + NS["r"] + "}id")]
        slide_name = posixpath.normpath(target.lstrip("/") if target.startswith("/") else posixpath.join("ppt", target))
        slide = ET.fromstring(archive.read(slide_name))
        tree = slide.find("p:cSld/p:spTree", NS)
        if tree is None:
            raise ValueError("Selected slide has no shape tree")
        native_shapes = len(tree.findall("p:sp", NS))
        connectors = len(tree.findall("p:cxnSp", NS))
        text_shapes = sum(1 for shape in tree.findall("p:sp", NS)
                          if any((node.text or "").strip() for node in shape.findall(".//a:t", NS)))
        if not native_shapes + connectors:
            problems.append("Selected slide has no top-level native figure objects")
        if not text_shapes:
            problems.append("Selected slide has no top-level native editable text")
        totals = {"groups": 0, "pictures": 0, "image_fills": 0,
                  "graphic_frames": 0, "ole_objects": 0}
        non_slide_visible = 0
        for name in names:
            if not re.fullmatch(r"ppt/(?:slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster)\d+\.xml", name):
                continue
            root = ET.fromstring(archive.read(name))
            for key, tag in (("groups", "p:grpSp"), ("pictures", "p:pic"),
                             ("image_fills", "a:blip"), ("graphic_frames", "p:graphicFrame"),
                             ("ole_objects", "p:oleObj")):
                totals[key] += count(root, tag)
            if "/slides/" not in name:
                for shape in root.findall(".//p:sp", NS):
                    # Empty layout placeholders are not fixed figure elements.
                    placeholder = shape.find(".//p:ph", NS) is not None
                    if not placeholder:
                        non_slide_visible += 1
                non_slide_visible += count(root, "p:cxnSp")
        for key, value in totals.items():
            if value:
                problems.append(f"PPTX contains {value} {key} across slides/layouts/masters")
        if non_slide_visible:
            problems.append(f"PPTX has {non_slide_visible} non-placeholder shapes fixed in layouts/masters")

    return {
        "status": "pass" if not problems else "fail",
        "scope": "Structural checks only; visual fidelity, all-label editability, fonts, object granularity, science and live PowerPoint behavior require separate verification.",
        "svg": {"sha256": digest(svg_path), "dimensions_inches": dimensions,
                "editable_text_nodes": svg_text, "image_nodes": svg_tags.count("image")},
        "pptx": {"sha256": digest(pptx_path), "slide_count": len(ids),
                 "audited_slide_index": slide_index, "dimensions_inches": ppt_dims,
                 "top_level_native_objects": native_shapes + connectors,
                 "top_level_text_shapes": text_shapes, **totals,
                 "fixed_layout_master_shapes": non_slide_visible},
        "problems": problems,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg", required=True, type=Path)
    parser.add_argument("--pptx", required=True, type=Path)
    parser.add_argument("--slide-index", type=int, default=1)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = inspect_pair(args.svg, args.pptx, args.slide_index)
    except (OSError, ET.ParseError, BadZipFile, KeyError, TypeError, ValueError) as exc:
        result = {"status": "fail", "problems": [str(exc)]}
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
