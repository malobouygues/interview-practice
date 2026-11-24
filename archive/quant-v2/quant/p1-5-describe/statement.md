> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

The clean dataset (`data/p1_crude_prices_clean_synthetic.csv`) is ready. Before modelling anything, describe it: a crude desk wants to know the typical level, the typical move, how fat the tails are, and how the spreads behave — and you want to know which of these numbers can be trusted.

### Objective

Write one function that summarises any series, apply it to the Brent **level**, Brent **daily log returns** and the **Brent–WTI spread**, and explain why the three summaries call for different statistics.

### Minimum theory

| statistic | measures | caution |
|---|---|---|
| mean / median | central value | the mean is pulled by extremes; the median is not |
| variance / standard deviation | dispersion around the mean | meaningful only if the dispersion is stable over time |
| quantiles (5 %, 95 %) | the range that contains 90 % of observations | robust to a few extremes |
| skewness | asymmetry (> 0: long right tail) | dominated by a few points |
| excess kurtosis | tail thickness vs a normal (normal = 0) | very sensitive to single events |

A **log return** is `log(P_t) − log(P_{t−1})`, computed between consecutive observed prices.

### Assumptions

Statistics describe *this* sample. They estimate a stable property of the market only if the series is stationary — which the level is not (Project 4 tests it formally).

### Your task

Implement `summary_stats(x)` for a `pd.Series` (ignore `NaN`). Return a `dict` with plain Python numbers:

`n` (int, non-missing values), `mean`, `median`, `std` and `var` (sample, `ddof=1`), `q05` and `q95` (`x.quantile(0.05)`, `x.quantile(0.95)`), `skew` (`x.skew()`), `excess_kurtosis` (`x.kurt()`: pandas already returns **excess** kurtosis).

Do not modify the input. Then answer in the **Explain** tab.
