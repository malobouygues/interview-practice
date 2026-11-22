### A. Reasoning — why split the sample

Every result of Cases 2–3 assumed one stable relationship. The desk gives you a reason to doubt it: a regulatory change that alters the arbitrage itself. With a known, economically motivated date, the first thing to do is to compare the relationship on each side — and to see what the full-sample test would have told you if you had not known.

### B. Theory

- Break in the long-run relation: the equilibrium y − βx − a shifts. A full-sample regression imposes one equilibrium, so its residual inherits a level shift.
- A stationary series with a level shift looks like a unit root to ADF (step 1.4) — and the Engle-Granger step 2 is an ADF test: the cointegration test loses its power.
- Break in the short-run dynamics: the daily pass-through β of returns changes; this is what the Chow test of step 4.2 tests formally.
- Placebo dates inside a regime should show no material change — a useful sanity check of the method.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| | pre (2012–2015) | post (2016–2019) |
|---|---|---|
| n | 1,044 | 1,043 |
| mean log spread (WTI discount) | 0.169 (≈ 16 %) | 0.059 (≈ 6 %) |
| std of the spread | 0.030 | 0.020 |
| return β (pass-through) | 0.59 | 0.89 |
| return correlation | 0.79 | 0.88 |
| Engle-Granger p-value | < 0.001 | < 0.001 |
| **full-sample Engle-Granger p-value** | **0.28** | |

- After the ban ended, the WTI discount fell from ≈ 16 % to ≈ 6 %, became less volatile, and WTI started to follow Brent much more closely day to day (pass-through 0.59 → 0.89). That is what an opened arbitrage route should do.
- Each regime is strongly cointegrated, but the full sample is not: one regression over 2012–2019 cannot fit two equilibria, its residual shifts by about 0.11 in 2016, and the Engle-Granger test reads that shift as non-stationarity. **Run on the full sample alone, the test would have told you there is no long-run relationship** — the opposite of the truth in each regime.
- Placebo dates inside a regime show statistics close to each other on both sides — around 2014, mean spread 0.163 vs 0.175 and pass-through 0.61 vs 0.57; around 2018, 0.059 vs 0.059 and 0.88 vs 0.89 — nothing like the jump at the real break.

### E. Decision

- Treat 2012–2015 and 2016–2019 as two regimes; estimate the current relationship (and the ECM of Case 3) on post-2016 data only.
- Never pool across a known change in the arbitrage mechanism without testing.
- Monitor the current regime: re-test the relationship regularly on recent sub-periods.

### F. Limitations and pitfalls

- Concluding cointegration (or its absence) on a sample containing an obvious break.
- Picking the break date by scanning the data for the largest change: the usual test distributions no longer apply (unknown-date break tests exist but are outside this track).
- Real breaks are often gradual (the spread narrowed over months in 2015); a sharp date is a simplification.
- Sub-period comparisons are descriptive; the formal test of a parameter change is next (Chow).

### G. Interview defence

> **Q: "Your Brent–WTI relationship isn't cointegrated on 2012–2019. Doesn't that kill your Case 3 model?"**
>
> **A:** No — it shows the full sample mixes two regimes. Until end-2015 US exports were banned; WTI traded at a ~16 % discount and followed Brent loosely. From 2016 the discount is ~6 % and the daily pass-through rises from 0.6 to 0.9. Each regime is strongly cointegrated on its own, but a single regression over both forces one equilibrium, so its residual jumps in 2016 and the Engle-Granger test reads that jump as a unit root — the same way a level shift fools an ADF test. So I estimate the relationship on the current regime and keep re-testing it, using an economically motivated date rather than one I picked from the chart.
