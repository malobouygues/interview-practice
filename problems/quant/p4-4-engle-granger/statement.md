> **Synthetic data** — the end of the US export ban (end-2015) is imitated by a change in the simulated WTI dynamics; values are invented.

### The desk asks

> “Brent and WTI clearly co-move day to day. But is there a long-run level they come back to — something I could trade the spread around? And I remember a 15-dollar discount in 2013; does that still mean anything?”

### What you have

`data/p4_crude_research_daily_synthetic.csv` — daily `brent`, `wti`, 2012–2019. Known event: the US crude export ban was lifted at the end of 2015.

### What to find out

Whether log WTI and log Brent are cointegrated, whether the relationship is the same before and after 2016, and what that means for a spread trader.

### Minimum theory (PDF A06-E, A05-D sub-periods, A08)

- **Why test at all**: Brent and WTI are substitutes linked by physical arbitrage (shipping, refinery runs, export capacity). The mechanism comes first; Engle-Granger (`coint(y, x)`, H0: no cointegration) only checks whether the data are compatible with it.
- **Long run**: OLS of log WTI on log Brent — a coefficient near 1 means a stable *percentage* discount.
- **Short run**: OLS of the daily log change of WTI on that of Brent — the **pass-through**.
- **Structural change at a known date**: estimate by sub-period. **Chow test** on the short-run regression (stationary data): with k coefficients, `F = ((SSR_pooled − SSR_1 − SSR_2) / k) / ((SSR_1 + SSR_2) / (n − 2k))`, compared with an F(k, n − 2k) (`scipy.stats.f.sf`). It assumes the same error variance in both periods. **Placebo dates** inside a regime should not reject.
- Optional extension: an **error-correction model** `ΔWTI_t = c + γ ΔBrent_t + α·gap_{t−1} + e`, half-life `ln(0.5) / ln(1 + α)`.

### Assumptions

Logs of prices. Compute the daily changes **once on the full sample, then split them by date**: the change across the break belongs to the second period, and both sides of the Chow test use the same days. `n` for the Chow test = number of daily changes in the full sample; k = 2.

### Your task

Implement `relationship_by_period(prices, break_date="2016-01-01")` returning:

- `periods`: frame indexed by `"full sample"`, `"before <break_date>"`, `"from <break_date>"` with `n_days`, `eg_stat`, `eg_p`, `long_run_beta`, `mean_spread_usd` (Brent − WTI in $/bbl), `pass_through`, `pass_through_se`;
- `chow_f`, `chow_p`: Chow test at `break_date` on the short-run regression.

Run the placebos and the optional ECM in the Test code pad, then the **Explain** tab.
