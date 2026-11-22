### A. Reasoning — why an ECM rather than a model in differences

Engle-Granger told you an equilibrium exists. A regression in differences (Case 2) captures the daily co-movement but forgets where the levels are — it cannot see that WTI is "too cheap" today. The ECM adds exactly that missing piece, the lagged deviation from equilibrium, and its coefficient answers the question a trader actually asks: *how fast does a gap close?*

### B. Theory

- Δy_t = c + α·ECT_{t−1} + γ·Δx_t + e_t, with ECT = y − a − βx from the long-run regression.
- **Long run (β)**: the equilibrium. **Short run (γ)**: the same-day pass-through. **Adjustment (α)**: the pull back towards equilibrium.
- α < 0 is required: if y is above its equilibrium (ECT > 0), the next Δy is pushed down. α = 0 → no correction (no cointegration); α < −1 → overshooting.
- After k periods without new shocks, a deviation is multiplied by (1 + α)^k → half-life k* = ln(0.5)/ln(1 + α).
- Engle-Granger representation theorem: cointegrated series admit an error correction form — and an ECM on non-cointegrated series regresses a stationary Δy on a non-stationary ECT, i.e. nonsense.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| | β (long run) | γ (short run) | α | t(α) | half-life |
|---|---|---|---|---|---|
| WTI ~ Brent | 0.979 | 0.888 | −0.115 | −7.7 | **5.7 business days** |
| simulated (true α = −0.30, γ = 0.50, β = 1) | ≈ 1.00 | ≈ 0.50 | ≈ −0.30 | | ≈ 2 periods |
| coffee ~ Brent (not cointegrated) | 1.051 | 0.028 | −0.006 | −1.6 | 118 — meaningless |

- When Brent moves 1 % today, WTI moves 0.89 % today; the remaining gap with the long-run relation (elasticity 0.98) is then closed at **11.5 % per day**: half of any deviation has gone in about 6 business days.
- The August 2017 WTI-specific shock shows it: the log spread jumps from ≈ 0.08 to ≈ 0.12 and is back near its average within roughly three weeks.
- The simulated pair recovers its known coefficients — the estimator works when the model is right.
- For coffee, α is indistinguishable from zero and the "half-life" is an artefact: there is no equilibrium to return to.

### E. Decision

- WTI–Brent: the ECM is a coherent description: a deviation of the spread from its equilibrium is expected to shrink by about half in a week, *if* the relationship is stable — which Case 4 questions.
- Only estimate and interpret an ECM after a cointegration test has rejected H0.

### F. Limitations and pitfalls

- Interpreting an ECM on a non-cointegrated pair (the coffee row).
- Mis-aligning the ECT: it must be **lagged** (yesterday's deviation explains today's change); using ECT_t would put the answer on the right-hand side.
- Two-step estimation treats β as known; with a short sample its estimation error matters.
- A single equation cannot cleanly say which market does the adjusting when the same-day move of the other is on the right-hand side.
- The half-life assumes a constant α: it changes if the regime changes (Case 4).

### G. Interview defence

> **Q: "What does the error-correction coefficient tell you, and why must it be negative?"**
>
> **A:** It's the speed of adjustment: the share of yesterday's deviation from the long-run relation that is closed today. For WTI on Brent it's about −0.115 with a t-stat near −8, so roughly 11.5 % of a gap closes per day — a half-life of about six business days. It has to be negative because it's a pull back: if WTI is above its equilibrium relative to Brent, the next move has to be down. The ECM also separates the short run — WTI follows 89 % of a Brent move on the same day — from the long run, where the elasticity is about 0.98. And it only makes sense because the pair is cointegrated; on coffee and Brent it gives a meaningless 118-day half-life.
