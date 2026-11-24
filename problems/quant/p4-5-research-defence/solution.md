### Reference answer

**Yes — but say it carefully.** Brent and WTI are tied by something real: physical arbitrage between two light sweet crudes. The data are consistent with that: day to day, WTI moves with Brent (return correlation 0.82), and over time the gap between them comes back (Engle-Granger rejects “no equilibrium”).

**What I would not use as evidence** is the 0.996 correlation of prices. Two trending prices correlate whatever links them: coffee has 0.82 with WTI on the same measure, and a levels regression of WTI on coffee gives a t-stat of 69 — which vanishes in daily changes and fails a proper cointegration test. Prices behave like random walks, so levels regressions without an economic reason are fishing.

**What changed:** the relationship is not one fixed number. Until the US export ban ended in 2015, the discount averaged about 16 $/bbl, WTI passed through only 60 % of Brent's daily moves and closed gaps slowly (half-life ≈ 12 days). Since 2016 the discount is about 3 $/bbl, pass-through is 90 % and the half-life is about 5 days. The Chow test leaves no doubt (F ≈ 113). The full-sample average discount of 9 $/bbl describes neither period — trading back to it after 2016 would have been a mistake.

**What I'm comfortable saying:** there is a stable post-2016 equilibrium with a small discount and fast adjustment, explained by export arbitrage. **What I'm not:** that it will hold if export or pipeline capacity changes, that the statistics prove causality beyond that arbitrage story, or that the spread is a free mean-reversion trade — it has fat-tailed days (hurricanes) and changing volatility. I'd monitor export capacity, Gulf Coast disruptions and the spread's half-life.

### Why this answer works

- Answer first, then the reason (mechanism), then the evidence in the right order (returns for co-movement, cointegration for the long run).
- Uses the coffee control to show why correlation of levels is not evidence.
- Treats the break as the central finding, with the practical consequence for a spread trader.
- Separates what is supported from what is not, and ends with what to monitor.

### Common weaknesses

- “Correlation 0.996, so they're linked.”
- Reporting cointegration over the full sample as one stable equilibrium.
- Claiming ADF non-rejection *proves* a unit root.
- Forgetting the mechanism: cointegration found without a reason is not a trading relationship.
