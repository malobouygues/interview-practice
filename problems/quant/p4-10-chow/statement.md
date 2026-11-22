> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

Step 4.9 showed the daily pass-through from Brent to WTI looks very different before and after 1 January 2016 (0.59 vs 0.89). Statistically significant, or noise? With a date known in advance, the classical tool is the **Chow test**.

### Objective

Implement the Chow test from three regressions, apply it at the economically motivated date and at placebo dates, and understand why the regression you test matters as much as the test.

### Minimum theory

- Regression `y_t = a + b·x_t + e_t`, `k = 2` parameters. Fit it on the **whole sample** (`SSR_pooled`), **before** the date (`SSR_pre`) and **after** it (`SSR_post`).
- **H0**: identical coefficients in both sub-periods. **H1**: they differ.
- `F = [(SSR_pooled − SSR_pre − SSR_post) / k] / [(SSR_pre + SSR_post) / (n − 2k)]`, compared with an F distribution with `(k, n − 2k)` degrees of freedom: p-value = `scipy.stats.f.sf(F, k, n − 2k)` (`scipy` is installed with `statsmodels`).
- Intuition: if separate lines fit much better than one common line, relative to the remaining noise, the coefficients changed.

### Assumptions

Date known a priori; stationary variables; errors independent over time with the **same variance** in both sub-periods.

### Your task

Implement `chow_test(y, x, break_date)` for two `pd.Series` with a `DatetimeIndex` (align, drop `NaN`; *pre* = `index < break_date`). Fit the three regressions with `sm.OLS(..., sm.add_constant(...))` and use `.ssr`. Return `F`, `pvalue`, `ssr_pooled`, `ssr_pre`, `ssr_post` (floats), `n_pre`, `n_post` (ints), `reject` (`pvalue < 0.05`).

The test code applies it to WTI on Brent **log returns** at 2016-01-01, at two placebo dates, and — as a warning — to log **levels**. Answer in the **Explain** tab.
