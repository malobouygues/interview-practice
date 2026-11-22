> **Synthetic data** — simulated with fixed seeds; the diesel crack responds to true demand conditions by construction.

### Context

A colleague's chart shows the monthly diesel crack (`data/p3_diesel_crack_monthly_synthetic.csv`) moving closely with US demand growth (year-on-year, %), and concludes that demand data are a strong indicator for the crack. The chart uses the **final, revised** demand history, aligned on the **observation month**. Using the vintages of step 3.4, rebuild what was actually known at each month-end.

### Objective

For each decision date (month-end), compute the year-on-year demand growth an analyst could compute **that day**, and compare it with the final growth of the same month.

### Minimum theory

- At decision date t, the information set is the as-of view at t (step 3.4): its latest month is about two months old.
- **Real-time growth** at t: in the as-of view, `value(latest month) / value(same month a year earlier) − 1` — computed within the view, as the analyst did (mixing a fresh first estimate with an older, revised year-ago value).
- **Pseudo point-in-time**: final revised data, even when publication lags are respected. **Not point-in-time**: final data aligned on the observation month (lag ignored).

### Assumptions

Decisions at each month-end; growth in % (`pct_change(12) * 100` on a complete monthly view).

### Your task

Implement `realtime_growth(vintages, decision_dates)`:

1. Copy; convert `obs_month` (`format="%Y-%m"`) and `vintage_date`; sort by `vintage_date`.
2. Final growth: the latest estimate per month over all vintages, then `pct_change(12) * 100`.
3. For each decision date: the as-of view (vintages published on or before that date, latest per month), its growth `pct_change(12) * 100`, the latest month of the view, and the real-time growth of that month. Record `[decision_date, obs_month, growth_realtime, growth_final_of_that_month]`.

Return a `DataFrame` indexed by `decision_date` with columns `obs_month`, `growth_realtime`, `growth_final`. Answer in the **Explain** tab.
