### A. Reasoning — why selection is not a beauty contest on R²

Every regressor you add raises R², so a model chosen on R² keeps growing until it fits noise. A defensible model is the simplest one whose variables have a mechanism and add information that survives a penalty for complexity — and whose coefficients stay interpretable. Comparing a handful of reasonable specifications, on the same sample, with several criteria, makes that choice explicit.

### B. Theory

- R² is non-decreasing in the number of regressors. Adjusted R² = 1 − (1 − R²)(n − 1)/(n − k − 1).
- AIC = −2 log L + 2k; BIC = −2 log L + k log n: lower is better; BIC penalises extra parameters more when n is large.
- Multicollinearity inflates standard errors by ≈ √(1/(1 − ρ²)) for two regressors with correlation ρ; coefficients become unstable and can change sign.
- Overfitting: in-sample improvements from variables without a mechanism usually vanish out of sample.
- Same sample for every model: information criteria are only comparable on identical observations.

### C. Implementation

{{code}}

### D. Interpretation (exports-allowed regime, 911 days)

| specification | R² | adj. R² | AIC | BIC | Brent β (SE) | added coef (p) |
|---|---|---|---|---|---|---|
| brent | 0.7689 | 0.7686 | −6101.4 | **−6091.7** | 0.889 (0.016) | — |
| brent + dubai | **0.7695** | **0.7690** | **−6101.9** | −6087.4 | 0.964 (**0.050**) | −0.074 (0.11) |
| brent + coffee | 0.7689 | 0.7684 | −6099.5 | −6085.0 | 0.889 (0.016) | 0.005 (0.77) |
| brent + brent_lag1 | 0.7691 | 0.7686 | −6100.2 | −6085.8 | 0.889 (0.016) | −0.015 (0.35) |

- Dubai: R² +0.0006, AIC slightly better, but BIC worse, Brent's SE ×3, and a **negative**, insignificant Dubai coefficient — Brent and Dubai returns correlate at 0.95 (variance inflation ≈ 10). The model cannot separate them; Dubai brings no new information about WTI.
- Coffee and lagged Brent: no mechanism, no evidence.

**Choice: WTI returns on Brent returns only.**

### E. Decision

Use the parsimonious specification; record why each alternative was rejected. Re-run the comparison on the other regime (second test) before claiming the choice is general.

### F. Pitfalls and limits

- Choosing the model with the highest R².
- Comparing AIC/BIC across different samples (e.g. after a lag removes rows).
- Interpreting each coefficient of a collinear pair separately.
- Testing many variables and keeping the "significant" ones: some will be significant by chance.

### G. Interview defence

> **Q: "Why not add Dubai to your WTI model? The R² goes up."**
>
> **A:** R² always goes up when you add a variable. Dubai's returns are 95 % correlated with Brent's, so it carries almost no new information: R² moves from 0.7689 to 0.7695, Brent's standard error triples, and Dubai comes out with a negative, insignificant coefficient that has no economic meaning — that's multicollinearity. BIC prefers the Brent-only model, AIC is indifferent, and the economics say Brent is the arbitrage benchmark. So I keep the simple model, estimated on the same sample as every alternative I considered.
