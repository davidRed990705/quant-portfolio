---
name: bilibili-render-pdf
description: Generate a professional Chinese teaching-note PDF from a Bilibili/YouTube URL, URL list, local video, or video plus timestamped transcript. Use when the user wants a Codex-native learning workflow that uses Codex for transcript understanding, finance knowledge extraction, visual question design, keyframe interpretation, AI teaching-visual design, source coverage audit, and zero-foundation textbook writing, while using tools only for mechanical media/file/PDF operations. Supports video/subtitle acquisition from Bilibili or YouTube, including Bilibili multi-part URLs and local-video adaptation.
---

# Bilibili Render PDF

Use this skill to turn a Bilibili/YouTube URL, URL list, or local video/transcript pair into a Chinese teaching-note package and a compiled PDF.

This is a Codex-native skill. Codex must lead the intellectual work: transcript understanding, semantic chaptering, knowledge extraction, visual interpretation, teaching-visual design, and final Chinese writing. Scripts and external tools are mechanical helpers only: frame extraction, crop application, contact sheets, compositing, LaTeX compilation, and cleanup.

Do not default to local API-key pipelines or external services. Use Codex platform capabilities first. If a local API, external model, or batch script would replace Codex judgment, explain the mode and get user approval.

This skill is not a simple summarizer. It must behave like a learning workflow:

1. understand the transcript first
2. decide which knowledge points need visual evidence
3. build subtitle-aligned dense candidate frames
4. inspect and interpret selected frames
5. crop or zoom selected frames around the actual visual question
6. rewrite selected keyframes into cleaner AI teaching visuals when screenshots are cluttered
7. fuse transcript evidence with visual evidence
8. design AI-generated teaching diagrams
9. audit source coverage and preserve important details
10. create a zero-foundation pedagogical writing plan
11. compile the final LaTeX/PDF
12. run independent QA before final/pass
13. clean unused candidate frames before delivery

## Required References

Read only the references needed for the current run:

- For default ownership between Codex and mechanical tools, read `references/codex-native-workflow.md`.
- For Bilibili/YouTube URL download, subtitle acquisition, URL-file deduplication, and source hand-off rules, read `references/source-acquisition.md`.
- For artifact names, schemas, and phase gates, read `references/workflow-artifacts.md`.
- For detailed knowledge extraction and finance/technical term explanation rules, read `references/knowledge-points.md`.
- For keyframe selection, frame interpretation, evidence fusion, and cleanup rules, read `references/visual-analysis.md`.
- For focus crops, AI keyframe rewrite, and main-body visual insertion policy, read `references/visual-rewrite.md`.
- For AI-generated teaching diagram prompts and output rules, read `references/ai-teaching-diagrams.md`.
- For teaching narrative, section writing, formula/code/box usage, and final synthesis rules, read `references/pedagogical-writing.md`.
- If the writing starts to feel repetitive, mechanical, or template-filled, read `references/textbook-writing-benchmarks.md` and apply its anti-template quality gate.
- Before marking any output final/pass, read `references/quality-review-agent.md` and run the independent QA gate.

## Inputs

Accept either:

- a Bilibili URL, BV number, b23 short link, or YouTube URL
- a local text file containing one or more video URLs
- a local video file
- a local timestamped transcript/SRT file
- a local video plus timestamped transcript

For Bilibili/YouTube URL inputs, run source acquisition before transcript understanding. For Bilibili URLs, inspect metadata first: title, parts, duration, thumbnail, subtitles, and available formats. If the video is multi-part and the URL contains `p=N`, process that exact part. If it is multi-part and the user did not specify a part, ask which part to process unless the user requested batch processing.

For local video inputs, record the local adaptation explicitly in `run_manifest.json`. If no platform cover is available, use a representative preview frame and state that limitation.

## Codex vs Tools

Default to Codex-native execution:

- Codex decides what the transcript means, where semantic boundaries are, which knowledge points matter, what visual questions to ask, how to interpret images, how to design teaching visuals, and how to write the textbook.
- Tools perform deterministic operations only: download/locate media, parse files, extract frames, crop according to Codex's decision, compose images, compile PDF, and clean files.
- A script may store Codex decisions into JSON, but it must not silently make teaching, finance, visual, or writing judgments on Codex's behalf.
- If you plan to use a local OpenAI API key, external API, external model, or non-Codex batch generator, tell the user first and ask for approval unless the user explicitly requested that mode.

Missing `OPENAI_API_KEY` is not a failure in Codex-native mode. It only means optional local batch API generation is unavailable. Use Codex's in-session capabilities or a transparent SVG/crop fallback instead.

