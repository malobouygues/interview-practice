### A. Reasoning — know the background before naming the anomaly

A “spike” only means something relative to a normal day. Power prices have a strong daily shape, a weekly rhythm, very fat tails and volatility that comes in episodes. Measuring those first prevents two mistakes: calling an ordinary evening peak a spike, and reading a correlation produced by the clock as a market mechanism.

### B. Theory (PDF A05)

- **Visual analysis** (A05-A): level, changes, histogram, boxplot by period — each answers a different question (timing, volatility, tails, seasonality).
- **Statistical properties** (A05-B): mean vs median, skewness, kurtosis. With excess kurtosis in the hundreds, a standard deviation is a poor summary and a z-score threshold flags too much or too little.
- **Rolling statistics** (A05-C): a 30-day window shows when the distribution changed.
- **Correlation** (A05-D): Pearson measures linear co-movement *at the sampling frequency*; with a common driver (time of day, season) it measures the driver. Remove the common component before interpreting.
- **ACF** (A05-E): peaks at seasonal lags = seasonality; the pattern is a clue, not a model order.

### C. Implementation

`groupby("local_hour").quantile(q)` for the boxplot statistics; `diff().dropna()` then `.std()`, `.skew()`, `.kurt()`; `acf(load, nlags=168)`; `x - x.groupby(local_hour).transform("mean")` to remove the hour-of-day mean; `groupby("local_date").mean().diff().rolling(30).std()`.

### D. Interpretation (this dataset)

- **Profile**: median 30.7 €/MWh at 03:00–04:00, 43.7 at 08:00, **50.3 at 19:00**; the 90th percentile reaches **108** at 18:00. High prices live in the evening peak, when solar has gone and load is still high.
- **Changes**: std **27.7**, skewness **6.8**, excess kurtosis **≈ 1,010**; **0.59 %** of changes beyond 3 std (normal law: 0.27 %). Prices go down to −123 €/MWh, so log returns are impossible.
- **Load ACF**: **0.950** (1 h), **0.011** (12 h), **0.931** (24 h), **0.951** (168 h): daily and weekly cycles.
- **Load–solar**: **+0.141** raw, **−0.447** within the hour. The raw sign comes from the daily cycle; the within-hour sign mostly from the annual cycle (sunny hours fall in summer, when there is no heating).
- **Rolling volatility**: highest (**70.3**) for the 30 days ending 21 Oct 2023, lowest (**4.0**) in late July 2023.

### E. Decision

For spikes: work at the daily level (the daily maximum or the evening peak), use rank statistics or medians, and look first at October 2023 and the winters, where volatility clusters. Discard the analyst's correlation: it measures the clock and the season, not solar.

### F. Pitfalls and limits

- Correlations on hourly data mix daily, weekly and annual cycles: compare like with like (same hour, same season) before interpreting.
- `plot_acf` on a series with gaps or on a 23/25-hour day calendar in local time misaligns lags — the UTC index avoids it.
- Kurtosis is dominated by a handful of observations: it describes this sample, not a stable law.
- The boxplot hides the extreme points on purpose (`showfliers=False`): spikes are the subject of 1.6, not of the profile.

### G. Interview defence

*“Your ACF has a huge spike at lag 168 — will you fit an autoregressive model with 168 lags?”* — No. A peak at one week on hourly load is the weekly calendar: Mondays look like Mondays. The ACF is a diagnostic. I'd model the calendar explicitly (hour, day of week, season, weather) and look at the ACF of what remains.
