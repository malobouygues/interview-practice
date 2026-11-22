### A. Reasoning — why a regression, and why twice

Case 3 will test whether WTI and Brent share an equilibrium; its first step *is* this regression in levels. Before using it as a tool you need to know what each number means, and which numbers become unreliable when the variables are non-stationary. Running the same regression in returns gives the short-run relationship, where the standard OLS assumptions are much closer to holding.

### B. Theory

- OLS: β̂ = cov(x, y)/var(x), α̂ = ȳ − β̂x̄. In a bivariate regression R² = r².
- Logs on logs: β is an elasticity (% for %). Returns on returns: β is the average daily pass-through.
- The residual is everything the line misses. In levels it is the deviation from the fitted *long-run* relation; for WTI–Brent, ≈ the log spread minus its average.
- The usual standard errors assume stationary regressors and serially independent errors. With I(1) levels and persistent residuals, the t-stat does not follow a t-distribution and is grossly inflated.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Regression | α | β | t(β) | R² | resid std |
|---|---|---|---|---|---|
| log WTI on log Brent (levels) | 0.027 | 0.979 | 271 | 0.988 | 0.018 |
| Δlog WTI on Δlog Brent (returns) | 0.000 | 0.890 | 55 | 0.770 | 0.0085 |
| log coffee on log Brent (levels) | 0.745 | 1.051 | 36 | 0.592 | 0.146 |

- **Levels**: WTI tracks Brent almost one-for-one in the long run (elasticity 0.98). The residual (std ≈ 1.8 %) is the WTI discount relative to its usual level.
- **Returns**: on a given day WTI absorbs ≈ 89 % of a Brent move — less than one-for-one in the short run, nearly one-for-one in the long run. This gap between short- and long-run responses is exactly what an error correction model formalises (Case 3).
- **Coffee**: t = 36, R² = 0.59, for a relationship that does not exist. The level t-statistic cannot be trusted — next step.

### E. Decision

- Use the returns regression for the short-run co-movement (hedge ratios on daily moves).
- Treat the levels regression as a candidate long-run relation **only** after checking that its residual is stationary (Case 3); never read its t-stat or R² as evidence.

### F. Limitations and pitfalls

- Reading a high R² or t-stat in levels as proof of a relationship (the coffee row).
- β depends on which variable is on the left: regressing Brent on WTI gives ≈ 1.01, not 1/0.98.
- A regression coefficient is an association, not a causal effect.
- Outliers move OLS; the August 2017 WTI shock is one such day.

### G. Interview defence

> **Q: "Your regression of WTI on Brent has a t-stat of 271. Isn't that conclusive?"**
>
> **A:** Not in levels. Both prices are non-stationary, and the residuals are very persistent, so the OLS standard errors are wrong and the t-stat is massively inflated — I get t = 36 for coffee on Brent, which has no link at all. What the levels regression gives me is a candidate long-run relation: an elasticity of about 0.98. Whether it's a real equilibrium depends on whether the residual is stationary, which is the cointegration test. The returns regression is the one with valid inference: WTI moves about 0.89 % for a 1 % Brent move on a given day.