## Source Acquisition

When the user provides a video URL or a URL text file, use `scripts/acquire_video_source.py` to download or probe video, subtitles, cover, and metadata into the standard workflow layout. Read `references/source-acquisition.md` first.

Examples:

```powershell
python C:\Users\david\.codex\skills\bilibili-render-pdf\scripts\acquire_video_source.py `
  C:\path\to\视频地址.txt `
  --output-dir C:\path\to\output `
  --dry-run
```

```powershell
python C:\Users\david\.codex\skills\bilibili-render-pdf\scripts\acquire_video_source.py `
  "https://www.bilibili.com/video/BVxxxx?p=2" `
  --output-dir C:\path\to\output `
  --cookies-from-browser chrome
```

Prefer this subtitle order:

1. platform manual subtitles
2. platform auto subtitles
3. Whisper transcription
4. visual-only mode when audio/subtitles are unavailable

Preserve timestamps. Do not flatten subtitles into plain text before visual localization is complete.

Download or locate the highest usable video source for frame extraction. For Bilibili 1080P+ sources, cookies may be required; tell the user when login-gated quality blocks a higher-resolution download.

Do not use danmaku as teaching content.

## Mandatory Workflow

### Phase 0: Acquire And Normalize Source

When the input is a URL, URL list, or BV/link rather than an already prepared local video/transcript pair:

- parse and deduplicate URLs by video identity and part
- preserve Bilibili `p=N` part selection
- download or probe metadata, cover, highest usable video, and platform subtitles
- convert selected subtitles to timestamped SRT and a readable timestamped transcript view
- write `acquisition_manifest.json`
- mirror a single ready item to `source/` and `srt/`
- stop for ASR/transcript repair if platform subtitles are missing

Do not start knowledge extraction from a URL until the source acquisition hand-off gate in `references/source-acquisition.md` passes.

### Phase 1: Knowledge Points First

Before selecting frames, create `knowledge_points.json` from the timestamped transcript.

Each knowledge point must include clear Chinese teaching prose plus structured fields:

- concept title in Chinese
- original English term and abbreviation when present
- plain-language explanation
- professional explanation
- transcript evidence with timestamps
- why this matters in the lecture
- common misunderstanding
- whether visual evidence is needed
- precise visual question to answer if visual evidence is needed
- manual-correction flags for unclear ASR, uncertain numbers, or ambiguous claims

The explanation must be easy to understand. Do not write stiff summaries or only list headings. If a term such as POC, VAH, VAL, risk-free, range chart, drawdown, stop loss, absorption, squeeze, DCF, ROE, duration, gamma, or CPI appears, define it before using it as a teaching building block.

### Phase 2: Keyframe Segment Set

Create `keyframe_segments.json` after `knowledge_points.json`.

Each segment must start from a knowledge point and a visual question. Do not pick arbitrary chapter-level timestamps.

For each visual question:

- identify the narrow subtitle-aligned time interval
- add a small boundary margin only when necessary
- extract dense candidate frames at 0.5-second intervals by default
- create a contact sheet or tiled strip for recall
- inspect enough candidates to avoid missing the fully revealed or most readable state

For micro-movement or dashboard-state changes, optionally create a 1-2 second micro clip, but still record which frame(s) enter the final document.

### Phase 3: Frame Interpretation And Analysis

Before a frame enters the PDF, create or update:

- `frame_selection_record.md`
- `frame_interpretations.md`
- `visual_evidence_analysis.md`

Every selected frame must answer:

- what is actually visible in the image
- which transcript line it connects to
- which knowledge point it supports
- what can be inferred from text plus image
- what cannot be proven from this frame
- whether the frame needs crop/zoom
- what exact sub-region answers the visual question
- whether the main PDF should use a focus crop, AI-rewritten keyframe, or full source screenshot
- confidence level and reason

Do not infer visual meaning only from filenames, subtitles, nearby narration, or OCR. Use direct visual inspection. OCR may assist reading tiny text, but cannot replace visual judgment.

After selecting a frame, create `visual_focus_crops.json` for every frame that is not already tightly focused. The crop must isolate the relevant price area, order panel, stop line, value area, POC, caption, or dashboard state. Do not let a wide platform screenshot enter the main body when only a small region carries the evidence.

Before final PDF insertion, create `visual_rewrite_prompts.json` and decide whether the selected frame needs AI rewriting. For cluttered trading interfaces, the default is:

