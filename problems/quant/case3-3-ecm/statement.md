> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Not market observations.

### Context

WTI and Brent are cointegrated (step 3.2). A model in differences alone would throw that information away; a model in levels alone would ignore the day-to-day dynamics. The **error correction model (ECM)** keeps both: it says how WTI reacts to Brent today, and how fast it closes any gap with the long-run relation.

### Objective

Estimate a basic two-step ECM, interpret its three coefficients economically and translate the speed of adjustment into a half-life.

### Minimum theory

The ECM (as in the source document):

`Δy_t = c + α·[y_{t-1} − β·x_{t-1} − a] + γ·Δx_t + e_t`

- `y_{t-1} − β·x_{t-1} − a` is the **error-correction term (ECT)**: yesterday's deviation from the long-run relation — in practice, the residual of the Engle-Granger step 1, lagged by one period.
- **β**: long-run relation (from step 1). **γ**: short-run response of `y` to a same-day move of `x`.
- **α < 0**: speed of adjustment — the share of yesterday's deviation corrected today. α = −0.2 means 20 % of the gap is closed per period.
- **Half-life** of a deviation: `ln(0.5) / ln(1 + α)` periods (defined for −1 < α < 0).

### Assumptions

The two series are cointegrated (otherwise the ECT is non-stationary and the regression is spurious). This is the single-equation, two-step version: the long-run relation is estimated first and then held fixed.

### Your task

Implement `fit_ecm(y, x)`:

1. Align `y` and `x`, drop `NaN`. Long-run step: OLS of `y` on a constant and `x` → `beta_long_run`; residuals = ECT.
2. Build a frame with `dy = y.diff()`, `ect_lag = ECT.shift(1)`, `dx = x.diff()`; drop `NaN`.
3. OLS of `dy` on a constant, `ect_lag` and `dx` (statsmodels).
4. Return a `dict`: `beta_long_run`, `alpha` (coefficient of `ect_lag`), `alpha_tstat`, `gamma` (coefficient of `dx`), `half_life` (`ln(0.5)/ln(1+alpha)` if −1 < alpha < 0, else `None`), `n` (int, observations in the ECM regression).

Then answer the question in the **Explain** tab.
