# Knowledge Point Extraction Rules

Knowledge extraction comes before visual search. The goal is to understand what the lecture teaches, then decide where visuals are needed.

## Output: `knowledge_points.json`

Use this structure:

```json
[
  {
    "id": "KP001",
    "title_zh": "控制点",
    "term_en": "Point of Control",
    "abbreviation": "POC",
    "category": "concept | mechanism | framework | strategy | case | metric | risk | misconception | viewpoint",
    "difficulty": "入门 | 进阶 | 专业 | 高级",
    "plain_explanation_zh": "",
    "professional_explanation_zh": "",
    "why_it_matters": "",
    "lecture_context": "",
    "timestamp_start": "00:00:00",
    "timestamp_end": "00:00:00",
    "transcript_evidence": [
      {
        "time_range": "00:00:00--00:00:00",
        "quote_or_paraphrase": ""
      }
    ],
    "related_terms": [],
    "common_misunderstandings": [],
    "manual_correction_flags": [],
    "needs_visual_evidence": true,
    "visual_question": ""
  }
]
```

## Explanation Standard

Each knowledge point should be teachable to a motivated learner.

Write:

- a simple explanation first
- a professional explanation second
- why the term matters in this video
- how it connects to surrounding ideas
- what mistake a learner may make

Avoid stiff phrasing such as "本段主要介绍..." repeated mechanically. Prefer concrete language:

- "这不是一个买入按钮，而是一个观察价格反应的位置。"
- "risk-free 在这里不是没有任何市场风险，而是止损已经移动到不会亏初始本金的位置。"
- "POC 说明成交最密集，不等于价格一定会反弹。"

For zero-foundation trading textbooks, use the novice standard:

- do not assume the learner knows the term;
- explain what it is in plain Chinese;
- explain where it appears in the video;
- explain why a trader cares;
- explain how it can be misread;
- explain what it cannot prove.

## Term Handling

If the transcript includes specialist language, preserve and explain it.

For finance/trading videos, define terms such as:

- POC: Point of Control，控制点，指定区间内成交量最集中的价格水平。
- VAH: Value Area High，价值区上沿。
- VAL: Value Area Low，价值区下沿。
- Range Chart: 按价格波动形成 K 线的图表，不按固定时间切分。
- Absorption: 吸收，指一方持续进攻但价格不能顺利延伸，说明另一方承接力量较强。
- Drawdown: 回撤，账户从高点回落的亏损幅度。
- Stop Loss: 止损，用于限制错误判断造成的亏损。
- Risk-Free Position: 在语境中通常指止损已移动到保本或锁定利润位置，不代表没有滑点或执行风险。
- Squeeze: 挤压，常指突破关键防守位后，对手方止损或追价导致价格加速。

Also explain when present:

- Futures / 期货
- Nasdaq / NQ
- Scalping / 剥头皮短线
- Order Flow / 订单流
- Volume Profile / 成交量分布
- Aggressive Buyers/Sellers / 主动买方/主动卖方
- Liquidation / 清算或强制平仓
- Trailing Stop / 移动止损
- Profit Factor / 盈利因子
- Edge / 交易优势
- Risk Reward / 风险收益比
- Win Rate / 胜率
- Slippage / 滑点
- CFD
- 0DTE Options / 当日到期期权
- Market Maker / 做市商
- Contraction Day / 收缩日
- Momentum Day / 动量日

Do not assume every term is correct just because ASR produced it. Mark uncertain terms in `manual_correction_flags`.

## Expanded Knowledge Cards

For trading textbook outputs, create `knowledge_cards_expanded.json` when core concepts exceed what fits cleanly in `knowledge_points.json`.

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
- how to observe it on the chart/interface;
- correct usage;
- novice misunderstandings;
- risk boundary;
- related concepts;
- counterexample or invalidation case;
- review question;
- standard answer.

Do not allow one-sentence cards for difficult mechanisms. Absorption, squeeze, risk-free position, edge, profit factor, drawdown, and order flow need multi-step explanation and misuse boundaries.

## Visual Need Decision

Set `needs_visual_evidence` to true when:

- the transcript refers to a chart, diagram, formula, code, table, order book, dashboard, or on-screen state
- the spoken explanation is ambiguous without seeing the visual
- the term depends on a spatial relation, such as price relative to POC/VAH/VAL/stop/target
- a learner could misunderstand the concept without visual grounding

The `visual_question` must be precise:

- Bad: "看一下图表。"
- Good: "画面是否同时显示 POC 水平线、volume profile 成交分布，以及价格相对 POC 的位置？"

## Manual Correction Flags

Add flags for:

- uncertain ASR term
- uncertain number or price
- unclear speaker attribution
- statement that sounds like investment advice
- visual state not available in transcript alone
- claim that requires later verification
