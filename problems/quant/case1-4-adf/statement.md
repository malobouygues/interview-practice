> **Synthetic data** — simulated with a fixed seed so that the concepts are visible. Not market observations.

### Context

The block statistics of step 3 say the TTF level wanders like a random walk. Your PM wants a formal answer. The standard tool is the **Augmented Dickey-Fuller (ADF)** test — and the standard mistake is to call `adfuller(y)` and read the p-value as "stationary / not stationary".

### Objective

Wrap the ADF test in a function that returns what you need to report, and learn to read it — including what it cannot tell you.

### Minimum theory

The ADF test runs the regression

`Δy_t = [constant] + [trend·t] + γ·y_{t-1} + (lagged Δy terms) + e_t`

- **H0: γ = 0** — unit root, non-stationary. **H1: γ < 0** — stationary (around 0, around a level, or around a linear trend, depending on the deterministic terms).
- The statistic is the t-stat of γ, compared with **Dickey-Fuller** critical values (not Student's t). The more negative, the stronger the rejection.
- **Lagged differences** absorb short-term dependence in the errors; `autolag="AIC"` chooses how many.
- **Deterministic terms** (`regression=`): `'n'` nothing (series centred on 0: returns, residuals) · `'c'` constant (a level, e.g. a spread) · `'ct'` constant + trend (visible trend, e.g. demand). Leaving out a trend that is there makes a trend-stationary series look like a unit root; adding useless terms costs power.
- `statsmodels.tsa.stattools.adfuller(x, regression=..., autolag="AIC")` returns `(stat, pvalue, usedlag, nobs, critical_values_dict, icbest)`.

### Assumptions

The test assumes the specification is right (deterministic terms, enough lags) and that the process is stable over the sample — no structural break. Its power depends on the **time span** covered, not on the number of points.

### Your task

Implement `adf_report(x, regression="c")`:

- Drop missing values, run `adfuller(x, regression=regression, autolag="AIC")`.
- Return a `dict`: `stat` (float), `pvalue` (float), `lags` (int, lags used), `nobs` (int), `crit_5pct` (float, the 5 % critical value), `reject_unit_root` (bool, `pvalue < 0.05`).

The test code runs it on the TTF level, its returns and four controlled examples.

Then answer the question in the **Explain** tab.
