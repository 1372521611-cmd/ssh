# Editable-pair QA

Run the original scientific QA and the available presentation-authoring finalization checks. Then audit the final paired files with the bundled non-rendering helper:

```bash
python scripts/audit_editability.py --svg /path/to/figure.svg \
  --pptx /path/to/figure_editable.pptx --report /path/to/editability_qa.json
```

The helper uses only the Python standard library and does not render or replot anything; it is allowed with either scientific backend. For a multi-slide deck, run once per SVG with `--slide-index N` and check that the slide count matches the figure contract. The strict audit deliberately rejects mixed raster content and non-ungrouped chart/table containers. If the user agreed to an image-panel exception, document it separately; do not suppress a failure and claim strict compliance.

## Required observations

- SVG has explicit physical dimensions, genuine editable text and no image/foreignObject content. Manually inspect math labels: a positive text-node count does not prove that no other labels were outlined.
- PPT has zero `p:grpSp` groups and zero pictures/image fills in the slide/layout/master content; the root shape tree is not a group. No embedded SVG/EMF/PNG figure, OLE object or opaque chart/table container substitutes for per-element objects.
- Text exists as native DrawingML text, not glyph paths. All figure objects live directly on the slide rather than being fixed on the master/layout. Record shape/text counts and size comparisons.
- The PPT canvas equals the SVG's actual canvas. Original plotting inch dimensions may differ after a tight bounding-box crop; audit the emitted files.
- Render every final slide and inspect it against the canonical SVG at comparable size. Check all panels, limits/ticks, values, symbol formatting, curves, uncertainty bands, dashed/dotted lines, color bars, opacity, rotations and z-order. Look especially for missing text in short-height boxes.
- Use a real PowerPoint interaction check when available and useful: click representative text, curve, point and heatmap cell separately. Do not claim this test occurred when only an offline renderer was used.

The helper does not certify visual equality, text completeness, font availability, object granularity, scientific correctness, absence of outlined glyphs, or behavior in PowerPoint. Its JSON is structural evidence, not a substitute for those checks. Any failure is actionable: fix the native output, or state the unresolved limitation instead of calling the pair complete.
