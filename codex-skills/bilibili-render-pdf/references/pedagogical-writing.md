# Pedagogical Writing Rules

Use this reference after knowledge extraction, frame interpretation, evidence fusion, and diagram review. The goal is to turn verified material into a coherent Chinese teaching note or textbook, not a chronological subtitle digest.

If the draft reads like repeated form fields instead of a real textbook, also read `textbook-writing-benchmarks.md`. Planning metadata is allowed to be structured; the visible chapter prose must not look like a checklist.

For finance/trading videos, the default writing target is stricter:

> Turn the transcript into a zero-foundation textbook that a novice can study independently.

Do not produce a document that only looks professional. The success criterion is whether a reader who does not know order flow can understand each concept, each trading judgment, each action, and each risk boundary.

Do not compress important trading details into generic claims such as "risk management is important" or "the speaker used order flow." Expand compressed trader language into explicit reasoning chains.

## Required Output: `source_coverage_report.json` And `.md`

Before `writing_plan.json`, create a source coverage report.

Audit by semantic segment or time range:

```json
[
  {
    "segment_id": "SRC001",
    "time_range": "00:00:00--00:03:00",
    "source_line_ids": [],
    "main_content": "",
    "key_concepts": [],
    "key_numbers": [],
    "trading_actions": [],
    "enters_textbook": true,
    "target_chapter_or_section": "",
    "compression_level": "none | light | medium | heavy",
    "needs_expansion": true,
    "needs_screenshot": false,
    "needs_teaching_diagram": false,
    "needs_manual_review": false,
    "reason_if_omitted": ""
  }
]
```

Do not silently omit important source material. If a segment is excluded, state why. Repeated greetings or platform logistics may be excluded; account constraints, risk limits, trade decisions, statistics, tool limitations, psychological rules, and warnings should not be dropped.

## Required Output: `writing_plan.json`

Create `writing_plan.json` before writing `notes.tex` or `integrated_knowledge_document.draft.md`.

The writing plan is a private design artifact. It should be more structured than the final chapter, because it needs to prove that source coverage, definitions, visual evidence, risk boundaries, and exercises have been considered. Do not convert every plan field into a visible heading.

Use this structure:

```json
{
  "document_language": "zh-CN",
  "audience_level": "入门 | 进阶 | 专业 | 高级",
  "global_teaching_goal": "",
  "global_thesis": "",
  "book_arc": {
    "central_problem": "",
    "reader_starting_point": "",
    "concept_progression": [],
    "case_progression": [],
    "risk_progression": [],
    "final_learning_destination": ""
  },
  "concept_threads": [
    {
      "concept": "",
      "first_introduced": "",
      "revisited_in": [],
      "progression": ""
    }
  ],
  "source_scope": [
    {
      "chapter_id": "",
      "time_range": "",
      "line_ids": []
    }
  ],
  "non_teaching_content_removed": [],
  "terms_to_define_before_use": [],
  "sections": [
    {
      "section_id": "SEC001",
      "title_zh": "",
      "source_chapters": [],
      "source_line_ids": [],
      "textbook_chapter_type": "problem_opener | concept_tool | mechanism_lab | trade_case | post_mortem | risk_memo | statistics_interlude | psychology_chapter | synthesis",
      "visible_structure_strategy": "narrative | case_walkthrough | worked_example | dialogue | figure_driven | memo | synthesis_essay",
      "bridge_from_previous_section": "",
      "bridge_to_next_section": "",
      "teaching_goal": "",
      "learner_question": "",
      "motivation": "",
      "problem_context": "",
      "why_simple_view_is_insufficient": "",
      "prerequisite_concepts": [],
      "core_idea": "",
      "three_layer_explanation": {
        "plain_human_language": "",
        "source_scene": "",
        "professional_understanding": ""
      },
      "mechanism_steps": [],
      "trade_case_replay": {
        "trade_time": "",
        "market_background": "",
        "speaker_observation": "",
        "original_plan": "",
        "cancelled_plan_and_reason": "",
        "entry_conditions": "",
        "why_not_full_size": "",
        "stop_location": "",
        "risk_amount": "",
        "target": "",
        "stop_move": "",
        "partial_exit": "",
        "exit_reason": "",
        "risk_if_held": "",
        "novice_lesson": "",
        "what_not_to_copy": ""
      },
      "examples_or_evidence": [
        {
          "type": "transcript | source_frame | crop | teaching_diagram | formula | code | metadata",
          "id": "",
          "time_range": "",
          "how_it_supports_the_section": "",
          "support_boundary": ""
        }
      ],
      "key_terms_defined_before_use": [],
      "subsection_plan": [],
      "teaching_boxes": [
        {
          "box_type": "importantbox | knowledgebox | warningbox",
          "title_zh": "",
          "payload": ""
        }
      ],
      "figures_to_insert": [],
      "common_misunderstandings": [],
      "risk_boundaries": [],
      "review_questions_with_answers": [],
      "manual_review_notes": [],
      "takeaway": ""
    }
  ],
  "final_synthesis_plan": {
    "speaker_substantive_closing": "",
    "distilled_core_claims": [],
    "cross_section_links": [],
    "practical_implications": [],
    "limits_and_risks": [],
    "open_questions_or_next_steps": []
  }
}
```

