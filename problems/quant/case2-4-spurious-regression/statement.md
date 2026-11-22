> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Coffee is independent of crude **by construction**.

### Context

Step 3 produced a "significant" regression of coffee on Brent (t = 36). This is the classic **spurious regression**: regress one non-stationary series on another, unrelated one, and OLS reports a high R² and huge t-statistics. You need a quick, defensible way to expose it.

### Objective

Compare each regression in levels with the same regression in **first differences**, classify the pair, and understand why non-stationary series make level regressions misleading.

### Minimum theory

- If `x` and `y` are independent random walks, the regression `y = α + β·x + e` has a **non-stationary residual**: the fitted line only describes the drift the two series happened to share in this sample. The t-stat of β then does not follow a t-distribution; its typical size grows with the sample, so "significance" appears almost always.
- In **differences**, `Δy = a + b·Δx + u` relates stationary variables: inference is valid again, and a spurious relationship disappears.
- A relationship that survives in differences shows real *co-movement*; whether the **levels** share an equilibrium is a separate question (cointegration, Case 3).

### Assumptions

Both series are I(1) — established with the tools of Case 1 (the log prices here all are).

### Your task

Implement `levels_vs_differences(y, x)`:

- Regression 1: `y` on a constant and `x` (levels). Regression 2: `y.diff()` on a constant and `x.diff()` (align and drop `NaN`).
- Return a `dict`: `r2_levels`, `tstat_levels`, `r2_differences`, `tstat_differences` (floats, t-stat of the slope) and `verdict`:
  - `"co-moving"` if |`tstat_differences`| ≥ 1.96;
  - otherwise `"spurious"` if |`tstat_levels`| ≥ 1.96;
  - otherwise `"unrelated"`.

Then answer the question in the **Explain** tab (run the test code first: it contains the Monte Carlo).
