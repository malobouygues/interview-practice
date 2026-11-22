> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Not market observations.

### Context

Correlation says *how strongly* two series move together; a regression says *by how much* one moves when the other does. A simple bivariate OLS is also the first building block of the cointegration test of Case 3 — so you need to master it, including what its output does **not** mean when the data are non-stationary.

### Objective

Write a small OLS wrapper, run WTI on Brent in **log levels** and in **log returns**, and interpret the coefficients and residuals.

### Minimum theory

- Model: `y_t = α + β·x_t + e_t`, estimated by ordinary least squares (minimises the sum of squared residuals).
- **β**: change in `y` for a one-unit change in `x`. With both in logs, β is an *elasticity*: % change in `y` for a 1 % change in `x`.
- **Residual** `e_t = y_t − α − β·x_t`: the part of `y` the line does not explain.
- **R²**: share of the variance of `y` explained. **t-stat of β**: β divided by its standard error; |t| > 1.96 ≈ significant at 5 % — *if* the assumptions hold.
- In statsmodels: `res = sm.OLS(y, sm.add_constant(x)).fit()` → `res.params`, `res.tvalues`, `res.rsquared`, `res.resid`.

### Assumptions

OLS inference (standard errors, t-stats, p-values) assumes stationary variables and errors that are not dependent over time. Two I(1) price levels violate both.

### Your task

Implement `ols_fit(y, x)`:

- `y`, `x` — `pd.Series` with the same date index (they may contain `NaN`, e.g. the first row of a return). Align them, drop incomplete rows.
- Fit `y = α + β·x` with a constant (statsmodels `OLS`).
- Return a `dict`: `alpha`, `beta`, `beta_tstat`, `r2`, `resid_std` (standard deviation of the residuals, pandas `.std()`), `n` (int, observations used).

The test code runs: log WTI on log Brent (levels), the same in daily log returns, and log coffee on log Brent.

Then answer the question in the **Explain** tab.
