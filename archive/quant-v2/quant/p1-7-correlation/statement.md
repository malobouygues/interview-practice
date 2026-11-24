> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

The desk wants to know how closely the three crude benchmarks move together — a first view of hedging relationships. Correlation is the first number anyone computes, and on this dataset it is easy to get badly wrong: one genuine extreme day (the negative WTI expiry) and two trending price paths are enough to mislead.

### Objective

Compute correlations on the right scale and with the right estimator, and explain what they can and cannot say.

### Minimum theory

- **Pearson**: linear dependence, `cov(x, y) / (σx σy)`; built on moments, so a few extreme points can dominate it.
- **Spearman**: Pearson on ranks; captures any monotone relationship and is robust to outliers.
- **Levels vs changes**: two trending prices correlate in levels even without any link; co-movement is measured on **changes**.
- **Correlation ≠ causality**: a common factor (the global crude balance), reverse causality or coincidence all produce correlation.

### Assumptions

One correlation coefficient summarises a stable joint behaviour; it fails if the sample mixes regimes or contains a few extreme days.

### Your task

Implement `correlation_report(prices, a, b)` for a `DataFrame` indexed by date and two column names:

- levels: the prices themselves (USD/bbl); changes: `diff()` of each price (USD/bbl — log returns are undefined for WTI here);
- return a `dict` with `pearson_levels`, `spearman_levels`, `pearson_changes`, `spearman_changes` (floats). Let pandas drop the missing pairs.

Then answer in the **Explain** tab.
