> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Not market observations.

### Context

Step 4.1 showed that the daily pass-through from Brent to WTI looks very different before and after 1 January 2016 (0.59 vs 0.89). Is that difference statistically significant, or could it be noise? With a break date known in advance, the classical tool is the **Chow test**.

### Objective

Implement the Chow test from three regressions, apply it at the economically motivated date and at placebo dates, and understand why the regression you test matters as much as the test.

### Minimum theory

- Regression `y_t = a + b·x_t + e_t`, with `k = 2` parameters. Fit it three times: on the **whole sample** (residual sum of squares `SSR_p`), **before** the date (`SSR_1`) and **after** it (`SSR_2`).
- **H0**: the coefficients are identical in both sub-periods. **H1**: they differ.
- `F = [(SSR_p − SSR_1 − SSR_2) / k] / [(SSR_1 + SSR_2) / (n − 2k)]`, compared with an F distribution with `(k, n − 2k)` degrees of freedom: p-value = `scipy.stats.f.sf(F, k, n − 2k)`.
- Intuition: if separate lines fit much better than one common line, relative to the remaining noise, the coefficients changed.

### Assumptions

The date is known a priori; the variables are stationary; the errors are independent over time and have the **same variance** in both sub-periods. Daily log returns satisfy this reasonably well — I(1) price levels do not.

### Your task

Implement `chow_test(y, x, break_date)`:

- `y`, `x` — `pd.Series` with a `DatetimeIndex` (they may contain `NaN`: align and drop). *pre* = `index < break_date`, *post* = the rest.
- `ssr_*` = `.ssr` of `sm.OLS(y, sm.add_constant(x)).fit()` on each sample; `k = 2`; `n` = total observations.
- Return a `dict`: `F`, `pvalue`, `ssr_pooled`, `ssr_pre`, `ssr_post` (floats), `n_pre`, `n_post` (ints), `reject` (`pvalue < 0.05`).

The test code applies it to WTI on Brent **log returns** at 2016-01-01, at two placebo dates, and — as a warning — to log **levels**.

Then answer the question in the **Explain** tab.
