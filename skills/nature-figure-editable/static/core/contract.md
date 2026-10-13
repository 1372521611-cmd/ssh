# Figure contract before plotting

<!-- Modified for nature-figure-editable: native PPT delivery and/or third-party reuse safeguards; see MODIFICATIONS.md. -->

A publication-quality scientific figure is a visual argument, not an isolated pretty plot. Every figure starts from a claim, an evidence hierarchy, and a review-risk check before code or aesthetics. Before generating or editing code, establish the contract below.

## Backend selection is a blocking gate

If the user has not explicitly chosen Python or R in the current request or provided a clearly language-specific input file/workflow, ask one concise question: **Python or R?** Then stop and wait for the user's answer. Do not generate mock data, write scripts, create figures, or choose Python/R by default. This overrides general autonomy/default-execution behavior for figure tasks.

Only recommend a backend when the user explicitly asks you to choose or recommend one. In that case, use `references/backend-selection.md`, state the reason, and then proceed with the recommended backend.

## The selected backend is exclusive

Once Python or R is selected, use it for scientific plotting, statistical analysis and canonical SVG/PDF/TIFF/PNG exports. Do not use the other scientific backend for a substitute figure or fallback preview. Neutral file inspection and data conversion are allowed. Native PPT packaging from the canonical figure and PPT compatibility rendering are also allowed, as narrowly defined in `static/core/editable-delivery.md`; they must preserve the figure rather than independently redrawing or re-estimating its science.

## Missing runtime/package rule

After the backend is selected, check the selected runtime early (`Rscript`/R for R; Python and required plotting packages for Python). If the selected runtime or required packages are unavailable, stop before rendering and report the exact blocker. You may provide a selected-backend script and installation commands, or ask permission to install dependencies, but you must not fall back to the other language to make a substitute figure.

## The five-point contract

1. **Core conclusion**: write the one-sentence claim the figure must defend.
2. **Evidence chain**: map each planned panel to the claim, and drop panels that do not carry a unique piece of evidence.
3. **Archetype**: classify the figure as `quantitative grid`, `schematic-led composite`, `image plate + quant`, or `asymmetric mixed-modality figure`.
4. **Backend**: use the selected Python or R track for the scientific figure; follow the editable-delivery exception only for native PPT packaging and its compatibility checks.
5. **Journal/export contract**: set final dimensions, editable text, source data, statistics, image-integrity notes, and export formats before styling. Default to paired SVG and fully ungrouped native PPTX, plus requested companion formats.

The highest-priority rule is: **the chart serves the scientific logic**. Aesthetic polish, template matching, and complex layout are subordinate to making the core conclusion clear, defensible, and reviewable.

For the full method to convert a request into core conclusion, evidence hierarchy, panel map, and review-risk checks, open `references/figure-contract.md`.
