### A. Reasoning — why a regression, and why in returns first

The hypothesis is about how WTI responds to Brent. A regression gives the size of that response with a measure of uncertainty — but its uncertainty measures are only valid for stationary data with independent errors. Returns satisfy that reasonably; price levels do not. Running both shows which numbers you are allowed to quote.

### B. Theory

- β̂ = cov(x, y)/var(x); in a bivariate regression R² = r².
- SE(β̂) = σ̂ / √(Σ(x − x̄)²); t = β̂/SE; p-value from the t distribution; CI = β̂ ± t₀.₉₇₅ SE.
- Assumptions behind SE, t, p, CI: stationarity, no autocorrelation, constant variance (and normality in small samples).
- Statistical significance answers "is it distinguishable from 0 in this sample?" — not "is it large, useful or stable?".

### C. Implementation

{{code}}

### D. Interpretation (this dataset, from July 2016)

| regression | β | SE | t | 95 % CI | R² |
|---|---|---|---|---|---|
| WTI on Brent, **returns** | 0.890 | 0.016 | 55 | 0.858 – 0.921 | 0.77 |
| WTI on Brent, levels | 0.979 | 0.004 | 271 | 0.972 – 0.987 | 0.99 |
| coffee on Brent, returns | 0.025 | 0.031 | 0.8 | −0.036 – 0.087 | 0.001 |
| coffee on Brent, levels | 1.051 | 0.029 | 36 | 0.994 – 1.107 | 0.59 |

- In returns: WTI absorbs about 0.89 % of a 1 % Brent move on the same day, precisely estimated.
- In levels: an elasticity of about 0.98 — a candidate long-run relation — but its SE and t are not valid (persistent residuals). The coffee rows make the point: "t = 36" in levels for a relationship that does not exist; nothing in returns.

### E. Decision

Quote the returns regression with its CI; treat the levels regression as a candidate equilibrium to be tested with cointegration methods (4.7), not with its t-statistic.

### F. Pitfalls and limits

- Reading R² or t in levels as evidence.
- Confusing the CI of β with a range for tomorrow's WTI move.
- β depends on which variable is on the left (Brent on WTI gives about 1.01 in levels, not 1/0.98).
- "Significant" with n ≈ 900 can still mean economically negligible.

### G. Interview defence

> **Q: "Your regression of WTI on Brent has a t-stat of 271. Isn't that conclusive?"**
>
> **A:** Not in levels: both prices are non-stationary and the residuals are very persistent, so the standard error is far too small — I get t = 36 for coffee on Brent, which has no link at all. The inference I trust is in returns: β ≈ 0.89 with a 95 % confidence interval of roughly 0.86 to 0.92, so WTI moves about 0.9 % on the day for a 1 % Brent move. The levels regression gives me a candidate long-run elasticity near one, which I then test properly with Engle-Granger.
