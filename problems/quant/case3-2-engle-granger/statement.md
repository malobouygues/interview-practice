> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Coffee is independent of crude **by construction**.

### Context

Both crude prices are I(1) and their spread looks I(0) (step 3.1). The formal test of a long-run equilibrium between two series is the **Engle-Granger** procedure. It looks like "OLS, then ADF on the residuals" — but if you read the second step with ordinary ADF p-values you will find relationships that do not exist.

### Objective

Implement both steps by hand, compare the naive p-value with the correct Engle-Granger p-value, and interpret the results for WTI–Brent and coffee–Brent.

### Minimum theory

- **Step 1** — cointegrating regression in levels: `y_t = α + β·x_t + u_t` (OLS). `u_t` is the deviation from the candidate equilibrium.
- **Step 2** — unit-root test on the residuals `û_t`: an ADF regression **without** constant (`regression='n'`), since OLS residuals have mean zero.
- **H0: no cointegration** (the residuals have a unit root). **H1: cointegration** (the residuals are stationary).
- **Critical values.** β was *estimated* to make the residuals as small as possible, which makes them look more stationary than a series you merely observe. The ADF statistic must therefore be compared with **Engle-Granger (MacKinnon) critical values** — about −3.34 at 5 % for two variables with a constant — not with Dickey-Fuller ones.
- `statsmodels.tsa.stattools.coint(y, x, trend="c")` runs both steps and returns `(stat, pvalue, crit_values)` with `crit_values = [1 %, 5 %, 10 %]`.

### Assumptions

Both series are I(1); there is at most one cointegrating relation (two series); the relation is stable over the sample (no break — see Case 4).

### Your task

Implement `engle_granger(y, x)`:

1. Align `y` and `x`, drop `NaN`. Step 1: `sm.OLS(y, sm.add_constant(x)).fit()` → `alpha`, `beta`, residuals.
2. Step 2: `adfuller(residuals, regression="n", autolag="AIC")` → `adf_stat` and `naive_pvalue` (its p-value — *the wrong reference distribution*).
3. `coint(y, x, trend="c", autolag="aic")` → `eg_pvalue` and `eg_crit_5pct` (second critical value).
4. Return a `dict`: `alpha`, `beta`, `adf_stat`, `naive_pvalue`, `eg_pvalue`, `eg_crit_5pct`, `cointegrated` (`eg_pvalue < 0.05`).

Check in the output that `adf_stat` is the statistic `coint` uses: same number, different verdict.

Then answer the question in the **Explain** tab.
