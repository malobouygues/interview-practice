> **Synthetic data** — simulated with fixed seeds; coffee is independent of crude **by construction**.

### Context

Both prices are I(1) and their log spread looks I(0) (step 4.4). The formal test of a long-run equilibrium between two series is the **Engle-Granger** procedure. It looks like "OLS, then ADF on the residuals" — but read with ordinary ADF p-values it finds relationships that do not exist.

### Objective

Implement both steps by hand, compare the naive p-value with the correct Engle-Granger p-value, and interpret WTI–Brent and coffee–Brent (exports-allowed regime, from 2016-07-01).

### Minimum theory

- **Economic intuition**: two prices tied by arbitrage drift together; their gap is pulled back to a stable value.
- **Step 1**: `y_t = α + β x_t + u_t` (OLS in levels). `u_t` is the deviation from the candidate equilibrium.
- **Step 2**: ADF on `û_t` **without** constant (`regression='n'`: OLS residuals have mean zero).
- **H0: no cointegration** (residuals have a unit root). **H1: cointegration**.
- **Critical values**: β was *estimated* to make the residuals small, so they look more stationary than an observed series; compare the statistic with **Engle-Granger (MacKinnon)** critical values — about −3.34 at 5 % for two variables with a constant.
- `statsmodels.tsa.stattools.coint(y, x, trend="c")` returns `(stat, pvalue, crit_values)` with `crit_values = [1 %, 5 %, 10 %]`.

### Assumptions

Both series I(1); at most one relation; the relation is stable over the sample (tested in 4.9–4.10).

### Your task

Implement `engle_granger(y, x)`:

1. Align, drop `NaN`; Step 1 with `sm.OLS(y, sm.add_constant(x))` → `alpha`, `beta`, residuals.
2. Step 2: `adfuller(residuals, regression="n", autolag="AIC")` → `adf_stat`, `naive_pvalue`.
3. `coint(y, x, trend="c", autolag="aic")` → `eg_pvalue`, `eg_crit_5pct` (second critical value).
4. Return `alpha`, `beta`, `adf_stat`, `naive_pvalue`, `eg_pvalue`, `eg_crit_5pct`, `cointegrated` (`eg_pvalue < 0.05`).

Check in the output that `adf_stat` is the statistic `coint` uses: same number, different verdict. Answer in the **Explain** tab.
