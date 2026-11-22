> **Synthetic data** — simulated with fixed seeds. The regime change is *inspired by* the end of the US crude export ban (December 2015); its size and dynamics are invented.

### Context

Everything so far used the exports-allowed regime (from mid-2016), as decided in 4.1. Now test that choice on the full panel, 2012–2019. Until the end of 2015 US crude exports were banned: WTI was a landlocked crude priced at Cushing. Is 2012–2019 one Brent–WTI relationship, or two?

### Objective

Compare the relationship before and after a known date, and see what a structural break does to a cointegration test run on the whole sample.

### Minimum theory

- A **structural break**: a lasting change in the parameters of a relationship (level, slope, variance) at a date.
- With a **known** date, split the sample and compare the statistics of each sub-period.
- A shift in the equilibrium makes the residual of a full-sample regression shift in level; a stationary series with a level shift looks non-stationary (4.4) — so a full-sample cointegration test can miss a relationship that holds in each regime.
- **Placebo dates**: the same comparison at dates where nothing happened should show no change.

### Assumptions

One break at a known date; stability within each sub-period.

### Your task

Implement `regime_comparison(prices, break_date)` for a `DataFrame` indexed by date with `brent` and `wti`:

- *pre* = `index < break_date`, *post* = the rest; work on log prices.
- For each period compute (a helper function is natural here — it is used twice): `n`, `mean_spread` and `std_spread` of `log(brent) − log(wti)`, `return_beta` (OLS slope of WTI log returns on Brent log returns, with a constant, returns computed **within** the period), `return_corr`, `eg_pvalue` (`coint(log_wti, log_brent)` on the period).
- Return `{"pre": {...}, "post": {...}, "full_eg_pvalue": coint on the full sample}`.

Answer in the **Explain** tab.
