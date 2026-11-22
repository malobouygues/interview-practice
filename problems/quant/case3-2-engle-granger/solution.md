### A. Reasoning — why Engle-Granger, and why the details matter

The economic hypothesis is an equilibrium in **levels**: log WTI ≈ α + β·log Brent, with deviations that die out. Correlations and differenced regressions cannot test it (differences throw the levels away). Engle-Granger tests it directly: estimate the relation, then ask whether the deviations from it are stationary. The trap is in step 2 — and the coffee pair falls straight into it.

### B. Theory

- Cointegration: x, y ∼ I(1) and u = y − α − βx ∼ I(0). Economically: one common stochastic trend, and a force (arbitrage) that closes gaps.
- **H0: no cointegration** = û has a unit root. Rejecting H0 is the evidence for an equilibrium.
- OLS picks β to minimise the variance of û. Even for unrelated random walks, this search makes û look more mean-reverting than any given series would. The Dickey-Fuller distribution ignores this, so its critical values are too lenient. Engle-Granger critical values (MacKinnon) account for the estimation: about −3.34 at 5 % with two variables and a constant, against ≈ −1.94 for an ADF without constant.
- The statistic is the same ADF t-stat; only the reference distribution changes.
- Limits: one relation only, results depend on which series is on the left, low power, sensitive to breaks.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Regression | β | ADF stat on residuals | naive p | EG p | EG 5 % crit | cointegrated |
|---|---|---|---|---|---|---|
| WTI ~ Brent | 0.979 | −7.44 | < 0.001 | < 0.001 | −3.34 | yes |
| Brent ~ WTI | 1.009 | −7.48 | < 0.001 | < 0.001 | −3.34 | yes |
| coffee ~ Brent | 1.051 | −2.05 | **0.038** | **0.501** | −3.34 | **no** |
| Brent ~ coffee | 0.563 | −2.69 | 0.007 | 0.203 | −3.34 | no |

- **WTI–Brent**: a statistic of −7.4 against a critical value of −3.34 — overwhelming evidence of an equilibrium, with an elasticity close to 1 (consistent with the stationary spread of step 3.1).
- **Coffee–Brent**: with ordinary ADF tables you would "confirm" a link at the 5 % level. With the correct distribution, p = 0.50: no evidence at all. This is the spurious regression of Case 2 coming back through a wrongly-read residual test.
- **Ordering**: brent ~ coffee gives a different statistic and p-value — Engle-Granger is not symmetric. For a genuinely cointegrated pair (WTI/Brent) both orderings agree.

### E. Decision

- WTI–Brent: cointegrated → model the relationship with an error correction model (step 3.3), or work directly on the spread since β ≈ 1.
- Coffee–Brent: not cointegrated → no level relationship; at most a relationship in differences (and Case 2 found none).
- When the two orderings disagree, report both and be sceptical.

### F. Limitations and pitfalls

- Reading the residual ADF with standard tables (the naive p-value).
- Concluding cointegration on a sample containing an obvious break (Case 4), or from a high level correlation.
- Engle-Granger finds at most one relation and has low power: a non-rejection on a short sample is weak evidence of "no equilibrium".
- No mechanism, no cointegration claim: the statistical result must match an economic story (arbitrage, substitution, transport).

### G. Interview defence

> **Q: "Engle-Granger is just ADF on regression residuals — why can't you use the ADF p-value?"**
>
> **A:** Because the residuals aren't an observed series: OLS chose β precisely to make them as small and stationary-looking as possible. Under the null of no cointegration that search makes the ADF statistic more negative than the Dickey-Fuller distribution expects, so the standard critical values reject far too often. Engle-Granger uses its own critical values — about −3.34 at 5 % for two series — which account for the estimation. On my data, coffee against Brent has a residual ADF stat of −2.05: the naive p-value is 0.038, the correct one is 0.50. WTI against Brent is −7.4, so that one is cointegrated whichever way you look at it.
