---
name: nature-figure-editable
description: >-
  Nature Figure 可编辑版。Create or revise publication-quality scientific figures in Python or R, delivering both an editable-text vector SVG and a visually matched PPTX with all figure elements already ungrouped as native, individually selectable objects. Use for Nature-style/manuscript figures with editable PowerPoint delivery, 科研图可编辑PPT、SVG拆解、取消组合、打开直接编辑, or explicit invocation of this skill. Retains nature-figure's scientific contract, design references, source-data traceability and statistical QA. Not a general slide-deck or raster-to-data reconstruction tool.
metadata:
  version: "1.0.1-rc1"
  based-on: "nature-figure 2.0.0"
---

# Nature Figure 可编辑版

<!-- Modified for nature-figure-editable: paired SVG/PPTX workflow and release licensing safeguards. -->

This is a self-contained fork of `nature-figure`, not a replacement for or an edit to the original skill. Its distinguishing default is **paired SVG + fully ungrouped native PPTX delivery**. Do not ask the user to repeat this preference. An explicit request to omit a format overrides this default.

Before copying or adapting bundled third-party examples or their derivative reference material, read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Do not infer that permission from one upstream author covers other rightsholders. When a specific reuse lacks adequate authorization, omit that reuse and continue with user-owned data and an independent implementation where possible. This is not a blanket gate on ordinary plotting.

## Load and route

1. Read [manifest.yaml](manifest.yaml) and every `always_load` file. The editable-delivery contract governs PPT packaging where inherited references describe only static exports.
2. Resolve Python or R from the user's explicit choice or a clearly language-specific workflow. If neither is known, ask **Python or R?** and stop. If the user asks you to choose, consult `references/backend-selection.md` and state your choice. This plotting gate does not block maintenance of the skill itself.
3. Read only the chosen backend fragment. Create the scientific figure contract before plotting: claim, evidence chain, panel map, data provenance, statistics, dimensions and formats. Honor requested grids, fonts and dimensions rather than imposing a preferred archetype.
4. Use the selected backend for the statistical analysis, scientific drawing and canonical SVG. Load the original on-demand references as needed. Preserve the original skill's statistical, source-data, simulation and image-integrity safeguards.
5. Read [references/editable-ppt-workflow.md](references/editable-ppt-workflow.md) before PPT construction. Use the available presentation-authoring skill and its required authoring/finalization tools; read its instructions before using them. PPT packaging and its renderer are a narrow exception to backend exclusivity, not permission to replot the science in another language.
6. Read [references/qa-contract.md](references/qa-contract.md) and [references/editable-ppt-qa.md](references/editable-ppt-qa.md) before delivery. Run the structural auditor, render every final slide, inspect against the canonical SVG and fix failures.

## Default result

- `figure.svg`: genuine vector geometry, editable text; no rasterized plot layers.
- `figure_editable.pptx`: same figure canvas and visual design, one figure per slide, all elements ungrouped and directly selectable. No embedded whole-figure SVG, EMF, PNG or PDF masquerading as editable shapes.
- The selected-backend source code, relevant source data, an ordinary preview and brief QA notes. Add PDF/PNG/TIFF at the user's requested resolution and any statistical outputs the task needs.

State what was actually verified: native shape/text counts, zero group/picture counts for an all-vector plot, size match and visual inspection. File-structure checks are not proof of successful interaction in PowerPoint; claim a live PowerPoint test only after performing it. Never call a raster placement or a grouped import “fully editable”.

Keep delivery concise. Link the paired final files and the reproducible source. Explain any explicitly agreed raster exception or unsupported effect instead of silently dropping it.
