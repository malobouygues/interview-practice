> **Synthetic data** — a fictional power market, simulated with fixed seeds. Not market observations.

### The desk asks

> “Before you show me the spikes, show me what normal looks like. When in the day is power expensive? How wild are hour-to-hour moves? And one of the analysts found that solar output and load are positively correlated — is solar pushing load up?”

### What you have

`data/p1_power_hourly_treated_synthetic.csv` — the output of 1.2 (UTC index; `local_date`, `local_hour`, `price_eur_mwh`, `load_mw`, `wind_mw`, `solar_mw`, capacity and flags). The loader is in the Test code pad.

### What to find out

The daily shape of prices, the distribution of hourly price changes, how persistent load is, whether the analyst's correlation means anything, and when volatility was high.

### Minimum theory (PDF A05-A to A05-E)

- **Boxplot by hour** = quartiles of the price at each local hour: it shows where in the day prices — and their dispersion — are high.
- **Changes, not log returns**: power prices can be negative, so `log(p_t / p_{t-1})` does not exist; use `diff()`.
- **Skewness** (asymmetry) and **excess kurtosis** (`.kurt()`, 0 for a normal law): fat tails mean the standard deviation understates the risk of extreme moves. Under a normal law 0.27 % of observations lie beyond 3 standard deviations.
- **ACF** (`statsmodels.tsa.stattools.acf`): correlation of the series with itself k steps earlier. Peaks at 24 and 168 hours are calendar cycles. A slowly decaying or periodic ACF is not, by itself, evidence of a high-order autoregressive model.
- **A correlation made by a common driver**: two series that both follow the clock correlate even with no link between them. Removing each series' hour-of-day mean (`groupby("local_hour").transform("mean")`) shows what is left *within* an hour.
- **Rolling volatility**: `daily_price.diff().rolling(30).std()`.

### Assumptions

ACF on the full hourly load series (no gaps in load). Hourly changes in UTC order; changes next to a missing price are dropped.

### Your task

Implement `price_patterns(hours)` returning a dict:

1. `hourly_profile`: indexed by `local_hour`, columns `q10`, `q25`, `median`, `q75`, `q90` of the price.
2. `change_stats`: of `price.diff().dropna()` — `std`, `skew`, `excess_kurtosis`, `share_beyond_3_std_pct`.
3. `acf_load`: `{1: ..., 12: ..., 24: ..., 168: ...}` from `acf(load_mw, nlags=168)`.
4. `load_solar_correlation`: `{"raw": ..., "within_hour": ...}` (within-hour = correlation of the deviations from each series' mean at that local hour).
5. `rolling_std_30d`: 30-day rolling standard deviation of the change in the daily average price (indexed by `local_date`).

Draw the charts in the Test code pad, then the **Explain** tab.