- keep the raw selected frame in `figures/` for audit
- create a focused crop in `crops/`
- create an AI-rewritten teaching visual in `rewritten_keyframes/final/`
- insert the rewritten visual in the main body
- move full raw screenshots and contact sheets to a visual evidence appendix

Only insert a full raw screenshot in the main body when the entire interface context is necessary for understanding.

### Phase 4: AI Teaching Diagrams

If screenshots are too cluttered, too platform-specific, or do not clearly teach the mechanism, design a teaching diagram.

Before generating the diagram asset, create `diagram_prompts.json`. Do not generate a diagram first and invent a prompt afterward. Each prompt must specify:

- knowledge point ID
- source frame(s) and transcript timestamps
- teaching objective
- required visual elements
- logical relationships and arrows
- labels
- color semantics
- what must not be implied
- preferred output format
- why a screenshot, crop, or rewritten keyframe is still insufficient

Choose a diagram generation mode deliberately:

1. `codex_image_plus_svg_labels`: default for polished course-note diagrams when Codex image generation is available or when the user asks for better-looking diagrams. Prefer the in-session Codex image capability for a clean, mostly text-free conceptual background; then use Codex-authored SVG labels, arrows, legends, and callouts for exact Chinese text and logic.
2. `image_model_plus_svg_labels`: optional local/API batch mode for reproducible image generation, only when the user explicitly approves or asks for API mode.
3. `codex_svg`: preferred fallback when image generation is unavailable, when exact editability matters most, or when the diagram is simple enough to draw cleanly as SVG.
4. `codex_tikz`: use only for formulas, simple geometric mechanisms, or when LaTeX-native rendering is explicitly preferred. Do not use TikZ as the default for polished teaching visuals.
5. `deterministic_plot`: use only for true data/geometry charts where Python or another deterministic renderer is the correct source of the visual.

Do not ask Codex image generation or any image model to render dense Chinese labels, small formulas, exact price levels, or source citations directly inside the bitmap. The image model may create layout, background objects, simplified chart shapes, and visual style. Codex must own the exact text layer.

For `codex_image_plus_svg_labels` or approved `image_model_plus_svg_labels`, create and record all layers:

- `diagrams/backgrounds/`: image-model background PNG/WebP, with no important text
- `diagrams/overlays/`: Codex-authored SVG overlay containing exact Chinese labels, arrows, legends, and evidence notes
- `diagrams/final/`: final composited PNG/PDF/SVG asset inserted into the LaTeX/PDF

Every generated teaching diagram must be reviewed for visual quality, label accuracy, and unsupported implications before insertion. If a diagram looks ugly, cramped, generic, or contains malformed text, revise or reject it rather than inserting it. A rough SVG that merely proves the logic is not acceptable as a polished teaching diagram when image generation is available.

Use Python only for mechanical rendering, validation, cropping, compositing, or conversion; do not let Python be the source of the teaching idea unless the user asks for a deterministic plot.

If Codex image generation or another image-generation model is used, record the prompt and generated asset path in `diagram_prompts.json` and `run_manifest.json`. If local API mode is used, also record that the user approved it.

### Phase 5: Pedagogical Writing Plan

Before writing the final document body, create:

- `source_coverage_report.json`
- `source_coverage_report.md`
- `writing_plan.json`
- `writing_review.md`

The writing plan must transform verified material into a teaching narrative. For trading videos, default to a zero-foundation textbook standard: do not compress the source into a polished short summary, and do not assume the reader knows trading vocabulary.

The writing plan fields are quality checks, not a visible chapter template. Build a book arc first, then choose chapter shapes that fit the source material. The final PDF must not simply repeat the same headings for every chapter.

Do not create a beautiful but hollow document. The standard is whether a novice can understand every concept, judgment, trading action, and risk boundary.

Each important transcript segment must be audited before writing:

- original time range
- main content
- key concepts
- key numbers
- trading actions
- whether it enters the textbook
- where it enters
- whether it is compressed
- whether it needs expansion, screenshots, teaching diagrams, or manual review

Each major section should make clear, either in prose, case narration, captions, sidebars, or exercises:

- why the topic matters
- what learner problem or confusion it solves
- why a simpler view is insufficient when applicable
- the core idea in plain Chinese
- the mechanism, causal chain, formula, or decision process
- the transcript, frame, crop, diagram, formula, code, or metadata evidence
- what the evidence does not prove
- the takeaway for the learner

For novice trading textbooks, each chapter must satisfy learning goals, prerequisite concepts, source scene, timestamped source evidence, novice explanation, mechanism breakdown, case replay when relevant, image explanation when relevant, common misconceptions, risks and boundaries, chapter summary, and review questions with answers. These are required content checks, not required visible headings. Render them differently according to the chapter's teaching purpose.