## Source Inputs For Writing

Build the writing plan from all available verified sources:

- video title, chapter structure, part metadata, cover image, and duration;
- timestamped transcript lines and speaker emphasis;
- `semantic_chapter_plan.json`, `knowledge_points.json`, and `knowledge_blocks.json` when present;
- `frame_interpretations.md` and `visual_evidence_analysis.md`;
- selected screenshots, crops, micro-clip observations, and support grades;
- `diagram_prompts.json` and `diagram_review.md`;
- formulas, tables, code snippets, dashboards, or charts visible in the source;
- the speaker's substantive closing discussion when it teaches synthesis, limitations, tradeoffs, advice, or open questions.

For trading videos, preserve these details unless truly absent:

- account constraints and account size;
- existing daily profit and profit cushion;
- maximum daily drawdown;
- risk amount per trade;
- floating profit changes;
- stop-loss placement and stop movement;
- partial exits and reasons for exiting;
- reasons for not continuing or not trading;
- why order flow is a tool, not magic;
- why large-account results cannot be copied by small accounts;
- average win, average loss, win rate, profit factor, edge, or other statistical claims;
- why not holding a full move can be a statistical choice rather than fear;
- why real money changes psychology and execution.

Skip non-teaching material unless the user asks otherwise:

- greetings and routine sign-offs;
- sponsorship or channel logistics;
- Bilibili engagement talk such as "一键三连", "关注", "投币";
- repeated filler that does not alter the explanation.

## Narrative Standard

Every major section should read like a good teacher guiding the learner.

Prefer this sequence when applicable, but treat it as a reasoning path, not a repeated visible heading template:

1. Motivation: why this matters.
2. Problem/context: what question the learner is facing.
3. Why the simple view is insufficient.
4. Core idea in plain Chinese.
5. Mechanism: step-by-step logic, causal chain, formula, or decision process.
6. Evidence/example: transcript evidence, screenshot, crop, diagram, formula, code, or case.
7. Boundary/risk: what the evidence does not prove, common misuse, or investment/trading caveat.
8. Takeaway: what the learner should retain.

Do not dump subtitles in chronological order. Reconstruct the teaching flow when it improves understanding. Preserve provenance by keeping source line ids and timestamps in the plan.

For live trading or step-by-step demonstrations, time order may be the teaching structure. Even then, each section must explain the decision logic, not merely list what happened next.

The visible PDF should have a book arc. The reader should feel that each chapter exists because the previous chapter created a new question. Use transitions such as:

- "现在我们知道账户约束是什么，下一步才有资格讨论入场。"
- "位置给了观察理由，但还没有给交易理由；这就是订单流出现的位置。"
- "第一次交易看似成功，复盘章要追问：成功里哪些是技术，哪些只是行情配合？"
- "统计数据不是装饰，它解释为什么交易员不一定要吃完整段行情。"

Do not use the same visible heading sequence in more than two adjacent chapters. If the draft does this, rewrite the chapters into different archetypes.

## Novice Textbook Chapter Standard

For a zero-foundation trading textbook, do not write chapters as broad summaries and do not expose a rigid checklist as the chapter layout. Each chapter must satisfy these content checks, but the final prose may express them through narrative paragraphs, worked examples, figure interpretation, sidebars, short exercises, or part-level review sections:

- `本章学习目标`: what the reader should understand after the chapter;
- `本章先备知识`: prerequisite terms, explained in plain Chinese;
- `原视频场景`: time range, what the speaker was doing, and what market state existed;
- `关键原文与时间戳`: short quotes or faithful paraphrases with timestamps;
- `新手版解释`: teacher-like explanation, starting from intuition;
- `机制拆解`: the causal chain or decision chain;
- `交易案例复盘`: required when a concrete trade, cancellation, stop move, partial exit, or no-trade decision appears;
- `图像与截图解释`: required when visual evidence matters;
- `新手常见误解`: list and correct likely misunderstandings;
- `风险与边界`: how the idea can be misused;
- `本章小结`: 8-12 concrete points for substantial chapters;
- `复习题与标准答案`: at least 8 questions for substantial chapters.

If one chapter introduces more than three new novice-level trading terms, split the chapter or move the terms into a prerequisite chapter.

