> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

Not every trending series is a random walk. US diesel demand (`data/p4_diesel_demand_monthly_synthetic.csv`, kb/d, monthly 2010–2019) grows with activity along a fairly stable path, with a strong winter (heating) seasonality. The Brent price also "trends". Applying the same transformation to both — the reflex `diff()` — is a classic mistake.

### Objective

Decide, for a monthly series, between **detrend** (deterministic trend) and **difference** (stochastic trend), and measure the damage of the wrong choice.

### Minimum theory

| | deterministic trend | stochastic trend (unit root) |
|---|---|---|
| model | `y_t = a + b·t + stationary noise` | `y_t = y_{t−1} + drift + shock` |
| shocks | transitory | permanent |
| remedy | **detrend** | **difference** |
| ADF | does not reject with `'c'`, **rejects with `'ct'`** | rejects with neither |

- Deterministic seasonality (same profile every year) is removed **before** testing: subtract the average deviation of each calendar month.
- **Over-differencing** a stationary series inflates its variance and destroys the level information; **detrending** a random walk leaves a wandering residual.

### Assumptions

Linear trend, stable seasonal profile, complete years, no structural break.

### Your task

Implement `trend_or_random_walk(y)` for a monthly `pd.Series` with a `DatetimeIndex`:

1. Drop `NaN`; `t = 0 … n−1`; fit `slope, intercept = np.polyfit(t, y, 1)`; `trend = intercept + slope·t`.
2. Seasonal profile = mean of `y − trend` by calendar month; deseasonalised = `y` minus the profile value of its month.
3. ADF p-values of the deseasonalised series with `'c'` and `'ct'` (`autolag="AIC"`).
4. `std_detrended` = std of (deseasonalised − trend); `std_differenced` = std of the first difference of the deseasonalised series.
5. `decision`: `"stationary"` if the `'c'` p-value < 0.05; else `"detrend"` if the `'ct'` p-value < 0.05; else `"difference"`.

Return `trend_per_year` (`slope·12`), `seasonal_amplitude` (max − min of the profile), `adf_p_c`, `adf_p_ct`, `std_detrended`, `std_differenced`, `decision`. Answer in the **Explain** tab.
