> **Synthetic data** — simulated with fixed seeds; coffee is independent of crude by construction.

### Context

The first quantitative step of the hypothesis: how much does WTI move when Brent moves? A bivariate OLS answers it — and also produces standard errors, t-statistics and confidence intervals whose validity depends entirely on what you regress. You work on the exports-allowed regime (from 2016-07-01).

### Objective

Write an OLS wrapper that reports what a researcher needs, run it in **returns** and in **levels**, and learn which numbers can be trusted.

### Minimum theory

- `y_t = α + β x_t + e_t`, estimated by least squares. With logs on both sides β is an elasticity; in returns it is the same-day pass-through.
- **Standard error** of β: the precision of the estimate. **t = β / SE**. **p-value**: probability of a |t| at least that large if the true β were 0. **95 % CI**: β ± ≈ 1.96 SE.
- These **assume** stationary variables and errors that are independent over time with constant variance. Two price levels violate the first two.
- **Statistical significance ≠ economic significance**: with many observations, tiny effects become "significant"; judge the size in units.
- statsmodels: `res = sm.OLS(y, sm.add_constant(x)).fit()` → `res.params`, `res.bse`, `res.tvalues`, `res.pvalues`, `res.conf_int()`, `res.rsquared`, `res.resid`.

### Assumptions

For the returns regression, the usual OLS assumptions are reasonable (the next steps test the levels case).

### Your task

Implement `ols_fit(y, x)` for two `pd.Series` with the same date index (they may contain `NaN`): align them, drop incomplete rows, fit with a constant, and return a `dict`:

`alpha`, `beta`, `beta_se`, `beta_tstat`, `beta_pvalue`, `beta_ci_low`, `beta_ci_high` (95 %), `r2`, `resid_std` (pandas `.std()` of the residuals), `n` (int).

Answer in the **Explain** tab.
