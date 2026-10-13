"""Regression fixtures exercise structure and dimensions, not instruction wording."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from audit_editability import inspect_pair, inches, NS


class AuditTests(unittest.TestCase):
    def fixture(self, extra="", svg_extra="", width="648pt", master=""):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        svg = root / "figure.svg"
        svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="576pt"><text x="1" y="12">Test</text>{svg_extra}</svg>')
        ppt = root / "figure.pptx"
        with ZipFile(ppt, "w") as z:
            z.writestr("ppt/presentation.xml", f'<p:presentation xmlns:p="{NS["p"]}" xmlns:r="{NS["r"]}"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="8229600" cy="7315200"/></p:presentation>')
            z.writestr("ppt/_rels/presentation.xml.rels", '<Relationships><Relationship Id="rId1" Target="slides/slide1.xml"/></Relationships>')
            z.writestr("ppt/slides/slide1.xml", f'<p:sld xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}"><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>Test</a:t></a:r></a:p></p:txBody></p:sp>{extra}</p:spTree></p:cSld></p:sld>')
            if master:
                z.writestr("ppt/slideMasters/slideMaster1.xml", f'<p:sldMaster xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}">{master}</p:sldMaster>')
        return svg, ppt

    def test_valid_native_pair(self):
        result = inspect_pair(*self.fixture())
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["pptx"]["top_level_native_objects"], 1)
        self.assertEqual(result["pptx"]["top_level_text_shapes"], 1)

    def test_nested_group_rejected(self):
        result = inspect_pair(*self.fixture(extra="<p:grpSp><p:grpSp/></p:grpSp>"))
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["pptx"]["groups"], 2)

    def test_svg_raster_rejected(self):
        result = inspect_pair(*self.fixture(svg_extra='<image href="data:image/png;base64,AAAA"/>'))
        self.assertEqual(result["status"], "fail")

    def test_ppt_picture_rejected(self):
        result = inspect_pair(*self.fixture(extra="<p:pic><a:blip/></p:pic>"))
        self.assertEqual(result["pptx"]["pictures"], 1)
        self.assertEqual(result["status"], "fail")

    def test_chart_container_rejected(self):
        self.assertEqual(inspect_pair(*self.fixture(extra="<p:graphicFrame/>"))["status"], "fail")

    def test_master_picture_rejected(self):
        self.assertEqual(inspect_pair(*self.fixture(master="<p:pic/>"))["status"], "fail")

    def test_fixed_master_shape_rejected(self):
        self.assertEqual(inspect_pair(*self.fixture(master="<p:sp/>"))["status"], "fail")

    def test_size_mismatch_rejected(self):
        self.assertEqual(inspect_pair(*self.fixture(width="10in"))["status"], "fail")

    def test_units_and_invalid_index(self):
        for value in ("9in", "648pt", "864px", "228.6mm", "22.86cm"):
            self.assertAlmostEqual(inches(value), 9)
        with self.assertRaises(ValueError):
            inches("100%")
        with self.assertRaises(ValueError):
            inspect_pair(*self.fixture(), slide_index=2)


if __name__ == "__main__":
    unittest.main()
