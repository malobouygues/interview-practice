> **Synthetic data** — simulated with a fixed seed so that the concepts are visible. Not market observations.

### Context

Step 4 left you with an ADF p-value of 0.91 on the TTF level — which, by itself, proves nothing. The **KPSS** test flips the hypotheses. Reading the two together turns two weak statements into a usable diagnosis.

### Objective

Combine ADF and KPSS into one verdict, and know what to do in each of the four possible outcomes.

### Minimum theory

- **KPSS**: **H0 = the series is stationary** (around a level with `regression='c'`, around a linear trend with `'ct'`); **H1 = unit root**. Small p-value → reject stationarity.
- `statsmodels.tsa.stattools.kpss(x, regression=..., nlags="auto")` returns `(stat, pvalue, lags, crit)`. Its p-value is **interpolated in a table that only covers 0.01–0.10**: outside that range it returns the bound and emits an `InterpolationWarning` (`from statsmodels.tools.sm_exceptions import InterpolationWarning`).
- The joint reading (5 % level, same deterministic terms in both tests):

| ADF (H0: unit root) | KPSS (H0: stationary) | verdict | next step |
|---|---|---|---|
| rejects | does not reject | `"stationary"` | look at the chart and the stability of the variance |
| does not reject | rejects | `"unit root"` | check for breaks; difference if the analysis requires it; re-test the difference |
| rejects | rejects | `"conflict"` | re-test with `'ct'`, test sub-periods, look at the variance: misspecified trend, break, changing variance or long memory |
| does not reject | does not reject | `"inconclusive"` | not enough information (short sample, low power): rely on the economics and make results robust to both |

### Assumptions

The table gives *plausible readings*, not an identification of the true process. Both tests are sensitive to breaks and to the deterministic terms you choose.

### Your task

Implement `stationarity_verdict(x, regression="c", alpha=0.05)`:

- Drop missing values. Run `adfuller(x, regression=regression, autolag="AIC")` and `kpss(x, regression=regression, nlags="auto")`, silencing the `InterpolationWarning` of KPSS (e.g. with `warnings.catch_warnings()`).
- Return a `dict`: `adf_pvalue`, `kpss_pvalue` (floats), `adf_rejects`, `kpss_rejects` (bools, p < `alpha`), `verdict` — one of `"stationary"`, `"unit root"`, `"conflict"`, `"inconclusive"` (exact strings, from the table).

Then answer the question in the **Explain** tab.