Choose a chapter archetype before writing:

- `problem_opener`: begin with a practical learner confusion and use the source to show why the confusion matters.
- `concept_tool`: teach one tool deeply, then show where it appears in the video.
- `mechanism_lab`: build a causal or decision chain step by step.
- `trade_case`: narrate a concrete trade chronologically, pausing only at decision points.
- `post_mortem`: start from the trade result and work backward to skill, luck, and risk.
- `risk_memo`: organize around constraints, drawdown, slippage, account size, or execution limits.
- `statistics_interlude`: turn performance claims into distribution, expectancy, variance, and sample-size language.
- `psychology_chapter`: connect real money, pressure, rule-breaking, and process design.
- `synthesis`: connect earlier ideas into a practice plan.

The archetype controls the visible structure. A `trade_case` chapter may read like a guided story; a `concept_tool` chapter may use definition, diagram, misuse boundary, and mini-exercise; a `risk_memo` may use a compact memo style. They should not all share the same headings.

For long videos, prefer multiple volumes over forced compression:

- Volume 1: prerequisite concepts;
- Volume 2: front-half live trading case breakdown;
- Volume 3: back-half method, psychology, statistics, and professionalization;
- Volume 4: knowledge cards, case replays, review questions and answers;
- Volume 5: visual evidence, teaching diagrams, and quality reports.

## Explanation Style

Write in Chinese unless the user requests another language.

Use clear teaching prose:

- explain intuition before formal terms;
- define specialist terms before relying on them;
- keep technical depth, but introduce formalism only after the learner understands the problem;
- break dense content into smaller subsections that build progressively;
- make transitions explicit: why this idea appears now, what it solves, and how it connects to the next idea.
- use the three-layer explanation pattern for complex concepts:
  1. one plain-language sentence;
  2. the concrete source scene;
  3. the professional definition, conditions, risks, and boundaries.

Avoid:

- repeated stiff openings such as "本段主要介绍";
- thin bullet lists that do not explain logic;
- attractive but hollow writing that has headings, figures, and boxes but does not teach the reasoning;
- repeating the same visible heading set across chapters just because those fields exist in `writing_plan.json`;
- turning `learning_goal`, `source_scene`, `evidence`, `misconceptions`, and `review_questions` into a form that every chapter visibly fills out in the same order;
- one-sentence definitions for difficult concepts such as absorption, squeeze, risk-free position, edge, profit factor, or drawdown;
- unsupported claims from nearby subtitles;
- decorative figures or boxes that do not teach;
- language that turns speaker opinion into fact or investment advice.

## Anti-Template Rewrite Pass

Before final PDF generation, run an anti-template pass:

1. List the visible headings of every chapter.
2. If more than two adjacent chapters share the same heading sequence, rewrite at least one chapter using a different archetype.
3. Check whether the chapter begins with a live learner problem, not administrative metadata.
4. Check whether the chapter has a bridge from the previous chapter and a reason the next chapter follows.
5. Move repeated review questions, source evidence, or prerequisite lists to part-level sections when they interrupt the teaching flow.
6. Keep the audit fields in `writing_plan.json`; do not delete rigor, but hide the scaffolding from the reader.

A draft fails this pass if it feels like "本章学习目标 / 原文证据 / 知识点 / 交易流程 / 视觉证据 / 误区 / 复习题" copied twelve times.

### Bad vs Good Detail Level

Bad:

> Fabio 在 Value Area Low 附近看到卖方被吸收，于是建立多头仓位，并很快把仓位变成 risk-free。

Good:

> Fabio 的第一笔多头不是因为“价格到了低位所以买入”。他先用 Value Area Low 找到一个值得观察的低位区，但这个区域本身不是买入信号。随后他观察卖方是否能继续把价格打下去。如果卖方主动进攻后价格仍不能有效延伸，说明下方可能有被动买盘承接，也就是 absorption 的假设开始出现。这个时候，他仍然不是一次性满仓，而是先用较小风险测试市场反馈；如果关键区域被打穿，做多假设就失效。

## Finance And Trading Writing Rules

When the source is finance/trading content:

- distinguish fact, inference, speaker viewpoint, and investment-advice tendency;
- explain abbreviations and English terms on first use;
- do not assume the reader knows futures, Nasdaq/NQ, scalping, order flow, volume profile, value area, VAL, VAH, POC, range chart, absorption, aggressive buyers/sellers, squeeze, liquidation, risk-free position, stop loss, trailing stop, drawdown, profit factor, edge, risk reward, win rate, slippage, CFD, 0DTE options, market maker, contraction day, or momentum day;
- for each first-use term, explain what it is, a plain-language interpretation, why traders watch it, where it appears in the source, common misunderstanding, what it cannot prove, and related terms;
- state assumptions and market conditions for every strategy or setup;
- mark model boundaries, execution risk, liquidity risk, slippage, and data uncertainty when relevant;
- never imply guaranteed profit, literal risk-free trading, or certainty when the source only supports a conditional setup.

