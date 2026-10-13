# Paired editable-delivery contract

## What “editable” means here

The user can open the PPTX and select a text label, axis, tick, curve, point, bar, uncertainty band, error bar, heatmap cell, legend item or panel label without using Convert to Shape, Ungroup, a macro or a plug-in first. Use native text boxes, lines and geometric/freeform shapes as top-level slide objects. Flatten every nested figure group, not just the outer group.

A continuous curve can remain one editable freeform/path object; do not split each vertex into its own object. A dashed curve may use disconnected subpaths within that object. Each plotted marker or heatmap cell should be separately selectable. A legend, forest table, panel or multi-series chart must not remain a single picture/group/Office-chart object. These are editable drawing objects, not automatically data-linked Excel charts; say so when relevant.

Text remains text, including labels, numeric cells, P values, subscripts and superscripts. Do not outline ordinary text to hide a font problem. Use suitable installed fonts and native runs/text boxes for mathematical formatting, with visual verification. Report any unsupported notation instead of claiming it remains editable.

## Canvas and source of truth

Generate the science once. Use its canonical SVG geometry or a shared scene description for the paired PPT, preserving sizes, coordinates, curves, markers, clipping, z-order, colors, opacity, dashes, fonts and labels. Never independently refit, interpolate or invent data in the converter. Match the SVG's actual physical canvas, including any tight-bbox change; do not force 16:9 or add a title slide.

The scientific backend stays Python or R. Neutral SVG/OOXML inspection, native-PPT packaging (for example JavaScript or an R vector device), and rendering that PPT for compatibility QA are permitted regardless of the selected backend. This packaging exception qualifies the inherited “all exports/QA in one backend” language. It does not permit a substitute scientific plot, statistical recalculation or approximation in the other language.

## Completion and boundaries

By default deliver both the SVG and the final ungrouped PPTX, plus reproducible source and requested companion outputs. Do not promise completion until both pass structural and visual checks. If PPT creation is blocked, preserve the successful scientific exports, state the exact limitation and ask only for the missing authority or decision. Do not pass off a picture-in-PPT fallback as the requested result.

For genuinely pixel-based science (SEM, microscopy, blots, gels or photographs), pixels cannot become meaningful editable scientific elements. Preserve image integrity; do not trace or invent underlying measurements. Explain that the image can be selected as one image while overlaid annotations can be native objects, and obtain the user's agreement before a mixed raster/vector exception. Record that exception in the QA note; never label it “all-vector/all-elements editable”. For pure data plots, zero placed pictures and zero groups are required.

Preserve existing user files. Conversion should target a new output or an explicitly authorized replacement. Do not change the original `nature-figure` skill or global application settings while using this fork.
