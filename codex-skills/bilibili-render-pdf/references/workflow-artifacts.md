# Workflow Artifacts And Phase Gates

This reference defines the required intermediate artifacts for the video-to-teaching-note workflow.

## Directory Layout

Use a run-specific output directory:

```text
output/
  acquisition_manifest.json
  url_list_normalized.txt
  source/
    source_video.mp4
    source_subtitle.srt
    source_transcript.txt
    source_metadata.json
    cover.jpg
  srt/
  items/
    item_001/
      metadata_probe.json
      raw/
      source/
      srt/
  candidate_frames/
  contact_sheets/
  figures/
  crops/
  rewritten_keyframes/
    prompts/
    backgrounds/
    overlays/
    final/
  diagrams/
    backgrounds/
    overlays/
    final/
  pdf_preview/
  knowledge_points.json
  keyframe_segments.json
  frame_selection_record.md
  frame_interpretations.md
  visual_evidence_analysis.md
  visual_focus_crops.json
  visual_rewrite_prompts.json
  visual_rewrite_review.md
  diagram_prompts.json
  diagram_review.md
  source_coverage_report.json
  source_coverage_report.md
  writing_plan.json
  writing_review.md
  knowledge_cards_expanded.json
  review_questions_with_answers.md
  novice_comprehension_review.md
  run_manifest.json
  quality_report.json
  quality_review.md
  qa_review.md
  final_checklist.md
  notes.tex
  notes.pdf
```

`candidate_frames/` is temporary by default. Delete unused raw candidates after final frame selection unless the user requests debug/audit retention.

## Phase Gates

Do not move to the next phase until the required artifact exists.

| Phase | Required artifact | Gate |
|---|---|---|
| source acquisition | `acquisition_manifest.json`, `source/` and `srt/` when URL input is used | URL inputs are deduplicated, selected video/subtitle/metadata are normalized, or `needs_asr`/visual-only is explicitly recorded |
| transcript understanding | `knowledge_points.json` | every major teaching point has a timestamp and explanation |
| visual planning | `keyframe_segments.json` | every segment starts from a knowledge point and visual question |
| dense extraction | `candidate_frames/`, `contact_sheets/` | each visual question has a dense candidate set |
| frame choice | `frame_selection_record.md` | chosen and rejected frames have reasons |
| frame interpretation | `frame_interpretations.md` | selected frames are interpreted as facts/inferences/limits |
| focus crop | `visual_focus_crops.json` when needed | loose frames have explicit crop targets and crop boxes |
| keyframe rewrite | `visual_rewrite_prompts.json`, `rewritten_keyframes/final/` when needed | cluttered screenshots are rewritten into teaching visuals before main-body insertion |
| evidence fusion | `visual_evidence_analysis.md` | transcript and frame evidence are merged |
| diagram design | `diagram_prompts.json` | each diagram has an explicit prompt before asset generation |
| diagram review | `diagram_review.md` | every teaching diagram has mode, source evidence, quality result, and support boundary |
| source coverage | `source_coverage_report.json`, `source_coverage_report.md` | important transcript details are included, expanded, or explicitly omitted with reason |
| pedagogical writing | `writing_plan.json`, `writing_review.md` | final narrative is planned as novice-readable textbook flow, not raw subtitle order |
| textbook support | `knowledge_cards_expanded.json`, `review_questions_with_answers.md` when applicable | core concepts and review questions are complete enough for independent study |
| final document | `notes.tex`, `notes.pdf` | XeLaTeX succeeds |
| cleanup | `run_manifest.json`, `final_checklist.md` | unused candidates removed or explicitly retained |
| independent QA | `qa_review.md`, `quality_review.md`, `quality_report.json` | a separate QA pass finds no blocking findings before final/pass |

## `run_manifest.json`

Record enough information to audit the run:

```json
{
  "workflow": "bilibili-render-pdf-knowledge-visual-v2",
  "input_mode": "bilibili_url | youtube_url | url_file | local_video | local_video_plus_transcript",
  "source_acquisition_manifest": "",
  "source_acquisition_status": "ready | metadata_only | needs_asr | visual_only | skipped_for_local_input",
  "video_file": "",
  "transcript_file": "",
  "segment": "00:00:00--00:20:00",
  "candidate_frame_interval_seconds": 0.5,
  "knowledge_points_total": 0,
  "visual_segments_total": 0,
  "candidate_frames_total_before_cleanup": 0,
  "candidate_frames_kept_after_cleanup": 0,
  "candidate_frames_deleted": 0,
  "contact_sheets_total": 0,
  "final_figures_total": 0,
  "crop_assets_total": 0,
  "rewritten_keyframe_assets_total": 0,
  "visual_focus_crops_total": 0,
  "visual_rewrite_prompts_total": 0,
  "diagram_assets_total": 0,
  "teaching_diagram_mode": "codex_image_plus_svg_labels | codex_svg | image_model_plus_svg_labels_approved_api | codex_tikz | mixed",
  "codex_native_mode": true,
  "external_api_user_approved": false,
  "codex_image_diagrams_total": 0,
  "approved_api_image_model_diagrams_total": 0,
  "codex_svg_diagrams_total": 0,
  "codex_tikz_diagrams_total": 0,
  "diagram_backgrounds_total": 0,
  "diagram_overlays_total": 0,
  "diagram_final_assets_total": 0,
  "source_coverage_segments_total": 0,
  "source_coverage_omissions_total": 0,
  "writing_sections_total": 0,
  "writing_review_passed": false,
  "novice_textbook_mode": false,
  "expanded_knowledge_cards_total": 0,
  "review_questions_total": 0,
  "debug_keep_candidates": false,
  "final_pdf": "",
  "final_tex": "",
  "qa_reviewer": "independent_agent | separate_local_review",
  "qa_review": "",
  "quality_report": "",
  "quality_gate_passed": false,
  "blocking_findings": [],
  "limitations": [],
  "final_checklist": {}
}
```

## Final vs Draft Naming

Use draft naming until all required phases are complete.

- `draft_notes.tex` / `draft_notes.pdf`: allowed before full visual interpretation, diagrams, cleanup, or checklist.
- `notes.tex` / `notes.pdf`: allowed only when every phase gate is satisfied.
- `final_knowledge_document.md`: allowed only after independent QA passes when the workflow creates a Markdown final. Use a draft name before QA.

If the user asks for a quick preview, produce a draft and state what phases remain incomplete.
