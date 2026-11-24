> **Synthetic data** — simulated with fixed seeds; the negative WTI print is *modelled on* a real type of event, its value is invented.

### Context

The loaded file (step 1.2) is faithful to the vendor — including its mistakes. Before any statistic, a desk researcher runs explicit **quality controls** and decides, observation by observation, whether to **correct** (certain error), **investigate** (unknown cause) or **document** (a genuine feature of the market).

### Objective

Code three controls as explicit rules and produce a log of flagged observations with the action to take.

### Minimum theory

| control | detects | typical action |
|---|---|---|
| impossible values | Brent or Dubai ≤ 0 | correct (set to NaN) |
| negative WTI | expiry squeeze — can be real | keep and document |
| jump vs recent level | a price more than ×2 or below ×0.5 of its recent level | correct if the other benchmarks did not move |

The reference level must use **past values only** (here the median of the 5 previous valid prices, `shift(1)`), and a **median** because a single bad print does not move it.

### Assumptions

Brent and Dubai never double or halve in one day; WTI's front month can go negative; a flagged value is confirmed as an error by the other benchmarks on the same day (you check that in the explanation).

### Your task

Implement `quality_checks(prices)` for a `DataFrame` indexed by date with columns `brent`, `wti`, `dubai` (the output of step 1.2). Return a `DataFrame` with columns `date`, `series`, `value`, `issue`, `action`, one row per flag, sorted by `date` then `series`, index reset:

1. `brent` or `dubai` ≤ 0 → issue `"non-positive price"`, action `"set to NaN"`.
2. `wti` ≤ 0 → issue `"negative WTI print"`, action `"keep and document"`.
3. For `brent` and `dubai`: drop the missing values, compute `ratio = price / (median of the 5 previous valid prices)` with `rolling(5, min_periods=3).median().shift(1)`; flag `ratio > 2` or `ratio < 0.5` → issue `"jump vs last 5 days"`, action `"set to NaN"`.

The test code then builds the corrected dataset (it is also provided as `data/p1_crude_prices_clean_synthetic.csv` for the next steps). Answer in the **Explain** tab.
