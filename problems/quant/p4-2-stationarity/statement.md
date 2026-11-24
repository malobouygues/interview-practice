> **Synthetic data** — Brent (daily, 2012–2019) and US diesel demand (monthly, 2010–2019) simulated with known properties.

### The desk asks

> “Before you regress anything on anything: what kind of series are we dealing with? One of the analysts tested our diesel demand series, found it ‘non-stationary’ and differenced it. Another says crude prices are random walks so nothing in levels means anything. Who is right?”

### What you have

- `data/p4_crude_research_daily_synthetic.csv` — daily `brent` (and others).
- `data/p4_diesel_demand_monthly_synthetic.csv` — `month`, `demand_kbd`: a physical demand series with a visible upward trend and a winter peak.

### What to find out

For each series and each candidate transformation: does ADF reject a unit root, with deterministic terms you can justify, and does the ACF of the transformed series look like what you intended?

### Minimum theory (PDF A06-A, A06-B, A06-D, A05-E)

- **Stationary**: constant mean, variance and autocorrelation over time. Sources of non-stationarity: a **stochastic trend** (unit root, shocks persist forever: I(1)), a **deterministic trend** (stationary around a line), **seasonality**, **breaks**, **changing volatility** — each needs a different treatment.
- **ADF**: H0 = unit root; H1 = stationary (around the deterministic terms). `adfuller(x, regression=..., autolag="AIC")` → statistic, p-value, lags used, n.
- **Deterministic terms**: `"n"` none (series around 0, e.g. returns), `"c"` constant (series around a level, e.g. log prices), `"ct"` constant + trend (series around a line). Choose them from the graph and the economics **before** looking at the p-value.
- **Transformations**: difference (stochastic trend), detrend (deterministic trend), remove month effects or seasonal difference (seasonality). Over-differencing a stationary pattern leaves an ACF near −0.5 at the differenced lag.
- **ACF**: a slow decay is a clue (trend or unit root), not a model order.

### Assumptions

Detrended and deseasonalised demand = residuals of OLS of demand on a constant, a linear trend and 11 month dummies (`pd.get_dummies(month, drop_first=True)`). ACF lag 20 for daily Brent, lag 12 for monthly demand.

### Your task

Implement `stationarity_table(prices, demand)` returning one row per candidate, in this order:

| series | transformation | regression |
|---|---|---|
| brent | log level | c |
| brent | log level | ct |
| brent | log return | n |
| diesel demand | level | c |
| diesel demand | level | ct |
| diesel demand | first difference | c |
| diesel demand | seasonal difference (12) | c |
| diesel demand | detrended and deseasonalised | n |

with `series`, `transformation`, `regression`, `adf_stat`, `p_value`, `lags_used`, `n_obs`, `acf_1`, `acf_long`, `long_lag`. Plot the series and their ACFs in the Test code pad, then the **Explain** tab.
