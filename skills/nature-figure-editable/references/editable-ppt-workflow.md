# Native PPT construction

Read this after choosing the scientific backend and before producing the paired PPT.

## 1. Author for paired export

Use the original scientific workflow and the user's chosen libraries. Export editable SVG text (`matplotlib.rcParams['svg.fonttype']='none'` or `svglite`), not text converted to outlines. Avoid raster heatmaps, rasterized collections and image-based color bars in all-vector figures. A heatmap can be a grid of native rectangular cells and a stepped/vector color scale; do not invent values to reduce object count.

Use consistent font metrics while composing and exporting. In R, grid/ggplotify measurements and final devices should use compatible installed fonts; a default PostScript measurement device may silently substitute fonts even when the final Cairo/SVG export uses Arial. Keep reference lines, intervals and risk tables as vectors.

Inspect the emitted SVG, not just the code: `use` references, CSS defaults, font fallback, math glyph paths, clipping and transforms may be introduced by the plotting library. Fonttype settings alone do not prove every math label is editable.

## 2. Choose an available native-object authoring route

Use the installed presentation-authoring skill if available, following its required package and finalization workflow. With that workflow, translate the canonical SVG/scene into native text boxes, shapes, lines and freeform paths. Do not embed the SVG as a picture. Do not copy absolute runtime paths or figure-specific data from a previous task; discover runtime paths for the current environment.

An R vector device such as `rvg` with a presentation writer is another route when permitted by the available authoring workflow. It is not automatically compliant: inspect for groups, raster content and outlined labels, then flatten all figure groups while preserving affine transforms and z-order. Read package documentation or local installed source for the version in use rather than guessing API signatures.

If the user explicitly wants to see PowerPoint interaction, a supported live UI workflow can convert to shapes and recursively ungroup. Save a new PPTX and audit it afterward. Automation still must not rely on the user manually ungrouping the delivered file.

## 3. Geometry and text fidelity

- Normalize SVG physical units and viewBox coordinates before PPT placement: 1 inch = 72 pt = 96 CSS px = 914400 EMU. Use the actual SVG viewport for the slide size.
- Resolve inherited styles and nested transforms. Expand SVG `use` references, preserve draw order, and handle affine transforms correctly. For existing PPT group flattening, compose parent offsets/extents, child coordinate systems, rotation and flips; simply deleting group wrappers changes the layout.
- Honor clipping. Intersect vector lines/polygons with panel boundaries or use a supported native vector representation. Never rasterize a difficult clip/mask/filter silently. Unsupported effects require an equivalent vector construction checked against the source, or a disclosed limitation.
- Preserve opacity, fill rule, joins, caps, dash lengths and offsets. If a renderer loses custom dash patterns, encode each curve's visible dash intervals as subpaths of one native freeform. Do not turn it into a solid curve or thousands of individually scattered objects.
- Convert text anchors/baselines and rotated labels, not merely top-left coordinates. Allow enough text-box height for the font's ascent/descent and PowerPoint line height while maintaining the intended baseline. Inspect small statistical annotations and math fragments for clipping and overlap.
- Keep main curves and legend samples stylistically matched. Preserve the same data, panel order, tick values, risk-table alignment, confidence intervals and color scale in both formats.

For dense plots, object count may be high. Prefer a path per curve and editable markers/cells; do not silently downsample points or simplify curves enough to change scientific evidence. Ask if a meaningful editability/fidelity tradeoff is unavoidable.

## 4. Deliver only after QA

Follow `editable-ppt-qa.md` plus the presentation author's finalizer. A deck that opens structurally can still have invisible text or substituted fonts. Render and inspect the final file, not only the source SVG or a pre-conversion preview.

Keep converter code reproducible/configurable when providing it. Do not claim the standalone R/Python plotting script regenerates the PPT if PPT packaging is a separate step; identify that step and its dependencies honestly.
