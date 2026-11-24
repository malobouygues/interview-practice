> **Synthetic data** — the price reaction and a temporary post-release drift are built into the simulation; they are not estimates from real markets.

### The desk asks

> “Can we use the weekly stock reports to understand WTI price reactions? Two questions: how much does a surprise move the price on the day, and does the market keep moving in the same direction afterwards? If it does, that's something we could trade after the release.”

### What you have

Built by the desk's pipeline with the rules of 3.1–3.3 (availability in UTC, backward joins, demand as known):

- `data/p3_release_events_synthetic.csv` — one row per release: `release_date`, `surprise_mbbl`, `wti_pre_release` (10:29 New York snapshot), `wti_settle` (14:30 settlement), `ret_reaction` = log(settle / pre-release), …
- `data/p3_decision_table_daily_synthetic.csv` — one row per trading day: what was known at the 14:30 settlement (`surprise_mbbl` of the latest published report, `demand_growth_known_pct`) and the label `ret_fwd_10d` = log return from this settlement to the settlement 10 trading days later, with `target_end_date`.

### What to find out

The size and precision of the release-day reaction, and whether there is a post-release drift — with standard errors that respect the structure of the data. **Use 2019–2022 only**: 2023–2024 is the untouched test period of 3.6.

### Minimum theory (PDF A10-C residual diagnostics, A09-D overlapping horizons)

- **Event study**: the return over a window around the event, regressed on the news (the surprise). A window that starts *before* the news is available would mix in earlier moves; this one starts at 10:29.
- **Overlapping returns**: two consecutive 10-day windows share 9 days, so their errors are correlated up to lag 9 *by construction*. Durbin-Watson ≈ 2 means no first-order autocorrelation; far below 2, strong positive autocorrelation.
- **Newey-West (HAC)** standard errors: robust to heteroskedasticity and autocorrelation up to `maxlags` (`fit(cov_type="HAC", cov_kwds={"maxlags": 9})`). Use `maxlags` ≥ the overlap − 1.
- HAC **changes** SEs, t, p and intervals; it **does not change** coefficients, fitted values, R² — and it does not repair look-ahead, a spurious regression or an unstable relationship.

### Assumptions

Reaction sample: releases with `release_date ≤ 2022-12-31`. Drift sample: days with `target_end_date ≤ 2022-12-31` (the label must be realised inside the research period). Rows with missing values dropped. HAC lags: 2 for the weekly reaction (for comparison only), 9 for the daily drift.

### Your task

Implement `reaction_and_drift(events, decisions)` returning:

- `reaction`: frame indexed by `const`, `surprise_mbbl` with `coef`, `se`, `t`, `se_hac`, `t_hac` (OLS of `ret_reaction` on the surprise);
- `drift`: same columns, indexed by `const`, `surprise_mbbl`, `demand_growth_known_pct` (OLS of `ret_fwd_10d`);
- `n_reaction`, `n_drift`, `dw_reaction`, `dw_drift` (Durbin-Watson of each residual series).

Look at the residual ACF in the Test code pad, then the **Explain** tab.