Use variable chapter archetypes such as problem opener, concept tool, mechanism lab, trade case, post-mortem, risk memo, statistics interlude, psychology chapter, and synthesis. No more than two adjacent chapters may share the same visible heading sequence.

If one planned chapter contains more than three new novice-level trading terms, split it into smaller chapters unless those terms are only briefly listed in a prerequisite section.

For finance/trading content, distinguish fact, inference, speaker viewpoint, and investment-advice tendency. State assumptions, market conditions, and execution risks when relevant.

### Phase 6: Final LaTeX/PDF

Start from `assets/notes-template.tex`.

The final PDF must:

- be written in Chinese unless the user requests another language
- read like a teacher explaining the material, not like a raw transcript summary
- for trading videos, read like a zero-foundation textbook that expands compressed trader language into explicit reasoning chains
- follow `writing_plan.json`; reconstruct the teaching flow when needed instead of blindly mirroring subtitle order
- introduce each major section with a real learner problem or narrative hook before moving into concepts, mechanisms, evidence, boundary/risk, and takeaway when applicable
- vary the visible chapter layout according to the material; planning metadata must not appear as a repeated fill-in-the-blank form
- include transitions that explain why one chapter follows from the previous one
- define specialist terms before relying on them
- define every first-use trading term with what it is, a plain-language explanation, why it matters, the source scene, common misunderstanding, misuse boundary, and related concepts
- explain intuition before formalism, formulas, or trading jargon
- preserve key source details such as account constraints, daily drawdown, existing profit, risk amount, position management, partial exits, reasons for not trading, and statistical claims; do not collapse them into generic claims
- include raw screenshots only when they materially support the surrounding explanation and cannot be replaced by a clearer crop or AI-rewritten visual
- prefer AI-rewritten keyframe visuals in the main body when the original screenshot is cluttered, platform-specific, or visually noisy
- keep full raw screenshots and contact sheets in the visual evidence appendix by default
- introduce every figure before insertion and interpret its support boundary after insertion when needed
- include crops when the original frame is too loose
- include AI-designed teaching diagrams when they improve understanding
- prefer polished `codex_image_plus_svg_labels` diagrams when Codex image generation is available; use `codex_svg` as a transparent fallback; use local/API `image_model_plus_svg_labels` only with explicit user approval
- keep all images outside `knowledgebox`, `importantbox`, and `warningbox`
- use `importantbox`, `knowledgebox`, and `warningbox` only for high-signal teaching payloads
- place source-time footnotes on the same page for every video frame or crop
- end each major part or substantial chapter with a compact synthesis, but do not force the same final subsection title everywhere when it makes the document feel mechanical
- end with a final synthesis section covering the speaker's substantive closing discussion, distilled claims, cross-section links, practical implications, limits, and open questions when supported
- compile successfully with XeLaTeX

Do not emit `[cite]` placeholders.

### Phase 7: Independent QA Gate

Do not let the same generation pass self-approve the output.

Before any output may be called `final`, `pass`, or `quality_gate_passed=true`, run an independent QA pass following `references/quality-review-agent.md`.

The QA pass must inspect files on disk. Do not treat a generated `quality_report.json` as proof by itself. The reviewer must compare the report with `notes.tex`, rendered preview pages, Markdown output when present, asset folders, and cleanup state.

The QA pass must specifically check:

- whether the run reused or renamed any old invalid output directory
- whether every main-body raw screenshot either has an AI-rewritten replacement or a written exception explaining why the raw screenshot itself is necessary
- whether `visual_rewrite_prompts.json` covers every selected visual that enters the main body
- whether teaching diagrams were actually generated with the recorded mode
- whether `codex_image_plus_svg_labels` means a real Codex/image-generated bitmap background plus Codex-controlled label overlay, not a Python/PIL/SVG substitute
- whether `codex_svg`, TikZ, deterministic plots, or local mechanical rendering were honestly marked as fallback/draft when the user asked for image-model visuals
- whether `run_manifest.json` and `quality_report.json` contradict the PDF or asset folders
- whether old fallback wording or code markers remain, such as `PIL-only`, `Python/PIL only`, `local PIL rendered`, `def create_rewrite`, or obsolete visual output paths
- whether unused dense candidate frames were removed unless debug/audit retention was explicitly requested
- whether final Markdown/PDF includes the requested synthesis, knowledge-card, review-template, and manual-correction sections when those are part of the workflow

