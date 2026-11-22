### A. Reasoning — why Engle-Granger, and why the details matter

The hypothesis of 4.1 is an equilibrium in **levels**: log WTI ≈ α + β·log Brent, with deviations that die out. Differenced regressions cannot test it (they discard levels), and a levels regression's t-statistic is invalid (4.6). Engle-Granger tests it directly — estimate the relation, then ask whether the deviations are stationary — but its second step needs its own critical values.

### B. Theory

- Cointegration: x, y ∼ I(1) and y − α − βx ∼ I(0): one common stochastic trend plus a force (arbitrage) closing gaps.
- H0: no cointegration. Rejecting H0 is the evidence for an equilibrium.
- OLS chooses β to minimise the residual variance → residuals look more mean-reverting than any given series; Dickey-Fuller critical values (≈ −1.94 with no constant) are too lenient; Engle-Granger ones (≈ −3.34 at 5 %, two variables) account for the estimation.
- Same statistic, different reference distribution.
- Limits: one relation, normalisation-dependent, low power, sensitive to breaks.

### C. Implementation

{{code}}

### D. Interpretation (from July 2016)

| regression | β | ADF stat on residuals | naive p | EG p | EG 5 % crit | cointegrated |
|---|---|---|---|---|---|---|
| WTI ~ Brent | 0.979 | −7.44 | < 0.001 | < 0.001 | −3.34 | yes |
| Brent ~ WTI | 1.009 | −7.48 | < 0.001 | < 0.001 | −3.34 | yes |
| coffee ~ Brent | 1.051 | −2.05 | **0.038** | **0.501** | −3.34 | **no** |
| Brent ~ coffee | 0.563 | −2.69 | 0.007 | 0.203 | −3.34 | no |

- WTI–Brent: overwhelming evidence of an equilibrium with an elasticity close to 1 (consistent with the stationary spread).
- Coffee–Brent: the naive reading would "confirm" a link at 5 %; the correct p-value is 0.50.
- Orderings disagree for coffee, agree for WTI/Brent.

### E. Decision

Model WTI–Brent with an error correction model (4.8), or work directly on the spread since β ≈ 1. No level relationship for coffee.

### F. Pitfalls and limits

- Reading the residual ADF with standard tables.
- Concluding cointegration on a sample with an obvious break (4.9), or from a high level correlation.
- A non-rejection on a short sample is weak evidence of "no equilibrium".
- No mechanism, no cointegration claim.

### G. Interview defence

> **Q: "Engle-Granger is just ADF on regression residuals — why can't you use the ADF p-value?"**
>
> **A:** Because the residuals aren't an observed series: OLS picked β to make them as small and stationary-looking as possible, so under the null the ADF statistic is pushed to the left and Dickey-Fuller tables reject far too often. Engle-Granger uses its own critical values — about −3.34 at 5 % for two series. In my data coffee on Brent has a residual statistic of −2.05: naive p-value 0.038, correct p-value 0.50. WTI on Brent is −7.4, so that pair is cointegrated however you look at it — which matches the arbitrage story.
