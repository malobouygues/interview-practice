> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). The regime change is *inspired by* the end of the US crude export ban (December 2015); its size and dynamics are invented.

### Context

Cases 2–3 used data from mid-2016. The desk now gives you the full history, `data/crude_history_synthetic.csv` (Brent and WTI, business days 2012–2019) — and a piece of context: **until the end of 2015 US crude exports were banned**. WTI was a landlocked crude priced at Cushing; from 2016 it could be shipped abroad. Does the relationship you modelled survive on the longer sample, or are there two relationships?

### Objective

Compare the Brent–WTI relationship before and after a known date, and see what a structural break does to a cointegration test run on the whole sample.

### Minimum theory

- A **structural break** is a lasting change in the parameters of a relationship (level, slope, variance) at a date.
- With a **known** date, the simplest analysis splits the sample and compares the statistics of each sub-period.
- A break in the long-run relation (e.g. the equilibrium spread moves) makes the residual of a full-sample regression shift in level. A stationary series with a level shift looks non-stationary (step 1.4) — so a full-sample cointegration test can miss a relationship that holds in each regime.
- The date must come from **outside the data** (an event with an identifiable mechanism), not from searching the chart for the biggest change.

### Assumptions

One break, at a known date; within each sub-period the relationship is stable.

### Your task

Implement `regime_comparison(prices, break_date)`:

- `prices` — a `DataFrame` indexed by date with columns `brent` and `wti`; `break_date` — a string such as `"2016-01-01"`. The *pre* period is `index < break_date`, the *post* period the rest.
- For each period compute, on log prices:
  - `n` (int), `mean_spread` and `std_spread` of `log(brent) − log(wti)`,
  - `return_beta`: slope of the OLS of WTI log returns on Brent log returns (with a constant; returns computed **within** the period),
  - `return_corr`: correlation of the two return series,
  - `eg_pvalue`: `coint(log_wti, log_brent)` p-value on that period.
- Return `{"pre": {...}, "post": {...}, "full_eg_pvalue": ...}` where the last value is `coint` on the full sample.

Then answer the question in the **Explain** tab.