If the QA pass finds any blocking issue, set:

- `output_status: draft_needs_review`
- `quality_gate_passed: false`
- `quality_report.status: needs_review`

Do not compile or present a PDF as final when the visual rewrite or image-generation requirements are only partially satisfied.

## Long Video Strategy

For videos longer than 20 minutes, or transcripts with more than 300 entries:

- split by semantic teaching boundaries when possible
- otherwise split by subtitle ranges with a small overlap
- when the user explicitly allows multiple agents, parallelize segment analysis
- integrate segment outputs into one coherent document, not a concatenation

The main agent is responsible for global consistency: terminology, section order, figure numbering, diagram style, and final synthesis.

## Cleanup Rules

After the final PDF determines which frames are used:

- keep final figures in `figures/`
- keep crops in `crops/`
- keep AI-rewritten keyframe visuals in `rewritten_keyframes/final/`
- keep visual rewrite prompts and overlays for audit
- keep generated teaching diagrams in `diagrams/`
- keep contact sheets only when they are useful for audit, or when the user asks for audit artifacts
- delete unused raw candidate frames by default
- preserve counts and deleted paths in `run_manifest.json`

Only keep unused candidate frames when the user asks for debug mode or audit mode.

## Required Delivery

Deliver:

- final `.tex`
- compiled `.pdf`
- cover image or preview-frame cover
- `knowledge_points.json`
- `keyframe_segments.json`
- `frame_selection_record.md`
- `frame_interpretations.md`
- `visual_evidence_analysis.md`
- `diagram_prompts.json`
- `diagram_review.md`
- `source_coverage_report.json`
- `source_coverage_report.md`
- `writing_plan.json`
- `writing_review.md`
- review questions with answers, either embedded in the final document or delivered as `review_questions_with_answers.md`
- novice comprehension review, either embedded in `writing_review.md` or delivered as `novice_comprehension_review.md`
- generated figures/crops/diagrams referenced by the document
- `visual_focus_crops.json` and `visual_rewrite_prompts.json` when selected frames need focus or rewrite
- AI-rewritten keyframe visuals in `rewritten_keyframes/final/` when raw screenshots are too cluttered for the main body
- if `codex_image_plus_svg_labels` or approved `image_model_plus_svg_labels` is used: generated backgrounds, Codex label overlays, and composited final diagram assets
- `run_manifest.json`
- final checklist

If any required phase is skipped, state why and mark the output as draft rather than final.

## Final Checklist

Before final delivery, verify:

- knowledge points were extracted before frame selection
- specialist terms have Chinese explanations, English terms, and abbreviations when available
- every selected frame links to a knowledge point and subtitle evidence
- selected frames were visually inspected
- crops were added when full frames were too loose
- `visual_focus_crops.json` records the exact region and rationale for every focus crop
- `visual_rewrite_prompts.json` exists before AI-rewritten keyframe assets are generated
- main-body visuals prefer AI-rewritten keyframes or focus crops over full raw screenshots unless full context is necessary
- diagram prompts were created before teaching diagrams
- final teaching diagrams match their prompts and do not imply unsupported claims
- `diagram_review.md` records the mode, source evidence, visual-quality decision, and label-accuracy decision for every teaching diagram
- generated diagram backgrounds, when used, have exact Chinese labels added by Codex-controlled SVG/LaTeX text rather than baked into the bitmap
- final teaching diagrams pass a visual quality check: readable labels, balanced spacing, consistent style, and no clutter
- `source_coverage_report.json` and `.md` audit all important transcript segments before final writing
- `writing_plan.json` exists before final writing and converts verified material into a teaching flow rather than raw subtitle order
- `writing_review.md` confirms source coverage, novice readability, motivation, mechanism, evidence/example, boundary/risk, chapter summaries, and review answers
- every chapter with trading content has novice-oriented prerequisite concepts, source scene, timestamped source evidence, mechanism breakdown, common misconceptions, and risk boundaries
- trading cases include market background, observation, judgment basis, entry/cancel decision, stop, risk amount when available, position management, exit, result, and what novices must not copy
- formulas, code, figures, boxes, and final synthesis follow `references/pedagogical-writing.md`
- unused candidate frames were removed unless debug/audit mode is requested
- source-time footnotes are present for every frame/crop in the PDF
- XeLaTeX compilation succeeds
- final text artifacts contain no mojibake or replacement-character corruption
- independent QA passed and did not find raw-screenshot, fake-image-generation, or self-approval issues
- QA checked actual asset counts, final image references, cleanup state, old fallback markers, and status/report consistency
