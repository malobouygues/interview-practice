> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

WTI and Brent are cointegrated (4.7). A model in differences alone ignores where the levels are; a levels regression ignores daily dynamics. The **error correction model (ECM)** keeps both: how WTI reacts to Brent today, and how fast it closes any gap with the long-run relation.

### Objective

Estimate a basic two-step ECM, interpret its coefficients economically, and translate the speed of adjustment into a half-life.

### Minimum theory

`Δy_t = c + α·[y_{t−1} − β·x_{t−1} − a] + γ·Δx_t + e_t`

- The bracket is the **error-correction term**: yesterday's deviation from the long-run relation — the Engle-Granger step-1 residual, **lagged by one period**.
- **β**: long run. **γ**: short-run response to a same-day move of `x`.
- **α < 0**: speed of adjustment — the share of yesterday's deviation corrected today.
- **Half-life**: `ln(0.5) / ln(1 + α)` periods, meaningful for −1 < α < 0 when the model's assumptions hold.

### Assumptions

The series are cointegrated (otherwise the error-correction term is non-stationary and the regression is spurious); single equation, two steps (β estimated first and held fixed).

### Your task

Implement `fit_ecm(y, x)`:

1. Align, drop `NaN`; long run: OLS of `y` on a constant and `x` → `beta_long_run`, residuals = deviation.
2. A frame with `dy = y.diff()`, `deviation_lag = deviation.shift(1)`, `dx = x.diff()`; drop `NaN`.
3. OLS of `dy` on a constant, `deviation_lag` and `dx`.
4. Return `beta_long_run`, `alpha` (coefficient of `deviation_lag`), `alpha_tstat`, `gamma` (coefficient of `dx`), `half_life` (or `None` if α is not in (−1, 0)), `n` (int).

Answer in the **Explain** tab.
