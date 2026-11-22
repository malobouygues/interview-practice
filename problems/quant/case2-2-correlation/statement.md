> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Coffee is independent of crude **by construction**.

### Context

In 2.1 you predicted that Brent and WTI returns should be strongly correlated. Correlation is the first number anyone computes — and the first one people misuse, because computing it on price **levels** gives an impressive figure for almost any two trending prices.

### Objective

Compute correlations on the right scale, compare a genuine pair (Brent–WTI) with a pair that has no link (Brent–coffee), and see which numbers can be trusted.

### Minimum theory

- **Pearson**: linear dependence, `cov(x, y) / (σx·σy)`; sensitive to a few extreme observations. `s1.corr(s2)`.
- **Spearman**: Pearson computed on ranks; captures any monotone relationship and is robust to outliers and to monotone transformations. `s1.corr(s2, method="spearman")`.
- **Levels vs returns**: two independent non-stationary series that both trend look correlated in levels (*spurious correlation*). The link that matters is in the co-movement of **changes**.
- **Correlation ≠ causality**: a common driver, reverse causality or coincidence can all produce correlation.

### Assumptions

A correlation coefficient estimates one stable number: it assumes the joint behaviour of the two series does not change over the sample — which fails for non-stationary levels.

### Your task

Implement `correlation_report(prices, a, b)`:

- `prices` — a `DataFrame` indexed by date; `a`, `b` — two column names.
- Work on **log prices**: levels = `np.log(prices[col])`; returns = the first difference of the log prices.
- Return a `dict` with `pearson_levels`, `spearman_levels`, `pearson_returns`, `spearman_returns` (floats). Let pandas drop the `NaN` of the first return.

Then answer the question in the **Explain** tab.
