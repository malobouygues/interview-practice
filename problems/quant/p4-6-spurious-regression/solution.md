### A. Reasoning — why compare levels with differences

You cannot tell a real relationship from a spurious one by looking at a levels regression: both produce large t-statistics. What separates them is whether the link survives once the trends are removed. Differencing removes stochastic trends, and in differences ordinary inference is valid.

### B. Theory

- Spurious regression (Granger–Newbold): for independent I(1) series, β̂ does not converge to 0, R² stays large, t diverges with n; the residual is I(1).
- In differences the variables are I(0): valid t-tests; independent series show nothing.
- Survives in differences → real co-movement; long-run equilibrium additionally requires a stationary levels residual (cointegration).
- Differencing discards the long run: if the levels are cointegrated, the right model keeps them (ECM, 4.8).

### C. Implementation

{{code}}

### D. Interpretation (from July 2016)

| pair | R² levels | t levels | R² differences | t differences | verdict |
|---|---|---|---|---|---|
| WTI ~ Brent | 0.988 | 271 | 0.770 | 55.2 | co-moving |
| coffee ~ Brent | 0.592 | 36.3 | 0.001 | 0.80 | **spurious** |
| independent random walks | 0.071 | −8.3 | 0.0005 | −0.68 | spurious |
| independent white noises | 0.001 | 0.81 | 0.001 | 0.75 | unrelated |

Monte Carlo: about **89 %** of independent random-walk pairs are "significant" in levels.

### E. Decision

Reject the "oil drives coffee" claim; the coffee–Brent levels regression is spurious. WTI–Brent co-moves daily; whether their levels share an equilibrium is tested next (Engle-Granger).

### F. Pitfalls and limits

- High R² or t in levels taken as evidence.
- The verdict assumes I(1) inputs (for stationary series a levels regression is fine).
- The 1.96 threshold on the levels t-stat describes how a naive analyst is fooled; it is not valid inference.
- Correlation, even in changes, is not causality.

### G. Interview defence

> **Q: "What's a spurious regression and how would you spot one?"**
>
> **A:** It's what you get when you regress one non-stationary series on an unrelated one: high R², huge t-stats, no relationship. The line just fits the drift the two series shared over the sample, the residual is non-stationary, and the t-statistic doesn't follow its usual distribution — in simulations about nine pairs of independent random walks in ten look significant. I re-run in differences: coffee on Brent goes from t = 36 in levels to 0.8 in differences, while WTI on Brent stays at 55. For a pair that survives, I then test cointegration before claiming any long-run relationship.
