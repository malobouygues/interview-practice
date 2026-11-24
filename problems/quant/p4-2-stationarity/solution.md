### A. Reasoning — “non-stationary” is not a diagnosis

A series can be non-stationary because shocks accumulate (a random walk), because it grows along a line, because it repeats every year, because the world changed, or because its volatility changed. Each has a different cure, and the wrong cure creates problems: differencing a deterministic pattern injects artificial negative autocorrelation; leaving a stochastic trend in levels invites spurious regressions (4.3). The ADF test helps — if its deterministic terms are chosen for the right reasons, and if its null hypothesis is read correctly.

### B. Theory (PDF A06)

- **ADF regression**: Δy_t = [terms] + ρ·y_{t−1} + Σ φ_i Δy_{t−i} + e_t; H0: ρ = 0 (unit root). Non-rejection = “compatible with a unit root”, not “has a unit root”. Low power against near-unit-root and trend-stationary alternatives, and against stationary series with breaks.
- **Deterministic terms** (A06-B): from the economic nature and the graph — prices: constant; returns: none; trending physical series: constant + trend. Trying all three and keeping the convenient one is p-hacking.
- **Treatments** (A06-D): stochastic trend → difference; deterministic trend → detrend; fixed seasonality → month effects (or a seasonal difference if the season itself drifts); break → sub-periods.
- **Check the transformed series**: plot, ADF, ACF (no lag-1 or seasonal-lag value near −0.5).

### C. Implementation

A list of tuples `(name, transformation, series, regression, long_lag)` and one loop: `adfuller(series, regression=..., autolag="AIC")` returns six values; `acf(series, nlags=long_lag)`. Detrending: `pd.get_dummies(index.month, drop_first=True)` + a trend column, OLS, residuals.

### D. Interpretation (this dataset)

| series / transformation | terms | ADF | p | ACF lag 1 | ACF long |
|---|---|---|---|---|---|
| log Brent level | c | −0.99 | 0.76 | 0.999 | 0.985 (20) |
| log Brent level | ct | −0.24 | 0.99 | 0.999 | 0.985 |
| Brent log return | n | **−9.97** | < 0.001 | 0.020 | 0.023 |
| demand level | c | 0.31 | **0.98** | 0.876 | 0.714 (12) |
| demand level | ct | **−7.64** | < 0.001 | 0.876 | 0.714 |
| demand first difference | c | −9.35 | < 0.001 | 0.143 | **0.397** |
| demand seasonal difference | c | −6.91 | < 0.001 | 0.148 | **−0.485** |
| demand detrended + deseasonalised | n | −8.96 | < 0.001 | 0.090 | −0.052 |

- Brent: a unit root cannot be rejected; returns are clearly stationary → work with returns, or with a *tested* equilibrium in levels (4.4).
- Demand: the colleague's p = 0.98 came from omitting the trend. With the trend, the unit root is strongly rejected: demand is trend-stationary with a fixed season. Differencing leaves the season (0.40 at lag 12); seasonal differencing over-differences (−0.49 at lag 12); detrending + month effects leaves near-white noise.

### E. Decision

Model demand in levels with a trend and month effects (or as deviations from them) — do not difference it. Treat Brent and WTI levels as I(1) unless an economic equilibrium is shown to tie them (4.4); analyse co-movement on returns.

### F. Pitfalls and limits

- ADF on residuals of an estimated trend-plus-dummies model uses slightly different critical values than the tabulated ones; with a statistic of −9, the conclusion is unaffected.
- The Brent sample contains a slump with its own drift and a doubling of volatility: ADF can mistake a break for a unit root. Sub-period tests would help; they do not change the economic prior for prices.
- `autolag="AIC"` picks the lag length; a very different choice can move borderline statistics — report it.
- Stationarity is not required for every question: a forecast of next month's demand can be built on a trend-stationary model directly.

### G. Interview defence

*“ADF didn't reject on your demand series, so it has a unit root and you must difference it.”* — Two mistakes. Non-rejection is absence of evidence, not evidence of a unit root. And the test was run without a trend on a series that obviously has one, so the alternative it was testing against was wrong. With constant and trend it rejects at any level; differencing would only add a −0.5 autocorrelation at lag 12.
