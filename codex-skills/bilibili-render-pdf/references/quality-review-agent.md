# Quality Review Agent

Use this reference before any generated package is marked final/pass.

The reviewer must be independent from the generation step. If sub-agents are available and the user has allowed agent use, spawn a separate QA reviewer. If not, perform a separate review pass and explicitly state that no independent agent was available. The reviewer does not write the lesson, choose frames, repair assets, or soften findings. Its job is to block regressions, false claims, and self-approval.

## QA Inputs

Inspect at least:

- `notes.tex`
- `notes.pdf` or rendered preview pages
- `run_manifest.json`
- `quality_report.json`
- `visual_focus_crops.json`
- `visual_rewrite_prompts.json`
- `visual_rewrite_review.md`
- `diagram_prompts.json`
- `diagram_review.md`
- `figures/`
- `crops/`
- `rewritten_keyframes/`
- `diagrams/`
- `final_knowledge_document.md` when this workflow creates it
- `pdf_preview/` rendered page images when available
- any prior invalid or superseded output directory mentioned in the run context

## Blocking Findings

Any of the following blocks final/pass:

1. The run reuses, copies, or renames a known invalid/superseded output as the current final output.
2. A main-body visual references `figures/*.jpg`, `crops/*`, `contact_sheets/*`, or another raw/audit asset without either:
   - a corresponding AI-rewritten main-body visual, or
   - an explicit exception explaining why the raw screenshot itself is necessary.
3. `visual_rewrite_prompts.json` does not cover every selected frame that enters the main body.
4. The report claims `codex_image_plus_svg_labels`, but no image-generated background asset exists in `diagrams/backgrounds/` or `rewritten_keyframes/backgrounds/`.
5. Python, PIL, SVG, TikZ, deterministic plotting, or any other mechanical renderer produced the teaching visual, but the run describes it as AI/Codex image generation.
6. Old fallback wording remains in scripts or delivered files, including phrases such as `PIL-only`, `PIL rendered`, `Python/PIL only`, `local PIL rendered`, `def create_rewrite`, or paths such as `teaching_visuals/final` from earlier rejected versions.
7. `codex_image_diagrams_total`, `ai_visual_backgrounds_total`, and `approved_api_image_model_diagrams_total` are all zero while the user asked for image-model or Codex-generated teaching visuals.
8. The final checklist says pass while the manifest or report contains limitations that contradict pass.
9. The PDF is compiled successfully but the required AI visual rewrite or image-generation work is incomplete.
10. `candidate_frames/` still contains unused dense candidate images after final frame selection unless `debug_keep_candidates=true` and the user explicitly asked for audit retention.
11. The final Markdown/PDF omits mandatory synthesis or study-support sections required by the current workflow, such as a learning route, core term review, knowledge cards, review template, review questions, or manual-correction list when those were part of the requested output.
12. The final writing exposes a repeated fill-in-the-blank chapter template instead of a teaching narrative, or it fails the anti-template standard in `textbook-writing-benchmarks.md`.
13. `quality_report.json` claims `status: pass` or `quality_gate_passed=true` while any blocking finding above is true.
14. Any final text artifact contains mojibake, replacement-character corruption, or path/encoding errors that make the result hard to read.

## Required Mechanical Checks

Run or equivalent-check these before deciding:

- list all main-body image references in `notes.tex` and verify they point to `rewritten_keyframes/final/` or approved `diagrams/final/` assets unless an exception is documented;
- count `rewritten_keyframes/backgrounds`, `rewritten_keyframes/final`, `diagrams/backgrounds`, and `diagrams/final`; compare counts with `run_manifest.json` and `quality_report.json`;
- count `candidate_frames/` after cleanup;
- search delivered scripts and text artifacts for old fallback markers: `PIL-only`, `PIL rendered`, `Python/PIL only`, `local PIL rendered`, `def create_rewrite`, `teaching_visuals/final`;
- inspect `quality_report.json` fields for contradictions: image mode, external API usage, `blocking_findings`, `pdf_pages`, `main_body_raw_screenshot_refs`, and `quality_gate_passed`;
- if a previous invalid directory exists, compare representative file hashes or timestamps to verify the current output is newly generated and not a rename.

## Required QA Output

Create `qa_review.md` with:

- final decision: `pass`, `draft_needs_review`, or `fail`
- blocking findings
- non-blocking findings
- exact file references
- which status fields must be changed
- next repair steps
- whether this review was performed by a separate agent or by a separate local review pass
- the exact mechanical checks performed, including counts

Update:

- `run_manifest.json`
- `quality_report.json`
- `quality_review.md`
- `final_checklist.md`

Use `quality_gate_passed=true` only when there are no blocking findings.

## Status Semantics

- `pass`: all mandatory workflow gates passed, including AI visual requirements when requested.
- `draft_needs_review`: text/PDF may be useful for review, but one or more mandatory gates are incomplete.
- `fail`: output is misleading, corrupted, unusable, or contradicts the requested workflow.
