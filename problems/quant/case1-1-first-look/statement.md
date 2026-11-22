> **Synthetic data** — simulated with a fixed seed so that the concepts are visible. Not market observations.

### Context

You join a gas trading desk. Your first file is `data/ttf_daily_synthetic.csv`: the daily **settlement price of the front-month TTF contract**, in **€/MWh**, one row per **business day** from 2017 to 2019. It is a *price*: a level that is strictly positive, that is naturally aggregated by taking the last value or the mean (never the sum), and that, like most asset prices, may wander without a fixed anchor.

Before any test or model, a researcher describes the series — and describes it on the right scale.

### Objective

Write one function that summarises any series, then apply it to the price level **and** to the daily log returns, and explain why the two summaries tell different stories.

### Minimum theory

| Statistic | What it measures | Reading |
|---|---|---|
| mean / median | central value | a gap between them signals asymmetry or extreme values |
| variance, standard deviation | dispersion around the mean (std is in the unit of the data) | only meaningful if the dispersion is stable over time |
| skewness | asymmetry; > 0 = long right tail (upward spikes, typical of energy prices) | |
| excess kurtosis | tail thickness relative to a normal distribution (normal = 0) | > 0 = extreme values more frequent than a normal predicts |

A **log return** is `r_t = log(P_t) - log(P_{t-1})`: the relative change of the price, on a scale that does not depend on its level.

### Assumptions

Descriptive statistics summarise *the sample you have*. They estimate a stable property of the market only if the series is stationary (its distribution does not change over time) — which is exactly what the rest of this case investigates.

### Your task

Implement `summary_stats(x)`:

- `x` — a `pd.Series` (it may contain `NaN`, which must be ignored).
- Return a `dict` with exactly these keys, all plain Python numbers:

| Key | Definition (pandas convention) |
|---|---|
| `n` | number of non-missing values (`int`) |
| `mean`, `median` | `x.mean()`, `x.median()` |
| `var`, `std` | sample variance and standard deviation, `ddof=1` (`x.var()`, `x.std()`) |
| `skew` | `x.skew()` |
| `excess_kurtosis` | `x.kurt()` — pandas already returns *excess* kurtosis (0 for a normal) |

Do not modify the input. The test code loads the data and builds the log returns for you — read it, then run it.

Then answer the question in the **Explain** tab.
