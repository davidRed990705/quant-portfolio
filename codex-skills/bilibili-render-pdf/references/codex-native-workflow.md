# Codex-Native Workflow

This skill is a Codex-native workflow, not a standalone local automation pipeline.

The purpose of the skill is to help Codex do the intellectual work better inside the Codex environment. Local scripts and external tools are allowed only as helpers for mechanical operations.

## Default Ownership

Codex owns the work that requires understanding, judgment, pedagogy, or visual reasoning:

- reading the transcript and deciding what matters;
- defining semantic chapters;
- extracting and explaining finance/trading knowledge points;
- deciding which transcript moments need video evidence;
- forming precise visual questions;
- choosing which candidate frames answer those questions;
- interpreting images as visual facts, transcript evidence, inference, and limits;
- deciding where a crop is needed and what the crop should isolate;
- designing visual rewrite prompts;
- generating or guiding AI teaching visuals through Codex capabilities;
- writing the Chinese teaching narrative;
- reviewing whether the output teaches rather than merely fills a template;
- deciding whether evidence is strong enough to enter the final document.

Mechanical tools own only deterministic file or media operations:

- locating files and metadata;
- normalizing timestamped transcripts into JSON/SRT;
- extracting frames or micro-clips with ffmpeg;
- building contact sheets;
- applying crop boxes that Codex has chosen;
- compositing image-model backgrounds with Codex-authored SVG labels;
- converting images and compiling LaTeX/PDF;
- deleting unused candidate frames and writing manifests.

If a script starts making semantic decisions, the workflow is drifting away from Codex-native mode.

## External API Policy

Do not assume the user wants a local API pipeline.

Default order for AI work:

1. Use Codex reasoning in the current conversation.
2. Use Codex platform capabilities available in the current session, such as image generation tools, when the user wants AI-generated visuals.
3. Use local scripts only for mechanical execution or reproducible file handling.
4. Use external APIs or local API-key based CLIs only when the user explicitly asks for that mode or approves it after being told why it is needed.

Missing `OPENAI_API_KEY` is not a blocker for Codex-native visual design. It only blocks optional local batch image generation through the OpenAI API.

## Ask Before Switching Mode

Ask or state the mode clearly before doing any of these:

- replacing Codex analysis with a script-generated analysis;
- using a local API-key based image generator;
- using an external model or web service;
- changing from interactive Codex image generation to batch API generation;
- treating a fallback SVG/PNG as if it were an AI image-model output;
- skipping visual interpretation because a script produced a plausible figure.

Use this wording in run notes when relevant:

```text
Mode: Codex-native. Codex handled understanding, visual interpretation, teaching-visual design, and writing. Scripts handled frame extraction, cropping, compositing, PDF compilation, and cleanup.
```

## Image Generation Policy

When a polished teaching visual is needed, prefer Codex's in-session image generation capability if available. The workflow is:

1. Codex interprets the source frame and transcript.
2. Codex writes the teaching objective and prompt.
3. Codex generates a clean bitmap visual through the available Codex image tool.
4. Codex creates exact Chinese labels, arrows, legends, and evidence notes as SVG overlays.
5. Mechanical tools only composite and convert assets for the PDF.

Use a local OpenAI API key only for optional reproducible batch generation, not as the default.

If Codex image generation cannot save a reusable local file in the current environment, state that limitation and choose one of:

- use Codex-authored SVG as a transparent fallback;
- produce the prompt and ask the user whether to run batch API mode;
- keep the crop as the main visual until image generation can be run.

## Quality Gate

A run is not Codex-native if:

- semantic chapters are created by fixed time windows without Codex review;
- visual questions come only from keyword triggers;
- frame selection is based only on timestamps or filenames;
- generated diagrams are created before prompts and evidence boundaries;
- final writing is assembled from repeated templates without Codex narrative judgment;
- local scripts produce teaching claims that Codex has not checked.

