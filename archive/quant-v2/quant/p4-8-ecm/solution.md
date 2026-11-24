### A. Reasoning — why an ECM rather than a model in differences

Engle-Granger says an equilibrium exists. A regression in differences captures daily co-movement but cannot see that WTI is "too cheap" today. The ECM adds exactly that — the lagged deviation from equilibrium — and its coefficient answers the trader's question: *how fast does a gap close?*

### B. Theory

- Δy_t = c + α·dev_{t−1} + γ·Δx_t + e_t, dev = y − a − βx from the long-run regression.
- Long run β (equilibrium), short run γ (same-day pass-through), adjustment α (pull back).
- α < 0 required; α = 0 → no correction; α < −1 → overshooting.
- After k periods without new shocks a deviation is multiplied by (1 + α)^k → half-life ln(0.5)/ln(1 + α).
- Granger representation theorem: cointegrated series admit an error-correction form; on non-cointegrated series the ECM regresses a stationary Δy on a non-stationary deviation — nonsense.

### C. Implementation

{{code}}

### D. Interpretation (from July 2016)

| | β | γ | α | t(α) | half-life |
|---|---|---|---|---|---|
| WTI ~ Brent | 0.979 | 0.888 | −0.115 | −7.7 | **5.7 business days** |
| simulated (true α = −0.30, γ = 0.50, β = 1) | 0.995 | 0.518 | −0.292 | −25.6 | 2.0 |
| coffee ~ Brent (not cointegrated) | 1.051 | 0.028 | −0.006 | −1.6 | 118 — meaningless |

- WTI absorbs 0.89 % of a 1 % Brent move the same day; the remaining gap with the long-run relation closes at 11.5 % a day — half gone in about six business days.
- August 2017: a WTI-specific shock widens the log spread from ≈ 0.08 to ≈ 0.12; it is back near its 0.06 average within about three weeks.
- The simulated pair recovers its known coefficients.

### E. Decision

The ECM is a coherent description of the exports-allowed regime: a deviation is expected to halve in about a week — if the relationship is stable, which 4.9–4.10 test.

### F. Pitfalls and limits

- An ECM on a non-cointegrated pair.
- Using `deviation_t` instead of `deviation_{t−1}`: the answer is then on the right-hand side.
- Two-step estimation ignores the estimation error of β.
- A single equation with a same-day Δx cannot cleanly say which market does the adjusting.
- The half-life assumes a constant α: a regime change alters it.

### G. Interview defence

> **Q: "What does the error-correction coefficient tell you, and why must it be negative?"**
>
> **A:** It's the speed of adjustment: the share of yesterday's deviation from the long-run relation closed today. For WTI on Brent it's about −0.115 with a t-stat near −8: roughly 11.5 % of a gap closes per day, a half-life of about six business days. It must be negative because it's a pull back — if WTI is above its equilibrium, its next move is pushed down. The ECM also separates the short run, 0.89 on the same day, from the long-run elasticity of about 0.98. And it only makes sense because the pair is cointegrated: on coffee and Brent it gives a meaningless 118-day half-life.
