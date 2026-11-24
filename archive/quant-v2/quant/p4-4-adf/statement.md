> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

Step 4.2 showed a levels regression with an invalid t-statistic. Before any regression in levels, the question is: **are the series stationary?** The standard tool is the Augmented Dickey-Fuller test — and the standard mistake is to read its p-value as "stationary / not stationary". In this curriculum, ADF is the formal unit-root test.

### Objective

Wrap ADF in a function that reports what you need, apply it to the crude series and to controlled examples, and decide whether levels can be regressed.

### Minimum theory

- **Random walk**: `y_t = y_{t−1} + ε_t` — shocks are permanent, the variance grows with time, there is no level to return to. It is the simplest **unit-root** process; most prices are close to it. **I(1)**: stationary after one difference; **I(0)**: stationary in levels.
- ADF regression: `Δy_t = [constant] + [trend·t] + γ·y_{t−1} + (lagged Δy) + e_t`.
- **H0: γ = 0 (unit root)**; **H1: γ < 0** (stationary). The statistic (t of γ) is compared with **Dickey-Fuller** critical values. More negative = stronger rejection.
- **Deterministic terms** (`regression=`): `'n'` (series centred on 0: returns, residuals), `'c'` (a level: spreads), `'ct'` (a visible deterministic trend). Omitting a real trend makes a trend-stationary series look like a unit root; useless terms cost power.
- **Lags**: lagged differences absorb short-term dependence; `autolag="AIC"` chooses them.
- `adfuller(x, regression=..., autolag="AIC")` returns `(stat, pvalue, usedlag, nobs, critical_values, icbest)`.

### Assumptions

Correct deterministic terms, enough lags, and no structural break in the sample. Power depends on the **time span**, not the number of points.

### Your task

Implement `adf_report(x, regression="c")`: drop `NaN`, run `adfuller(x, regression=regression, autolag="AIC")`, return a `dict` with `stat`, `pvalue`, `lags` (int), `nobs` (int), `crit_5pct` (the 5 % critical value), `reject_unit_root` (`pvalue < 0.05`).

The test code applies it to log Brent, log WTI, their returns, the log spread, and to simulated examples (the PDF's random walk / trend-stationary pair, a short sample, a level shift), and shows the effect of the lag choice. Answer in the **Explain** tab.
