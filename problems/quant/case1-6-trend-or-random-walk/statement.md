> **Synthetic data** — simulated with a fixed seed so that the concepts are visible. Not market observations.

### Context

A colleague on the products desk sends you a second series: **monthly diesel demand** in kb/d, 2010–2019 (`data/diesel_demand_monthly_synthetic.csv`, column `demand_kbd`). "It trends up like your TTF price — just difference it like you did." Demand is a *flow* with a strong winter seasonality (heating gasoil), driven by economic activity. Is its trend the same kind of trend as the price's?

### Objective

Decide, for a seasonal monthly series, between **detrend** (deterministic trend) and **difference** (stochastic trend) — and measure what goes wrong with the wrong choice.

### Minimum theory

| | Deterministic trend | Stochastic trend (unit root) |
|---|---|---|
| model | `y_t = a + b·t + stationary noise` | `y_t = y_{t-1} + drift + shock` |
| shocks | transitory | permanent |
| remedy | remove the line (**detrend**) | **difference** |
| ADF | does not reject with `'c'`, **rejects with `'ct'`** | rejects with neither |

- Seasonality must be handled **before** testing. A *deterministic* seasonal profile (same shape every year) is removed by subtracting the average deviation of each calendar month.
- **Over-differencing** a stationary series inflates its variance (for white noise, the variance of the difference is twice the variance) and destroys the level information.
- **Detrending a random walk** leaves a residual that still wanders.

### Assumptions

The trend is linear, the seasonal profile is stable across years, the sample covers complete years, and there is no structural break.

### Your task

Implement `trend_or_random_walk(y)` for a monthly `pd.Series` with a `DatetimeIndex`:

1. Drop missing values; `t = 0, 1, …, n-1`. Fit a linear trend on the raw series: `slope, intercept = np.polyfit(t, y, 1)`; `trend = intercept + slope * t`.
2. Seasonal profile: the mean of `y - trend` **by calendar month** (`groupby(y.index.month)`). Deseasonalised series: `y` minus the profile value of its month.
3. ADF p-values on the deseasonalised series with `regression='c'` and `regression='ct'` (`autolag="AIC"`).
4. `std_detrended` = std of (deseasonalised − trend); `std_differenced` = std of the first difference of the deseasonalised series (both pandas `.std()`).
5. `decision`: `"stationary"` if the `'c'` p-value < 0.05; otherwise `"detrend"` if the `'ct'` p-value < 0.05; otherwise `"difference"`.

Return a `dict` with keys `trend_per_year` (`slope * 12`), `seasonal_amplitude` (max − min of the profile), `adf_p_c`, `adf_p_ct`, `std_detrended`, `std_differenced`, `decision`.

Then answer the question in the **Explain** tab.
