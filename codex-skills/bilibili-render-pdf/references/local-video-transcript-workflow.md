# Local Video + Timestamped Transcript Workflow

This reference captures the restored workflow that worked best in the first-20-minute finance video test. Use it when the user supplies a local video and a matching timestamped transcript.

## 1. Normalize Inputs

Create a run directory. Copy or reference:

- source video path;
- transcript path;
- optional scope, such as `00:00:00--00:20:00`;
- output language, normally `zh-CN`.

Normalize the transcript into stable entries:

```json
{
  "line_id": "L0001",
  "speaker": "S01",
  "start_time": "00:00:00.000",
  "end_time": null,
  "text": "..."
}
```

Preserve timestamps and source line ids. These ids must be used later in chapter plans, knowledge blocks, visual questions, and final notes.

## 2. Semantic Chapter Planning

Read the transcript before splitting. Create `semantic_chapter_plan.json`.

Each chapter must include:

- `chapter_id`
- Chinese title
- start/end time
- start/end line ids
- boundary reason
- core topic
- learning goal
- key line ids

Rules:

- Do not split by fixed 10-minute windows.
- Split when the speaker changes task, market state, trade lifecycle, reasoning mode, or teaching goal.
- For long videos, process chapter batches incrementally and later merge them.

## 3. Knowledge Extraction

Create `knowledge_blocks.json`.

Each block should include:

- source chapter and source lines;
- concise Chinese summary;
- core claim;
- facts vs inference vs speaker opinion;
- finance/trading concepts;
- risk notes;
- visual questions that would improve or verify the note.

The visual questions should come from unclear or visually dependent parts of the transcript, not from a keyword list.

## 4. Visual Retrieval Plan

Create `visual_retrieval_plan.json` and `.md`.

Each visual retrieval question must be atomic:

```json
{
  "question_id": "VRQ001",
  "knowledge_block_id": "KB002",
  "priority": "high",
  "question_type": "price_structure",
  "evidence_unit": "micro_clip",
  "target_time": "00:06:58.000",
  "micro_clip": {
    "start": "00:06:57.000",
    "end": "00:06:59.000",
    "fps": 6
  },
  "claim_to_verify": "...",
  "question": "...",
  "evidence_needed": ["..."],
  "success_criteria": ["..."],
  "minimum_support_level": "partial",
  "unacceptable_substitutes": ["..."],
  "candidate_frames": [
    "00:06:54.000",
    "00:06:54.500",
    "00:06:55.000"
  ],
  "answer_required_for": "..."
}
```

Default candidate frame policy:

- center on the target timestamp;
- sample from `target - 4s` to `target + 4s`;
- interval: 0.5 seconds;
- make a contact sheet before final selection.

Use micro-clips for:

- order movement;
- candles forming;
- trade entry/exit;
- price reacting to a zone;
- any claim that depends on sequence, not one static frame.

## 5. Frame And Micro-Clip Review

Inspect candidate frames visually. Then write `visual_retrieval_state.json`.

For each visual question, assign:

- `direct`: the visual directly answers the question;
- `partial`: useful but missing some readable detail;
- `context_only`: relevant scene but does not prove the claim;
- `not_supported`: does not support the claim.

Also assign final use policy:

- `use_as_evidence`
- `use_with_uncertainty`
- `context_only`
- `do_not_use`

Never upgrade a weak frame because the transcript says the concept nearby. The image must support the exact claim.

## 6. Visual Learning Notes

Create `visual_learning_notes.md` and, when useful, `visual_learning_units.json`.

A visual learning unit should include:

- what the frame/clip visibly shows;
- what it solves in the note;
- what remains uncertain;
- how to rewrite the visual observation into teaching prose;
- recommended caption;
- source time interval.

This is the key step that made the first-20-minute version better: the image is not pasted into notes; it is first converted into a teaching observation.

## 7. Source Coverage And Textbook Writing Plan

For trading videos, default to a zero-foundation textbook target unless the user explicitly asks for a brief note.

Create `source_coverage_report.json` and `source_coverage_report.md` before `writing_plan.json`.

For each semantic segment, audit:

