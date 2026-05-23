# Visual Analysis Rules

This reference covers keyframe segments, frame selection, interpretation, evidence fusion, and cleanup.

## Output: `keyframe_segments.json`

Each segment must originate from a knowledge point:

```json
[
  {
    "id": "SEG001",
    "knowledge_point_id": "KP001",
    "visual_question": "",
    "subtitle_time_range": "00:00:00--00:00:00",
    "extraction_range": "00:00:00--00:00:00",
    "candidate_interval_seconds": 0.5,
    "candidate_frames": [],
    "contact_sheet": "",
    "micro_clip": "",
    "selected_frames": [],
    "focus_crops": [],
    "rewritten_keyframes": [],
    "selection_status": "pending | selected | rejected | needs_more_sampling"
  }
]
```

## Dense Candidate Set

Default extraction interval is 0.5 seconds.

Use a narrow subtitle-aligned range. Add margin only when needed:

- use the exact subtitle range when the visual is stable
- add 1-2 seconds before/after if the visual reveal lags narration
- use a 1-2 second micro clip when motion or dashboard updates matter

Do not start from a guessed timestamp and one screenshot.

## Frame Selection Record

`frame_selection_record.md` must include:

- knowledge point ID
- visual question
- subtitle evidence
- extraction range
- contact sheet path
- every candidate frame or grouped near-identical frames
- chosen/rejected decision
- reason
- final figure path
- crop path if used
- rewritten keyframe path if used in the main body
- whether the raw frame is main-body material or appendix-only evidence

If there are many visually identical candidates, grouped rejection is allowed only when the group range is explicit, for example:

```text
00:04:43.0--00:04:46.5 rejected: same chart state, but subtitle has not reached the value-area reaction explanation.
```

## Output: `frame_interpretations.md`

Use one section per selected frame:

```markdown
## FIG001

- Knowledge point: KP001
- Source frame: figures/fig001.jpg
- Source time: 00:04:43--00:04:51
- Visual facts:
  - ...
- Transcript evidence:
  - ...
- Supports:
  - ...
- Reasonable inference:
  - ...
- Cannot prove:
  - ...
- Needs crop/zoom: yes/no
- Focus target: the exact region that answers the visual question
- Main-body asset decision: raw frame | focus crop | rewritten keyframe | teaching diagram
- Needs teaching diagram: yes/no
- Needs AI keyframe rewrite: yes/no
- Confidence: high/medium/low
- Manual review notes:
  - ...
```

## Fact vs Inference

Keep three layers separate:

1. visual fact: what is visibly present
2. transcript evidence: what the speaker says
3. analysis/inference: what can be concluded by combining them

Example:

- Visual fact: A red stop line is visible below current price.
- Transcript evidence: The speaker says the position is risk free.
- Inference: The speaker likely moved risk down after price advanced.
- Cannot prove: Exact realized PnL after fees/slippage.

## Output: `visual_evidence_analysis.md`

This file fuses knowledge points and frames.

For each knowledge point with visuals:

- restate the knowledge point
- list selected frames
- explain why the frames are sufficient or insufficient
- identify missing visual evidence
- state what the final note can safely say
- state what must remain a caution or manual-review point

## Focus Crop Gate

After a frame is selected, decide whether the selected frame is visually tight enough.

Create `visual_focus_crops.json` when any selected frame contains irrelevant platform UI, speaker windows, captions, menus, or large empty chart areas that distract from the visual question.

The crop must isolate the teaching target:

- price area around VAL/VAH/POC
- stop line or order marker
- order panel or position widget
- relevant subtitle/caption when the caption itself is evidence
- specific dashboard value or setting
- region showing a squeeze, absorption, rejection, or no-trade context

Do not use a crop merely as decoration. The crop must answer the visual question more clearly than the full frame.

## AI Keyframe Rewrite Gate

Before final PDF insertion, decide whether the selected visual should be rewritten.

Use `visual_rewrite_prompts.json` and `rewritten_keyframes/` when:

- the screenshot is too cluttered for a novice
- the relevant evidence occupies only a small portion of the frame
- platform branding, menus, or speaker windows distract from the concept
- the concept is better taught by simplified geometry, arrows, zones, or before/after states
- the original screenshot is useful as evidence but poor as a teaching image

Default policy for trading-screen screenshots:

1. keep the raw selected frame in `figures/` for audit
2. create a focus crop in `crops/`
3. create an AI-rewritten teaching visual in `rewritten_keyframes/final/`
4. insert the rewritten visual in the main teaching body
5. place raw screenshots and contact sheets in a visual evidence appendix

Only use the full raw screenshot in the main body if the entire interface context is necessary for the explanation.

## Cleanup Rules

After final frame selection:

- copy selected full frames into `figures/`
- copy crops into `crops/`
- keep AI-rewritten keyframes in `rewritten_keyframes/final/`
- keep diagrams in `diagrams/`
- optionally keep contact sheets for audit
- delete unused raw candidate frames unless debug/audit retention is requested

`run_manifest.json` must record:

- candidate count before cleanup
- selected frame count
- deleted candidate count
- whether contact sheets were retained
- whether debug retention was requested

Do not delete final figures, crops, diagrams, source video, transcript, SRT, manifest, or audit records.
