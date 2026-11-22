> **Synthetic data** — simulated with fixed seeds; the price reaction to stock surprises is built in, values are invented.

### Context

A junior analyst presents a "signal": *a build in US crude stocks predicts a fall in WTI over the following week*. The correlation is clearly negative. You suspect the alignment.

### Objective

Measure the relation between the latest known weekly stock change and the **next five days' WTI return** under three alignments, and show which one is legitimate.

### Minimum theory

- **Outcome**: `next_5d_return_t = log P_{t+5} − log P_t` — it uses future prices *on purpose*: it is what we try to explain, never an input.
- **Signal**: the latest weekly change in stocks known at the decision time t (14:30 settlement).
- If the market reacts to the report **on the release day**, a signal that is "known" before the release will look predictive, because the reaction falls inside its next-5-day window. That predictive power is an artefact of the publication lag.

### Assumptions

Decision at the 14:30 New York settlement; stock changes computed from consecutive weekly levels.

### Your task

Implement `predictive_correlation(prices, stocks, align_on)`:

1. Sort `stocks` by `week_ending` (copy) and add `stock_change` = first difference of `crude_stocks_mbbl`; drop the first row.
2. Copy `prices`, convert `date`, sort, add `decision_time = date + 14:30` and `next_5d_return = log(price).shift(−5) − log(price)`.
3. `merge_asof` backward of `prices` (on `decision_time`) with `stocks[[align_on, "stock_change"]]` sorted by `align_on` (on `align_on`) — no tolerance.
4. Drop rows where `stock_change` or `next_5d_return` is missing.

Return `{"n": number of rows, "corr": correlation of stock_change and next_5d_return}`. `align_on` is `"week_ending"`, `"available_at"` or `"ingested_at"` (the stock table has all three as datetimes). Answer in the **Explain** tab.
