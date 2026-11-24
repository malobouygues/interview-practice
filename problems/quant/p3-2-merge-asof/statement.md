> **Synthetic data** — simulated WTI settlements and weekly stocks; the price reaction to the stock surprise is built into the simulation.

### The desk asks

> “For every trading day, I want the stock information we actually had at the settlement. One of the analysts already did it and found that the latest stock surprise predicts the next day's WTI return with a t-stat of −4.4. If that's true it's a strategy. Is it?”

### What you have

- `data/p3_wti_daily_synthetic.csv` — `date`, `wti_settle_usd_bbl` (NYMEX settlement, 14:30 New York), 2019–2024.
- `data/p3_us_crude_stocks_weekly_synthetic.csv` — the weekly reports; the Test code pad rebuilds `available_at`, `surprise_mbbl` as in 3.1.

### What to find out

A daily table in which every stock figure is one a trader could have seen at the settlement — and whether the analyst's “signal” survives.

### Minimum theory (PDF A04-B joins, A04-E look-ahead, A04-F validation after alignment)

- **Decision time**: when the decision is taken — here the settlement, `date + 14:30` New York, converted to UTC like `available_at`.
- `pd.merge_asof(left, right, left_on=..., right_on=..., direction="backward", tolerance=...)`: for each left row, the last right row whose key is ≤ the left key and not older than the tolerance. Both sides sorted on their key.
- **The key decides everything**: on `available_at` the join is point-in-time; on `week_ending` it attaches reports before they exist.
- **Check after joining**: no matched `available_at` after its decision time (assertion), the distribution of the age of matched values, a few rows checked by hand.
- A predictive test must use information known at the *start* of the return window: the return from settlement t to t+1, against what was known at settlement t.

### Assumptions

Tolerance 10 days. `age_days` = days between the settlement date and the `week_ending` of the matched report.

### Your task

Implement `align_stocks(prices, stocks)`:

1. Copy `prices`; parse `date`; `decision_time` = `date + 14:30`, localised to New York, in UTC; sort by it.
2. From `stocks` take `available_at`, `week_ending`, `crude_stocks_mbbl`, `surprise_mbbl`, sorted by `available_at`.
3. Backward `merge_asof` on `decision_time` / `available_at`, tolerance 10 days.
4. `age_days`; assert that every matched `available_at` ≤ `decision_time`.
5. Return `date`, `wti_settle_usd_bbl`, `decision_time`, `week_ending`, `available_at`, `crude_stocks_mbbl`, `surprise_mbbl`, `age_days`.

Reproduce the analyst's result with the wrong key in the Test code pad, then the **Explain** tab.
