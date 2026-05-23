# Textbook Writing Benchmarks

Use this reference when the output starts to feel like a filled template instead of a coherent teaching document.

The goal is not to imitate any textbook's wording. The goal is to borrow proven organization patterns from finance education and apply them to video-derived learning notes.

## Benchmarks Consulted

- OpenStax, *Principles of Finance*: chapters commonly begin from a "why this matters" problem, then move into concepts, examples, figures, and applications. It also separates basic finance areas and repeatedly returns to risk-return tradeoffs. Source: https://openstax.org/books/principles-finance/pages/preface and https://openstax.org/books/principles-finance/pages/8-why-it-matters
- CFA Institute refresher readings: readings state learning outcomes, then organize material around a process or analytical framework, with summaries that help learners verify what they can do after studying. Source: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-management-overview and https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-risk-return-part-1
- Aswath Damodaran, *Applied Corporate Finance*: the useful pattern is question-driven application. Finance theory is turned into tools for solving concrete business decisions rather than presented as isolated definitions. Source: https://www.wiley-vch.de/en/areas-interest/finance-economics-law/applied-corporate-finance-978-1-118-80893-1

## What To Copy As Structure

### 1. Start From A Learner Problem

Do not start every chapter with the same administrative block. Start with the question the learner is likely asking:

- "Why is a profitable trade still dangerous?"
- "Why can a trader be directionally right and still make a bad trade?"
- "Why does a line on a volume profile matter only after price reacts there?"
- "Why is not trading sometimes the most professional decision?"

The first page of a chapter should give the reader a reason to care before listing terms, screenshots, or time ranges.

### 2. Build A Book Arc, Not A Sequence Of Boxes

Before writing chapters, define the document's narrative arc:

1. the real-world decision problem;
2. the minimum vocabulary needed to see the problem;
3. the core mechanism;
4. one or two full cases that make the mechanism concrete;
5. the general rule extracted from the cases;
6. boundary conditions and failure modes;
7. exercises, review questions, or next-step practice.

For trading videos, this usually becomes:

- account constraints before entries;
- market location before order-flow evidence;
- order-flow evidence before execution;
- execution before results;
- results before statistics;
- statistics before psychology;
- psychology before final practice plan.

### 3. Vary Chapter Archetypes

A good textbook does not use one chapter mold everywhere. Select a chapter archetype according to the material:

- `problem_opener`: opens a major part by showing why the coming material matters.
- `concept_tool`: teaches one concept deeply, with intuition, definition, diagram, and misuse boundary.
- `mechanism_lab`: explains a causal chain or decision process step by step.
- `trade_case`: narrates one concrete trade in time order, but pauses at decision points.
- `post_mortem`: starts from the result, then works backward to ask what was skill, what was luck, and what was risk.
- `risk_memo`: centers on constraints, drawdown, slippage, account size, or execution limits.
- `statistics_interlude`: turns scattered performance claims into sample-size, distribution, expectancy, and variance language.
- `psychology_chapter`: connects real money, pressure, rule-breaking, and process design.
- `synthesis`: connects the whole video into a practice plan.

Do not repeat the same visible subheadings across many chapters. Planning fields may be complete internally, but the rendered chapter should take the shape required by the material.

### 4. Use Hidden Planning, Visible Prose

The writing plan may contain structured fields:

- learning goal;
- prerequisite concepts;
- evidence;
- misconception;
- risk boundary;
- review question.

Those fields are quality checks, not necessarily visible headings. In the final PDF, weave them into prose, examples, sidebars, captions, and transitions.

If more than two adjacent chapters use the same heading sequence, rewrite them.

### 5. Teach By Revisiting Ideas

A finance textbook does not define risk once and abandon it. It revisits the same idea under new conditions:

- first as a definition;
- then inside a trade;
- then as account-level risk;
- then as statistical variance;
- then as psychological pressure;
- finally as a practice rule.

For this skill, maintain a `concept_threads` map in `writing_plan.json`:

```json
{
  "concept_threads": [
    {
      "concept": "risk",
      "first_introduced": "PRE",
      "revisited_in": ["CH01", "CH02", "CH05", "CH06", "CH11"],
      "progression": "definition -> trade stop -> account drawdown -> profit cushion -> real-money psychology"
    }
  ]
}
```

Then write transitions that make these revisits explicit.

### 6. Prefer Cases Over Lists

When a video contains a concrete trade, the case should carry the teaching. A case chapter should read like a guided decision:

1. What was the trader allowed to risk?
2. What was the market doing before the decision?
3. What evidence made the trade worth considering?
4. What evidence would cancel the idea?
5. How was the trade sized or protected?
6. What changed after entry?
7. Why was the exit reasonable or questionable?
8. What should a novice copy, and what should not be copied?

Only after the case should the document extract a general principle.

### 7. Use Figures As Teaching Moments

Do not insert a screenshot because a section has a screenshot quota. Insert it only when it changes what the reader can understand.

Before a figure, tell the reader what to look for. After it, explain:

- what the image directly shows;
- how it connects to the text;
- what inference is reasonable;
- what cannot be concluded.

### 8. Use Questions As Chapter Engines

The best chapter titles often answer a real learner question:

- "为什么先讲账户规则，而不是先讲入场？"
- "低位反应为什么不是买入信号？"
- "所谓 risk-free 到底免掉了什么风险？"
- "为什么 order flow 不是魔法？"
- "赚到钱以后，为什么还要停止？"

Use these questions to make the chapter flow feel organic.

## Anti-Template Quality Gate

Before marking a PDF final, run this review:

- No more than two adjacent chapters may share the same visible heading sequence.
- At least 70 percent of the main body should be explanatory prose, case narration, figure interpretation, or mechanism discussion, not tables, repeated boxes, or bullet lists.
- Every part must contain transitions that say why the next chapter follows from the previous one.
- Planning fields must be present in `writing_plan.json`, but the final PDF must not expose them as a rigid checklist.
- Each chapter must have a distinct pedagogical job in the book arc.
- Review questions may appear at part endings or chapter endings; they do not need to interrupt every chapter in the same format.
- If a chapter looks like "本章学习目标 / 原文证据 / 知识点 / 交易流程 / 视觉证据 / 误区 / 复习题" repeated from prior chapters, it fails.

