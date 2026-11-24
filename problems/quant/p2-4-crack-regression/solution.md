### A. Reasoning — the size of the effect, then how sure we are, then whether the shape is right

A regression answers three different questions that are often confused: *how big* is the effect (the coefficient, in $/bbl per unit), *how precisely* do we know it (the standard error — which depends on assumptions about the errors), and *is the model the right shape* (the residuals). Robust standard errors only address the second.

### B. Theory (PDF A08-C regression, A10-C residual diagnostics)

- Coefficients are unbiased under exogeneity; their usual SEs additionally assume **homoskedastic** and **uncorrelated** errors.
- **White's test** (H0: constant variance) — general form: squared residuals on regressors, squares and cross-products; LM = n·R² ~ χ².
- **HC3** (a heteroskedasticity-consistent covariance with a small-sample correction) replaces the SE formula; it leaves the point estimates untouched.
- **What remains**: a curved relationship, an omitted driver or autocorrelated errors are still there. Durbin-Watson ≈ 2 means no first-order autocorrelation; well below 2, positive autocorrelation.
- **VIF** = 1 / (1 − R²ⱼ) of regressor j on the others.

### C. Implementation

Two `sm.OLS(y, X).fit(...)` calls on the same data (default and `cov_type="HC3"`); `het_white(resid, X)` with the constant included in `X`; a loop over `X.columns` for VIF; `pd.cut` + `groupby(..., observed=False)` for residuals by regime.

### D. Interpretation (this dataset, 78 months)

| | coef | SE | p | SE (HC3) | p (HC3) |
|---|---|---|---|---|---|
| stocks vs 5y (%) | **−1.093** | 0.039 | < 0.001 | 0.059 | < 0.001 |
| outages (kb/d) | **0.0028** | 0.0014 | **0.046** | 0.0022 | **0.21** |
| utilisation (%) | 0.210 | 0.122 | 0.089 | 0.125 | 0.093 |

R² **0.93**; White LM **26.6**, p **0.0016**; Durbin-Watson **1.36**; VIF 1.0–1.2.
Residuals by stocks: below −15 %: mean **+0.99**, std **4.95** (11 months); −15 % to −5 %: mean **−1.42**, std 2.71; −5 % to +5 %: mean 0.12, std **1.67**; above +5 %: 0.75, 2.13.

- A 20 % stock deficit (2022) ≈ **+22 $/bbl** of crack.
- The outage effect looks significant with conventional SEs and disappears with HC3: it rests on a few high-leverage months.
- The residual means are not zero by regime: positive in the tightest months, negative just above — the straight line under-predicts scarcity. That is a shape problem.

### E. Decision

To the trader: *“Yes, the widening is consistent with a physical stock deficit — about a dollar of crack per point of deficit, and that holds with robust inference. Refinery outages add something, but the data don't establish it robustly. And the relationship is steeper when stocks are very low than the straight line says, so don't extrapolate it linearly into a deeper deficit.”*

### F. Pitfalls and limits

- Reporting HC3 p-values as if they validated the model: they don't touch the curvature or the autocorrelation (DW 1.36 → consider HAC errors, P3, or a dynamic specification).
- 78 overlapping-in-time monthly observations from one cycle: the 2022 regime drives the fit.
- Stocks and the crack are jointly determined (high cracks attract imports, which rebuild stocks): the coefficient is an association, not a pure causal effect.
- White's test also reacts to misspecification (the squares of the regressors capture curvature): a rejection is a reason to look, not only to switch SEs.

### G. Interview defence

*“Your t-stat was 2.0, with robust errors it's 1.3 — which one do you report?”* — The robust one, and I'd say why: the residual variance is three times larger in tight months, so the conventional formula understates the uncertainty. But I'd add that robust errors only make the *inference* honest; if the residuals show a pattern, the model itself needs fixing before anyone sizes a position on it.
