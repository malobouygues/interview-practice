### A. Reasoning — why establish the order first

Cointegration is a statement about non-stationary series sharing a stochastic trend. If one of them is already stationary there is nothing to share; if one is I(2) and the other I(1) no linear combination can be stationary. So "are both I(1)?" is a precondition, and testing it explicitly also forces you to look at the spread — which turns out to be the most informative series of all.

### B. Theory

- I(d): d differences to stationarity. Prices are typically I(1); returns and stable spreads I(0).
- Cointegration of x and y (both I(1)): ∃ β such that y − βx is I(0). The pair has **one** common stochastic trend.
- A spread with an imposed coefficient of 1 being I(0) is cointegration with β = 1. Estimating β (next step) tests whether 1 is right.
- The loop inherits the limits of ADF + KPSS: power, breaks, specification.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Series | verdicts | order |
|---|---|---|
| log Brent | unit root → stationary | I(1) |
| log WTI | unit root → stationary | I(1) |
| log spread log(Brent) − log(WTI) | stationary | **I(0)** |
| Brent log returns | stationary | I(0) |
| twice-accumulated noise | unit root → unit root → stationary | I(2) |
| log TTF | unit root → stationary | I(1) |

Each crude price wanders without anchor, but **the gap between them does not**: the WTI discount fluctuates around ≈ 0.059 log points (≈ 6 %) and keeps returning to it. Two I(1) series with an I(0) combination — the arbitrage of 2.1, seen in the data.

### E. Decision

- Both prices I(1) → testing cointegration is meaningful → Engle-Granger (step 3.2).
- The spread already looks stationary → strong prior for cointegration with β ≈ 1; the formal test with an estimated β follows.
- A series found I(2) → look for a break before accepting it.

### F. Limitations and pitfalls

- Testing cointegration between an I(0) and an I(1) series, or without checking orders at all.
- Concluding I(1) on a stationary series with a break (step 1.4) — and then "finding" or "missing" cointegration for the wrong reason.
- Mechanical differencing: the loop is a diagnostic, the decision still needs the chart and the economics.

### G. Interview defence

> **Q: "Why do you check the order of integration before a cointegration test?"**
>
> **A:** Because cointegration means two non-stationary series share the same stochastic trend, so that a combination of them is stationary. That only makes sense if both are I(1). Here log Brent and log WTI are each I(1) — ADF doesn't reject, KPSS rejects, and the differences are stationary — while the log spread between them is I(0): it fluctuates around a 6 % WTI discount. That's already strong evidence of cointegration with a coefficient close to one, which I then test formally with Engle-Granger.
