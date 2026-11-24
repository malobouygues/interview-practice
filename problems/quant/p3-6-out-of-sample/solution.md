### A. Reasoning — explaining the past is not predicting the future

An in-sample regression answers “how well can a line pass through these points?”. A desk needs “how wrong would I have been, using only what I knew at the time, on days the model never saw?”. That requires a test period untouched during estimation, a model frozen before looking at it, and a benchmark: an error is only good or bad relative to the simplest forecast available.

### B. Theory (PDF A09 train/test and backtesting, A10-A metrics, A08-A benchmarks)

- **Chronological split + purge**: training labels must end before the test starts.
- **Frozen specification**: features, transformations and the model are chosen on the training period; the test period is used once.
- **Metrics**: MAE = mean |error|; RMSE = √mean(error²) ≥ MAE, more sensitive to large errors. Absolute levels depend on the period's volatility → compare with baselines *on the same rows*.
- **Baselines** for a return: zero (no predictable move) and the training mean.
- **Walk-forward, expanding**: re-estimate at each origin with all labels known by then; the path of the coefficients shows stability; the pooled errors show what a desk re-fitting quarterly would have experienced.
- A model that fails out of sample is a result. A model that succeeds is evidence of usefulness, not of causality or future profit.

### C. Implementation

Boolean filters on `target_end_date` and `date`; `sm.OLS(...).fit()` once; `predict(sm.add_constant(test[FEATURES], has_constant="add"))`; errors and baselines as Series. The walk-forward is a `while` loop over quarter starts with `pd.DateOffset(months=3)`.

### D. Interpretation (this dataset)

| | rows | R² | MAE | RMSE |
|---|---|---|---|---|
| in sample 2019–2022 | 991 | 3.0 % | 7.35 % | 9.69 % |
| out of sample 2023–2024 (frozen) | 492 | — | **6.21 %** | **7.85 %** |
| baseline: zero | 492 | — | **5.98 %** | **7.56 %** |
| baseline: training mean | 492 | — | 6.06 % | 7.63 % |
| walk-forward (quarterly) | 492 | — | 6.17 % | 7.81 % |

- Hit rate 52.2 %. The out-of-sample MAE is *lower* than in sample only because 2023–2024 was calmer than 2020–2022 — the baselines show the model is worse than doing nothing.
- Walk-forward path: surprise coefficient **−0.514 % → −0.382 %** per mb from the first to the last origin (training rows 991 → 1,429); demand growth stays ≈ −0.13 %. The coefficient decays as data without the effect accumulate.
- In the simulation the drift exists only in May 2020 – Dec 2021: a regime the training period contained and the test period did not.

### E. Decision

Do not trade the drift. The reaction to the release is real and immediate (3.5); the post-release continuation was a feature of 2020–2022 that did not survive into 2023–2024, either with a frozen model or with quarterly re-estimation. Re-examine if a similar regime (very volatile, recovering market) returns — and test it out of sample again.

### F. Pitfalls and limits

- A random split lets the model learn from 2024 to predict 2021: errors look better and mean nothing.
- Without purging, the late-December 2022 rows (labels ending in January 2023) put test-period prices into the estimation.
- Choosing the features after looking at 2023–2024 and re-running would turn the test period into a training period.
- 492 overlapping daily forecasts are about 50 independent 10-day periods: differences of a few basis points in MAE are not significant — here the model is not better by any measure, which is the safe direction.

### G. Interview defence

*“Your out-of-sample MAE (6.2 %) is better than in sample (7.3 %) — so the model generalises?”* — No: 2023–2024 was simply less volatile, so every forecast had smaller errors, including predicting zero. On the same rows the zero forecast does 5.98 %, better than the model. Errors only mean something against a baseline on the same period; the in-sample R² of 3 % and the t-stats were measuring fit to 2019–2022, not usefulness.
