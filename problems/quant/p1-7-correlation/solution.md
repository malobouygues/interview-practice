### A. Reasoning — why two estimators and two scales

The economic question — "do these benchmarks move together day to day?" — is about changes. Levels add a second, irrelevant effect (both paths fell and recovered together). And with one genuine extreme day in the sample, the choice of estimator changes the answer from "weak" to "strong". Computing both, and understanding why they differ, is the analysis.

### B. Theory

- Pearson r ∈ [−1, 1], linear, moment-based → sensitive to extremes.
- Spearman ρ = Pearson on ranks → monotone association, robust.
- Trending levels correlate mechanically; correlate changes.
- Correlation is symmetric: it cannot say which market drives which. Dependent observations make naive significance tests too optimistic.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| pair | Pearson levels | Spearman levels | Pearson changes | Spearman changes |
|---|---|---|---|---|
| Brent / Dubai | 0.998 | 0.996 | 0.885 | 0.868 |
| Brent / WTI | 0.990 | 0.996 | **0.320** | **0.869** |
| Brent / WTI without 20–21 Apr 2020 | 0.997 | 0.996 | 0.884 | 0.871 |

- The expiry day makes WTI move −47.5 and +46.1 USD/bbl while Brent barely moves: those two points dominate Pearson's covariance and variance. Spearman treats them as "the largest moves" and keeps 0.87; dropping them brings Pearson back to 0.88.
- Level correlations of 0.99 would be high for almost any two crude prices over 2019–2021: they mostly reflect the shared crash and recovery.
- Brent and Dubai co-move at 0.88 in changes because both price the same global balance — not because one drives the other.

### E. Decision

Report the co-movement of changes with Spearman, or Pearson with and without the event, and explain the difference. Keep level correlations out of any argument about a relationship (Project 4 shows why formally).

### F. Pitfalls and limits

- A single Pearson number on a sample with a genuine extreme event.
- Silently dropping the event to "fix" the correlation: show both.
- Reading correlation as causality, or level correlation as co-movement.
- A full-sample correlation hides regimes (Project 4 tests a structural change).

### G. Interview defence

> **Q: "How correlated are Brent and WTI daily moves in your data?"**
>
> **A:** About 0.87 on a typical day — but it depends how you measure it. The Pearson correlation of daily changes is only 0.32, because of the April 2020 expiry: WTI fell 47 dollars and bounced 46 the next day while Brent barely moved, and those two points dominate a moment-based estimator. Spearman, which works on ranks, gives 0.87, and Pearson without those two days gives 0.88. So I'd report 0.87 and mention the event explicitly. And that's co-movement, not causality: both benchmarks respond to the same global crude balance.
