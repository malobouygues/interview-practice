> **Synthetic data** — simulated with fixed seeds; coffee is independent of crude **by construction**.

### Context

Step 4.4 established that the crude prices are I(1). What happens if you regress one I(1) series on another anyway? A colleague has done it: *"coffee on Brent in log levels since mid-2016: R² = 0.59, t-stat = 36 — oil drives coffee (fertiliser, diesel, transport)."*

### Objective

Expose the spurious regression with a simple, defensible comparison of levels and differences, and understand why non-stationary series make level regressions misleading.

### Minimum theory

- If `x` and `y` are independent random walks, `y = α + βx + e` has a **non-stationary residual**: the fitted line describes the drift the two series happened to share. The t-statistic of β does **not** follow a t-distribution; its typical size grows with the sample, so "significance" appears almost always. R² does not go to zero either.
- In **differences**, `Δy = a + b·Δx + u` relates stationary variables: inference is valid again, and a spurious link disappears.
- A link that survives in differences shows real co-movement; a **long-run** link in levels needs a stationary residual — cointegration (4.7).

### Assumptions

Both series are I(1) (step 4.4).

### Your task

Implement `levels_vs_differences(y, x)`:

1. Regression in levels: align `y` and `x`, drop `NaN`, OLS of `y` on a constant and `x`.
2. Regression in differences: the same aligned data, `.diff()`, drop `NaN`, OLS.
3. Return `r2_levels`, `tstat_levels`, `r2_differences`, `tstat_differences` (t of the slope) and `verdict`:
   `"co-moving"` if |t differences| ≥ 1.96; otherwise `"spurious"` if |t levels| ≥ 1.96; otherwise `"unrelated"`.

Then answer in the **Explain** tab (run the test code first: it contains the Monte Carlo).