- time range and source line ids;
- main content;
- key concepts;
- key numbers;
- trading actions;
- whether it enters the textbook;
- where it enters;
- whether it was compressed;
- whether it needs expansion, screenshots, teaching diagrams, or manual review.

Create `writing_plan.json` before drafting the final note. It must turn knowledge blocks, visual learning notes, diagram review, and source coverage into a teaching sequence.

For each major section, decide:

- the learner question or confusion;
- why the topic matters;
- the core idea in plain Chinese;
- the mechanism or decision process;
- transcript and visual evidence to use;
- what the evidence cannot prove;
- the section takeaway.

Do not simply concatenate chapter summaries. Reconstruct the teaching flow when that improves understanding, while preserving source line ids and timestamps.

For novice trading textbooks:

- add a prerequisite chapter before the source-video chapters;
- split any chapter that introduces more than three new novice terms;
- expand each complex concept using plain language, source scene, and professional boundary;
- include full trade-case replay whenever a concrete trade, cancelled plan, stop move, partial exit, or no-trade decision appears;
- include review questions with standard answers;
- prefer multi-volume output over compressing important source details.

Create `writing_review.md` after the plan. Confirm that each major section has motivation, mechanism, evidence/example, boundary/risk, and takeaway when applicable.

Create `integrated_knowledge_document.draft.md`.

Recommended structure:

1. 原文覆盖率报告
2. 教材总目录
3. 新手基础概念预备章
4. 正文教材章节
5. 完整知识卡片
6. 关键交易案例复盘
7. 图像 / 截图 / 示意图补充清单
8. 复习题与标准答案
9. 新手理解质检报告
10. 仍需人工复核的问题清单

Write in Chinese. Keep the explanation faithful to source lines and visual support levels.

When evidence is partial, write it as partial:

- “画面支持该解释的一部分，但无法直接读出 value area low 标签。”
- “可作为 squeeze 假设的视觉背景，不能写成清算已经发生。”
- “risk-free 在这里是账户级盈利垫语境，不是字面无风险。”

## 7.5 Teaching Diagram Generation

Create teaching diagrams only after visual learning notes exist.

Default mode for polished final notes:

- use `codex_image_plus_svg_labels` when Codex image generation is available;
- use Codex image generation for clean conceptual background only;
- use Codex-authored SVG/LaTeX text for all Chinese labels and arrows;
- save background, overlay, and final composited asset separately;
- write `diagram_review.md` before inserting diagrams into the final PDF.

Fallbacks:

- use `codex_svg` when Codex image generation is unavailable or when exact editability matters more than polish;
- use local/API `image_model_plus_svg_labels` only when the user explicitly approves API-key based batch generation;
- use `codex_tikz` only for simple formulaic diagrams, not as the default visual style.

Do not accept Codex/image-model output with malformed Chinese, fake platform labels, decorative clutter, or unsupported trading claims.

## 8. Quality Gate

Create `quality_report.json` and `quality_review.md`.

Final output is allowed only when:

- semantic chapters exist and are not fixed-window splits;
- knowledge blocks cover all chapters;
- high-priority visual questions are reviewed;
- every final figure has a support grade and final-use policy;
- no placeholder text remains;
- review questions exist;
- finance/trading risk warnings are present;
- teaching diagrams pass visual review and label-accuracy review;
- if Codex/image-model diagrams are used, exact Chinese labels are controlled by Codex overlay files;
- source_coverage_report.json and .md exist;
- writing_plan.json exists and the final narrative is not a raw subtitle dump;
- writing_review.md confirms source coverage, novice readability, term definitions, figure integration, chapter summaries, review answers, and final synthesis;
- substantial trading chapters include prerequisite terms, source scene, timestamped evidence, mechanism breakdown, common misconceptions, risk boundary, summary, and review questions with answers;
- the final document is Chinese.

If the gate fails:

- keep `integrated_knowledge_document.draft.md`;
- keep `visual_analysis_jobs.json`;
- do not create `final_knowledge_document.md`.

## 9. Finalization

When quality gates pass, create `final_knowledge_document.md`.

The final document may include knowledge cards, professional finance analysis, and review questions. That is intentional for Mode A. It is different from the strict Bilibili PDF-only mode.