Important mechanisms that must be expanded when present:

- account constraints and maximum daily drawdown;
- why a million-dollar account and a small account cannot be compared by nominal PnL;
- why order flow is not magic and a tool is not edge;
- absorption as a full mechanism: active attack, expected price extension, failure to extend, possible passive absorption, invalidation if the key area breaks;
- risk-free position as stop-management language, not literal absence of risk;
- why not holding the full move can reflect a statistical distribution choice;
- why being directionally right is not the same as making money.

When discussing a trade, use the full case chain:

market background -> speaker observation -> judgment basis -> entry or cancelled plan -> stop -> risk amount when available -> position management -> partial exit or final exit -> result -> novice lesson -> what not to copy.

## Figures, Diagrams, Formulas, And Code

Before inserting any figure, write a sentence explaining what the reader should look for. After the figure, write what it proves, what it only partially supports, and what remains uncertain when applicable.

For every screenshot-dependent chapter, separate:

- what the original screenshot directly shows;
- what the speaker says about it;
- what the agent infers;
- what the image supports;
- what the image cannot prove;
- whether a teaching diagram is needed and what it should show.

Captions must describe the visible teaching content, not just the file name or broad topic.

For formulas:

- first explain in plain Chinese what the formula expresses and why it appears;
- then show the formula;
- then explain every symbol in a flat list.

For code:

- explain what the code is supposed to do before the listing;
- include a descriptive caption;
- summarize the expected behavior after the listing when useful.

Use boxes deliberately:

- `importantbox`: definitions, central claims, core mechanism summaries, theorem-like statements, and must-remember takeaways.
- `knowledgebox`: background, side knowledge, prerequisites, terminology comparisons, and intuition-building analogies.
- `warningbox`: common misunderstandings, hidden assumptions, failure modes, misleading heuristics, execution risk, and causal confusion.

There is no quota for boxes. Use them only when they carry a distinct teaching payload. Keep images outside all boxes.

## Final Synthesis

End the document with a final synthesis section.

It should include:

- the speaker's substantive closing discussion, excluding routine sign-off;
- a compact restatement of core claims and mechanisms;
- cross-links between sections;
- practical implications that stay faithful to the source;
- limits, risks, open questions, or next steps when supported.

## Knowledge Cards

For trading textbooks, every core concept needs a complete card. Use `knowledge_cards_expanded.json` when the final document would become too long.

Each card must include:

- concept name;
- English name and abbreviation;
- one-sentence definition;
- plain-language explanation;
- professional explanation;
- source timestamp;
- transcript evidence;
- source scene;
- why it matters;
- how to observe it on a chart or interface;
- correct usage;
- novice misunderstandings;
- risk boundary;
- related concepts;
- counterexample or invalidation case;
- review question;
- standard answer.

Do not make difficult cards one paragraph long. For example, absorption must explain who is attacking, what price should do if the attack works, why failure to extend can indicate passive absorption, how high volume can mislead, how absorption differs from ordinary chop, how the hypothesis fails, and how novices misread it.

## Review Questions

For each substantial textbook chapter, include at least 8 questions with answers:

- concept definition;
- mechanism understanding;
- source video case;
- risk judgment;
- novice misconception;
- application.

Do not provide questions without answers. Do not ask vague reflection questions unless they are paired with a concrete standard answer.

## Review Output: `writing_review.md`

Before final delivery, create `writing_review.md`.

Check:

- source coverage report exists and important source details were not silently omitted;
- the document follows a teaching flow rather than raw subtitle order;
- the document has a book arc with explicit transitions between parts or chapters;
- no more than two adjacent chapters share the same visible heading sequence;
- required planning fields are satisfied without being exposed as a repetitive fill-in form;
- every substantial chapter has learning goal, prerequisite concepts, source scene, timestamped evidence, novice explanation, mechanism breakdown, misconceptions, risk boundary, summary, and review answers;
- specialist terms are defined before use;
- first-use trading terms satisfy the full novice definition standard;
- trade cases include entry/cancel decision, stop, risk amount when available, position management, exit, result, novice lesson, and what not to copy;
- figures are introduced and interpreted in the surrounding prose;
- boxes contain high-signal teaching payloads;
- final synthesis includes speaker closing value when present;
- no important teaching content is dropped during condensation;
- no unsupported visual or investment claim is introduced.

If the review finds a failure, revise the text before marking the output final. Do not pass a final document that a novice still cannot follow.
