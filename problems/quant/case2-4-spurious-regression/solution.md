### A. Reasoning — why compare levels with differences

You cannot tell a real relationship from a spurious one by looking at the levels regression: both give large t-statistics. What separates them is whether the link survives when you remove the trends. Differencing is the most direct way to remove stochastic trends, and in differences the usual OLS inference is valid.

### B. Theory

- **Spurious regression**: for independent I(1) series, β̂ does not converge to 0, R² does not converge to 0, and the t-stat diverges with the sample size. The residual is I(1). The regression fits the sample's common drift.
- In first differences the variables are stationary, the t-stat is valid, and independent series show no relationship.
- Three outcomes: significant in differences → genuine co-movement; significant in levels only → spurious; neither → no evidence of any link.
- Differencing throws away the long-run (level) information. If the levels share an equilibrium (cointegration), the right model keeps it — that is the error correction model of Case 3.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Pair | R² levels | t levels | R² differences | t differences | verdict |
|---|---|---|---|---|---|
| WTI ~ Brent | 0.988 | 271 | 0.770 | 55.2 | co-moving |
| coffee ~ Brent | 0.592 | 36.3 | 0.001 | 0.80 | spurious |
| two independent random walks | 0.071 | −8.3 | 0.0005 | −0.68 | spurious |
| two independent white noises | 0.0007 | 0.81 | 0.0006 | 0.75 | unrelated |

**Monte Carlo** (test code): about **89 %** of 200 independent random-walk pairs give |t| > 1.96 in levels, where a valid 5 % test would give 5 %. The coffee result is not bad luck — it is what level regressions on I(1) series do.

### E. Decision

- Coffee–Brent: no relationship; report nothing in levels.
- Brent–WTI: genuine co-movement. Next question — do the levels share an equilibrium? → Engle-Granger (Case 3), which tests whether the levels residual is stationary with the correct critical values.
- If no cointegration is found, model in differences only.

### F. Limitations and pitfalls

- The verdict assumes both series are I(1); for stationary series a level regression is fine.
- "Co-moving" in differences says nothing about the long run; "no co-movement" in differences with a stationary level residual would be unusual but possible (very noisy short-run).
- The simple 1.96 threshold on the levels t-stat is itself invalid inference — it is used here only to *describe* how the naive analyst would be fooled.

### G. Interview defence

> **Q: "What's a spurious regression and how would you detect one?"**
>
> **A:** It's what you get when you regress one non-stationary series on another unrelated one: high R², huge t-stats, no relationship. The residual is non-stationary — the line just fits the drift the two series shared over the sample — and the t-stat doesn't follow a t-distribution, so in simulations about nine pairs of independent random walks in ten look significant. I detect it by re-running in differences: coffee on Brent goes from t = 36 in levels to 0.8 in differences. For a pair that survives in differences, like WTI–Brent, I then test cointegration — a stationary residual in levels — before I'd claim a long-run relationship.
