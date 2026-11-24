> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

You now attach to each daily WTI settlement (`data/p3_wti_daily_synthetic.csv`, `date`, `wti_usd_bbl`) the **latest weekly stock level known at that moment**. Two frequencies, two release schedules: the classic tool is `pd.merge_asof`, and the classic mistake is to use it on the wrong key.

### Objective

Build a daily table in which every stock value is one a trader could have seen at the 14:30 New York settlement.

### Minimum theory (PDF, A04-B)

- `pd.merge_asof(left, right, left_on=..., right_on=..., direction="backward")`: for each left row, the last right row whose key is **≤** the left key. Both tables **must be sorted** on their key.
- `tolerance=pd.Timedelta(days=10)`: no match if the latest value is older than that → `NaN` rather than a stale number.
- **Backward + availability key + right vintage = point-in-time.** A backward join on the observation date still leaks.
- Check after the join: no `available_at` after the decision time; distribution of the age of matched values.

### Assumptions

Decision time = WTI settlement, `date + 14:30` New York; the stock table comes from step 3.1 (`available_at` computed).

### Your task

Implement `align_stocks(prices, stocks)`:

1. Copy `prices`, convert `date`, add `decision_time = date + 14:30`, sort by it.
2. Take `available_at`, `week_ending`, `crude_stocks_mbbl` from `stocks`, sorted by `available_at`.
3. `merge_asof` backward on `decision_time` / `available_at`, tolerance 10 days.
4. `age_days` = days between `decision_time` and `week_ending` (`.dt.days`).
5. Assert that every matched `available_at` is ≤ its `decision_time`.

Return the columns `date`, `wti_usd_bbl`, `week_ending`, `available_at`, `crude_stocks_mbbl`, `age_days`. Answer in the **Explain** tab.
