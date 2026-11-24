> **Synthetic data** — simulated with fixed seeds; the hurricane-type shock is imitated, values are invented.

### Context

The gasoline crack showed one absurd day (step 2.1), and late August 2017 looked extreme too. Before deciding what to do with extremes, you need a way to *find* them. Three classic scores exist, and on commodity returns they give very different answers.

### Objective

Compute four scores on RBOB daily log returns and understand why they disagree.

### Minimum theory

| method | rule | weakness |
|---|---|---|
| z-score | `(r − mean) / std`, flag ≈ \|z\| > 3 | mean and std are contaminated by the outliers themselves (**masking**) |
| modified z-score | `0.6745 (r − median) / MAD`, flag ≈ \|z\| > 3.5 | MAD = 0 if many identical values |
| IQR rule | outside `[Q1 − 1.5 IQR, Q3 + 1.5 IQR]` | too many flags on fat-tailed returns |
| rolling modified z | median and MAD of the **previous** 60 days only | needs a history; reacts to regime changes |

`MAD = median(|r − median(r)|)`; 0.6745 makes it comparable with a standard deviation for normal data. Detection is done on **returns**, not on trending price levels.

### Assumptions

Returns are computed on the treated prices of step 2.2 (`data/p2_products_treated_synthetic.csv`), between consecutive observed prices.

### Your task

Implement `outlier_scores(returns)` for a `pd.Series` of log returns (drop `NaN` first). Return a `DataFrame` on the remaining index with columns:

- `return`; `z` (full-sample mean and `std()`); `modified_z` (full-sample median and MAD);
- `iqr_outlier` (bool, full-sample quartiles);
- `rolling_modified_z`: `rolling_median = r.rolling(60, min_periods=30).median().shift(1)`, `rolling_mad` = the same rolling median applied to `|r − rolling_median|`, shifted by one; score `0.6745 (r − rolling_median) / rolling_mad`.

Answer in the **Explain** tab.
