# AI Teaching Diagram Rules

Teaching diagrams must be designed after frame interpretation, focus cropping, visual rewrite planning, and evidence fusion. Do not generate diagrams before knowing what they need to explain.

Do not treat diagram generation as "make this screenshot prettier." First write the teaching problem and prompt. Then generate the visual. Then review it against the prompt.

## Output: `diagram_prompts.json`

Use this schema:

```json
[
  {
    "id": "DIA001",
    "knowledge_point_id": "KP001",
    "source_frames": ["figures/fig001.jpg"],
    "source_time_ranges": ["00:04:43--00:04:51"],
    "teaching_objective": "",
    "why_screenshot_is_not_enough": "",
    "why_focus_crop_or_rewritten_keyframe_is_not_enough": "",
    "required_elements": [],
    "relationships": [],
    "labels": [],
    "color_semantics": {},
    "layout": "",
    "must_not_imply": [],
    "preferred_output": "svg | tikz | pdf | png",
    "generation_method": "codex_image_plus_svg_labels | codex_svg | image_model_plus_svg_labels | codex_tikz | deterministic_plot",
    "style_spec": {
      "tone": "professional Chinese course-note visual",
      "palette": [],
      "background": "",
      "label_style": "",
      "avoid": []
    },
    "prompt": "",
    "image_model_prompt": "",
    "negative_prompt": "",
    "label_overlay_spec": {
      "labels": [],
      "arrows": [],
      "callouts": [],
      "legend": [],
      "source_note": ""
    },
    "background_path": "",
    "overlay_path": "",
    "output_path": "",
    "review_status": "pending | accepted | rejected | revised"
  }
]
```

## Generation Mode Selection

Choose the mode by teaching need:

1. `codex_image_plus_svg_labels`: default Codex-native mode for polished conceptual teaching diagrams. Use the in-session Codex image capability for the bitmap background when available.
2. `codex_svg`: preferred when exact editability and label precision matter, and the diagram can look good as a clean vector schematic.
3. `image_model_plus_svg_labels`: optional local/API batch mode, only when the user explicitly asks for or approves API-key based generation.
4. `codex_tikz`: use only for formulas, compact geometric diagrams, or LaTeX-native mechanisms. Do not use TikZ as the default for polished teaching visuals.
5. `deterministic_plot`: use only for actual charts based on data, formulas, or exact geometry.

Python may render, crop, convert, composite, or validate images. Python should not silently decide the teaching logic.

If Codex image generation is not available or cannot save a stable local asset, fall back to `codex_svg` and record the downgrade in `diagram_prompts.json`, `run_manifest.json`, and the quality review. Missing `OPENAI_API_KEY` is not a failure unless the user explicitly requested local API mode. Do not describe a fallback SVG as a polished image-model result.

## Codex Image Plus SVG Labels

Use this mode when the user wants better-looking teaching diagrams and Codex image generation is available in the current session, or when the user explicitly approved local/API batch generation.

Workflow:

1. Write `diagram_prompts.json` first.
2. Generate a clean background with Codex image generation by default:
   - no dense Chinese text
   - no small formulas
   - no exact price labels
   - no source citation text
   - no hallucinated platform UI or fake broker branding
3. Save the background in `diagrams/backgrounds/`.
4. Create a Codex-authored SVG overlay in `diagrams/overlays/` containing:
   - exact Chinese labels
   - arrows and callouts
   - color legend
   - source evidence note if needed
   - caution text such as "不代表保证盈利" when relevant
5. Composite the background and overlay into `diagrams/final/`.
6. Insert only the final reviewed asset into the PDF.

Codex image generation is responsible for visual polish, composition, and clean abstract scene design. Codex-authored overlay files are responsible for conceptual correctness, Chinese text, arrows, labels, evidence boundaries, and source references. Local API generation is only an approved batch alternative.

Do not accept a generated image if it includes malformed Chinese, fake chart numbers, invented platform names, fake broker statements, guaranteed-profit implications, or visual claims that exceed the evidence.

## Prompt-First Diagram Workflow

For each diagram:

1. Write the exact teaching objective in one sentence.
2. Write the learner confusion the diagram will resolve.
3. List source frames, focus crops, transcript timestamps, and support boundaries.
4. Decide whether this should be a rewritten keyframe or an abstract teaching diagram.
5. Create `diagram_prompts.json`.
6. Generate the Codex/image-model background only after the prompt exists.
7. Add Codex-controlled SVG labels and arrows.
8. Composite and review the final asset.

If steps 1-5 are missing, the diagram cannot enter the final PDF.

## Prompt Standard

Each prompt must be precise enough that another agent could generate the same diagram without reading the whole transcript.

Include:

- the learner's confusion
- the mechanism to explain
- the required objects
- how objects relate
- labels and language
- what to avoid
- source evidence
- visual style and output mode
- whether labels belong in the bitmap or the SVG overlay

Example:

```text
Mode: codex_image_plus_svg_labels.

Create a polished professional course-note background explaining why "risk-free position" in this trading video means a stop-management state, not absence of all risk. The bitmap background should show a clean abstract price path rising from an entry area, an initial risk zone below entry, and a later protected zone. Do not include Chinese text, exact numbers, broker UI, or fake platform labels in the bitmap.

SVG overlay labels: 入场价, 初始止损, 移动后止损, 初始风险区, 已保护区域, 目标区, 仍有滑点/执行风险. Use green for protected/profit area, red for initial risk, blue for entry, and purple for target. Do not imply guaranteed profit. Source: KP010, frame FIG005, transcript 00:10:38--00:10:46.
```

## Visual Style Standard

A final teaching diagram should look like a professional finance course visual:

- clean white or subtle neutral background
- restrained color palette with consistent semantics
- generous spacing
- readable Chinese labels
- no decorative clutter
- no platform branding unless it is directly from a source screenshot
- no tiny text
- no low-resolution blur
- no overlapping labels or arrows
- no rough engineering-sketch appearance when image generation is available
- no decorative gradients or generic shapes that do not explain the mechanism

For a series of diagrams in one PDF, keep a shared style system: same palette, label size, arrow style, caption tone, and caution-note treatment.

## Diagram Review

Before inserting a diagram into the PDF:

- check it matches the prompt
- check it does not introduce unsupported claims
- check labels are readable
- check it is not decorative
- check it complements rather than duplicates the screenshot
- check Chinese text is controlled by Codex and is exact
- check visual quality is better than a rough engineering sketch
- check `background_path`, `overlay_path`, and `output_path` exist when using `codex_image_plus_svg_labels` or approved `image_model_plus_svg_labels`
- record review status in `diagram_prompts.json`

## PDF Insertion

In the LaTeX/PDF:

- label AI diagrams as teaching diagrams or schematic diagrams
- do not present them as original video screenshots
- cite the related source time range in the caption or nearby prose when helpful
- keep visual style consistent across diagrams
- if using `codex_image_plus_svg_labels` or approved `image_model_plus_svg_labels`, insert the composited final asset and keep the background/overlay files for audit
