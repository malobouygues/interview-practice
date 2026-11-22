> **Synthetic data** — simulated with fixed seeds; coffee is independent of crude by construction.

### Context

The desk wants one simple model of WTI's daily moves. Colleagues suggest adding regressors: Dubai ("another benchmark, more information"), coffee ("why not, it's significant in levels"), yesterday's Brent move ("maybe WTI lags"). More variables always raise the R² — the question is whether they genuinely improve the explanation.

### Objective

Estimate four reasonable specifications on the same sample and choose one with explicit criteria.

### Minimum theory

| criterion | what it does |
|---|---|
| economic justification | is there a mechanism and an expected sign? |
| R² | never decreases when you add a regressor — useless for selection on its own |
| adjusted R², AIC, BIC | penalise extra parameters; BIC (penalty ∝ log n) favours smaller models more than AIC |
| t / p of the added variable | does it add information given the others? |
| stability of the other coefficients | does the added variable inflate their standard errors (multicollinearity)? |

**Multicollinearity**: two highly correlated regressors share the same information; the model cannot tell them apart, so their coefficients become imprecise and can take implausible signs. Rule of thumb: variance inflation ≈ 1/(1 − ρ²).

All specifications must be estimated on **the same observations**.

### Assumptions

Daily log returns of the exports-allowed regime (from 2016-07-01); returns are stationary, so OLS inference is reasonable.

### Your task

Implement `compare_specifications(returns)` for a `DataFrame` of daily log returns with columns `wti`, `brent`, `dubai`, `coffee`:

1. Add `brent_lag1 = brent.shift(1)` and drop every row with a missing value (one common sample).
2. Regress `wti` (with a constant) on: `["brent"]`, `["brent", "dubai"]`, `["brent", "coffee"]`, `["brent", "brent_lag1"]`, named `"brent"`, `"brent + dubai"`, `"brent + coffee"`, `"brent + brent_lag1"`.
3. For each, record `n`, `r2`, `adj_r2`, `aic`, `bic`, `brent_beta`, `brent_se`, and for the added variable `added_coef` and `added_pvalue` (`NaN` for the Brent-only model).

Return a `DataFrame` indexed by `specification`, in that order. Answer in the **Explain** tab.
