> **Synthetic data** — the post-release drift exists in the simulation only in part of the history; nothing here is a real trading result.

### The desk asks

> “Your drift regression had t-stats around −4.8 — even after correcting for the overlap, it looked interesting. I've seen beautiful in-sample models lose money from day one. Does this one work on data it was not fitted on? I want a test where 2023–2024 played no role in building the model.”

### What you have

`data/p3_decision_table_daily_synthetic.csv` — one row per trading day 2019–2024: `date`, `surprise_mbbl` and `demand_growth_known_pct` (known at the 14:30 settlement), `target_end_date` and `ret_fwd_10d` (log return to the settlement 10 trading days later).

### What to find out

How the model performs on 2023–2024 compared with its own in-sample fit and with naive forecasts, and whether re-estimating it as time goes by changes the picture.

### Minimum theory (PDF A09-A/B/D/F, A10-A, A08-A)

- **Chronological split**: estimation period, then test period. A random split mixes future and past and measures nothing useful for a forecast.
- **Purging**: a training row can only be used if its label (here a 10-day return) is fully realised before the split — otherwise test-period prices leak into the estimation.
- **Frozen model**: choose the specification on the training period only; the test is used once.
- **Errors**: MAE (typical error), RMSE (weights large errors). In-sample R² measures fit to the past; out-of-sample error measures usefulness — compare it with **baselines** evaluated on the same rows: zero (no move expected) and the training mean.
- **Expanding-window walk-forward**: at each origin, re-estimate on all rows whose target was realised *before* the origin, predict the next block, move on. It shows whether the coefficients and errors are stable.

### Assumptions

- Training rows: `target_end_date ≤ 2022-12-31`. Test rows: `date ≥ 2023-01-01` and `target_end_date ≤ 2024-12-31`. Rows with a missing feature or target are dropped first.
- Walk-forward origins: 1 Jan, 1 Apr, 1 Jul, 1 Oct of 2023 and 2024 (`origin + pd.DateOffset(months=3)`); training rows: `target_end_date < origin`; predicted rows: test rows with `origin ≤ date < next origin`.
- Hit rate: share of test rows where the prediction and the realised return have the same sign.

### Your task

Implement `validate_out_of_sample(decisions)` returning:

- `fixed`: dict with `n_train`, `n_test`, `r2_in`, `mae_in`, `rmse_in`, `mae_out`, `rmse_out`, `mae_zero`, `rmse_zero`, `mae_mean`, `rmse_mean`, `hit_rate`;
- `coefficients`: the frozen model's parameters (Series);
- `walk_forward`: frame with `date`, `origin`, `realised`, `prediction` (fresh index);
- `walk_forward_path`: one row per origin with `origin`, `n_train`, `coef_surprise`, `coef_demand`;
- `walk_forward_mae`, `walk_forward_rmse`.

Chart the errors over time in the Test code pad, then the **Explain** tab.
