# Visual Focus And Rewrite Rules

Use this reference after selecting keyframes and before inserting visuals into the final PDF. The goal is to move from "screenshot as evidence" to "visual material as teaching."

## Three-Layer Visual Asset Model

Every important visual moment should be separated into three layers:

1. `evidence_frame`: the original selected source frame, kept for audit.
2. `focus_crop`: a cropped or zoomed version that isolates the part of the frame that answers the visual question.
3. `rewritten_teaching_visual`: a Codex-designed AI rewrite or Codex-composited teaching visual that explains the mechanism cleanly.

The final PDF main body should prefer `rewritten_teaching_visual`. Use `focus_crop` when the original visual appearance itself is important. Keep the raw `evidence_frame` in the visual evidence appendix or audit section unless the user explicitly wants original screenshots in the main body.

## Required Directories

```text
output/
  figures/                 # selected original evidence frames for audit
  crops/                   # focused crops/zooms derived from selected frames
  rewritten_keyframes/
    prompts/               # image rewrite prompts and overlay specs
    backgrounds/           # AI-generated bitmap backgrounds, no dense text
    overlays/              # Codex-authored SVG labels, arrows, legends
    final/                 # composited rewritten visuals inserted in PDF
  diagrams/
    backgrounds/
    overlays/
    final/
```

`diagrams/` explains abstract mechanisms. `rewritten_keyframes/` explains a concrete selected keyframe by simplifying or redrawing it. The two may overlap, but keep both concepts distinct in records.

## `visual_focus_crops.json`

Create this file before visual rewrite.

```json
[
  {
    "id": "CROP001",
    "source_frame_id": "FIG001",
    "source_frame_path": "figures/fig001.jpg",
    "knowledge_point_id": "KP001",
    "visual_question": "",
    "focus_target": "price position | order panel | stop line | value area | POC | caption | speaker gesture | dashboard value",
    "crop_box_pixels": {"x": 0, "y": 0, "width": 0, "height": 0},
    "crop_path": "crops/crop001.jpg",
    "why_this_crop": "",
    "what_it_shows": [],
    "what_it_does_not_show": [],
    "needs_ai_rewrite": true,
    "rewrite_reason": "too cluttered | platform-specific | text too small | concept needs abstraction | privacy/branding reduction | direct screenshot insufficient"
  }
]
```

Cropping is not optional when the selected frame contains large irrelevant areas and the teaching point is local. The crop must make the key evidence more readable than the full frame.

## `visual_rewrite_prompts.json`

Create this file before generating AI-rewritten visuals.

```json
[
  {
    "id": "VR001",
    "source_frame_id": "FIG001",
    "source_crop_id": "CROP001",
    "knowledge_point_id": "KP001",
    "source_time_range": "00:00:00--00:00:00",
    "teaching_objective": "",
    "learner_confusion": "",
    "visual_summary_of_source": "",
    "rewrite_strategy": "simplify_chart | redraw_interface | abstract_mechanism | compare_before_after | zoom_and_annotate | flow_diagram",
    "must_preserve": [],
    "must_remove_or_simplify": [],
    "must_not_imply": [],
    "image_model_prompt": "",
    "negative_prompt": "",
    "overlay_spec": {
      "labels": [],
      "arrows": [],
      "callouts": [],
      "legend": [],
      "source_note": ""
    },
    "background_path": "rewritten_keyframes/backgrounds/vr001.png",
    "overlay_path": "rewritten_keyframes/overlays/vr001.svg",
    "final_path": "rewritten_keyframes/final/vr001.png",
    "review_status": "pending | accepted | rejected | revised"
  }
]
```

The prompt must describe the teaching goal, not just ask for a prettier chart. It should state what the original screenshot contains, what is distracting, and what the rewritten visual should help the learner understand.

## Codex-Native Image Generation Policy

For polished rewritten visuals, prefer Codex's in-session image generation capability when available. Do not require a local `OPENAI_API_KEY` by default.

Use modes in this order:

1. `codex_image_plus_svg_labels`: preferred Codex-native mode. Codex generates a clean mostly text-free bitmap visual, then Codex adds exact SVG labels and arrows.
2. `codex_svg`: transparent fallback when Codex image generation cannot produce a local reusable asset in the current environment.
3. `image_model_plus_svg_labels`: optional local/API batch mode, only when the user explicitly asks for or approves API-key based generation.

Use the image model for:

- clean abstract chart backgrounds;
- professional composition;
- simplified price paths, zones, order blocks, or dashboard silhouettes;
- visual hierarchy and polish.

Do not use the image model for:

- dense Chinese labels;
- exact formulas;
- exact prices, account balances, or platform numbers;
- source citations;
- broker/platform UI reconstruction that looks like a real account statement;
- unsupported future price paths or guaranteed outcomes.

Codex must own the exact text layer through SVG overlays. Put Chinese labels, arrows, legends, and source notes in `rewritten_keyframes/overlays/` or `diagrams/overlays/`.

If Codex image generation is unavailable or cannot save a stable local file, fall back to `codex_svg`, but record the downgrade in `visual_rewrite_prompts.json`, `diagram_prompts.json`, `run_manifest.json`, and `quality_review.md`. Missing `OPENAI_API_KEY` is not a failure unless the user explicitly requested local API mode.

## Main Body Insertion Policy

The final PDF main body should use this priority:

1. AI-rewritten teaching visual, when a screenshot is cluttered or platform-specific.
2. Focus crop, when source authenticity matters and the crop clearly answers the visual question.
3. Full raw screenshot only when the entire interface context is pedagogically necessary.

Raw full screenshots should normally be moved to a visual evidence appendix with contact sheets. Captions must label them as source evidence, not teaching diagrams.

## Rewrite Review

Before a rewritten visual enters the PDF, record a review:

- does it answer the original visual question?
- does it preserve the source evidence without inventing unsupported claims?
- is the key teaching element more readable than the screenshot?
- are Chinese labels controlled by SVG/Codex rather than baked into the bitmap?
- are arrows, colors, and callouts consistent with the series style?
- does it avoid fake platform data, guaranteed-profit implications, and misleading precision?

Reject or revise any rewritten visual that looks generic, decorative, visually noisy, or less informative than the crop.

## Caption Standard

Main-body caption:

```text
教学改写图：根据 00:10:38--00:10:46 原视频截图和字幕重写，用于说明 risk-free position 是止损管理状态，不代表没有滑点或执行风险。
```

Appendix evidence caption:

```text
原始证据帧：00:10:41.500，显示交易界面与字幕语境。该截图只证明画面中可见内容，不证明最终成交结果。
```
