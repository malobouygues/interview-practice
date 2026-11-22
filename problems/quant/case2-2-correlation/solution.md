### A. Reasoning — why compute correlation twice

The economic hypothesis (2.1) is about co-movement: when Brent moves, WTI moves. That is a statement about **changes**. A correlation of levels mixes it with something else — whether the two paths happened to drift in the same direction over the sample — and for trending prices that second effect can dominate completely. Computing both, on a genuine pair and on a control pair, shows the size of the trap.

### B. Theory

- Pearson r = cov(x, y)/(σx σy) ∈ [−1, 1]: linear association.
- Spearman ρ = Pearson on ranks: monotone association, robust to outliers and invariant to monotone transformations (log or not, same Spearman).
- For two **independent random walks**, the level correlation does not converge to 0 as the sample grows: it stays random and is often large in absolute value. For their returns, it converges to 0.
- Common seasonality or common trends also inflate level correlations: correlate changes (or deseasonalised residuals).
- Correlation is symmetric: corr(x, y) = corr(y, x). It cannot say which variable drives which.

### C. Implementation

{{code}}

### D. Interpretation (this dataset, Jul 2016 – Dec 2019)

| Pair | Pearson levels | Spearman levels | Pearson returns | Spearman returns |
|---|---|---|---|---|
| Brent / WTI | 0.994 | 0.987 | 0.878 | 0.862 |
| Brent / coffee | 0.769 | 0.745 | 0.027 | 0.043 |
| WTI / coffee | 0.768 | 0.739 | 0.028 | 0.039 |

- Coffee has *no* link with crude in this data, yet its level correlation with Brent is 0.77 — the two paths happen to have trended together. In returns: 0.03. **The level correlation was measuring the drift, not a relationship.**
- Brent–WTI returns correlate at 0.88: day-to-day co-movement is real and strong. Pearson and Spearman agree, so it is not driven by a few extreme days (the −5 % WTI-specific shock of August 2017 barely moves it).
- The monotone non-linear test pair shows the Pearson/Spearman difference cleanly: ranks agree perfectly (ρ = 1) while the linear fit is imperfect.

### E. Decision

- Report the **returns** correlation as the measure of co-movement (0.88), never the level correlation.
- A high level correlation is a reason to ask "is this a long-run relationship or two shared trends?" — Case 3 answers that with a cointegration test, not with a correlation.
- If Pearson and Spearman diverge markedly, look for outliers or non-linearity before reporting either.

### F. Limitations and pitfalls

- Correlation over the whole sample hides regimes: compute it on sub-periods if the relationship may have changed (Case 4).
- With dependent data, the effective number of independent observations is smaller than n, so naive significance tests of r are too optimistic.
- Different closing times (Asia / Europe / US) can create an apparent one-day lead between markets.
- "Correlated, therefore one drives the other": a common factor — the global crude balance — moves both.

### G. Interview defence

> **Q: "Coffee and Brent are 77 % correlated in your data. Should we hedge coffee with Brent?"**
>
> **A:** No — that 77 % is computed on price levels, and both are trending prices: two unrelated random walks often show a large level correlation just because they drifted the same way over the sample. On daily returns the correlation is about 3 %, i.e. nothing. A hedge works on changes, so the returns correlation is the relevant number. For Brent and WTI the returns correlation is 0.88 — that one reflects a real arbitrage link — and even then it doesn't tell me which one drives the other: both respond to the global crude balance.
