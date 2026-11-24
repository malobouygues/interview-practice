> **Synthetic data** — daily Brent, WTI, Dubai and coffee prices simulated with fixed seeds, 2012–2019. The end of the US crude export ban (end-2015) is imitated; values are invented.

### The desk asks

> “Brent and WTI often move together. Can we establish whether this is a meaningful relationship, or are we simply correlating two trending price series? Start with the basics — and humour me: put coffee in as well.”

### What you have

`data/p4_crude_research_daily_synthetic.csv` — `date`, `brent`, `wti`, `dubai`, `coffee` (USD/bbl for crude, US cents/lb for coffee), business days 2012–2019.

### What to find out

What the levels and the daily changes each say about co-movement, the shape of the return distribution, whether volatility is stable, and how the Brent–WTI spread evolved.

### Minimum theory (PDF A05-A to A05-D)

- **Levels vs returns**: levels carry trends; daily log returns `log(p_t / p_{t−1})` carry day-to-day moves. A correlation of levels mostly measures whether two series trended the same way over the sample.
- **Pearson** (linear, sensitive to extremes) vs **Spearman** (on ranks, robust).
- **Mean vs median**, **skewness**, **excess kurtosis** (0 for a normal law).
- **Volatility**: standard deviation of returns; annualised × √252. A 60-day rolling window shows regimes.
- **Spread**: Brent − WTI in USD/bbl, the quality/location differential between the two crudes.

### Assumptions

Returns are daily log returns; volatility is annualised with 252 trading days.

### Your task

Implement `levels_and_returns(prices)` returning a dict:

- `level_corr`: `{"brent_wti": ..., "wti_coffee": ...}` (Pearson, levels);
- `return_corr`: `{"brent_wti_pearson", "brent_wti_spearman", "wti_coffee_pearson"}` on daily log returns;
- `brent_distribution`: `mean`, `median`, `std`, `skew`, `excess_kurtosis` of Brent log returns;
- `rolling_vol_60d`: annualised 60-day rolling volatility of Brent (Series indexed by date);
- `yearly_vol`: annualised volatility of Brent by calendar year;
- `spread_by_year`: mean Brent − WTI spread by calendar year.

Draw the charts in the Test code pad, then the **Explain** tab.
