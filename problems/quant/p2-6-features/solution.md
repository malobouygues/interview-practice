### A. Reasoning — why the information set comes first

A feature is valid only if it can be computed at the forecast origin with the information available then; its economic relevance comes second (PDF, A07). The most common leakage is invisible: a rolling mean whose window includes today, so "yesterday's average" quietly contains the answer. Writing the origin and the information set at the top of the function, and shifting every market feature by one day, makes the timing checkable line by line.

### B. Theory

- Origin = morning of t; information = settlements ≤ t−1; target = change from t−1 to t.
- `rolling(n)` on row t uses rows t−n+1…t → `.shift(1)` moves it to t+1, i.e. uses only data up to t−1 on row t.
- Calendar variables are deterministic: no shift.
- Screening by correlation with the target is a *first filter*: the sign must be economically sensible and stable across sub-periods; with many candidates, some correlations are luck.
- Truncation check: features computed on data cut at a past date must equal the full-data features up to that date (formalised in Project 3).

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| feature | corr with crack change 2017–18 | 2019 | verdict |
|---|---|---|---|
| change_lag1 | −0.16 | −0.22 | keep — daily moves partly reverse |
| gap_to_mean_60 | −0.07 | −0.11 | keep — a stretched crack tends to come back |
| mean_change_20 | −0.05 | −0.12 | weak, overlaps with gap_to_mean_60 |
| vol_change_20 | −0.11 | +0.02 | sign flips — drop |
| corr_gasoil_60 | +0.03 | −0.02 | ≈ 0 — drop for this target |
| heating_season | +0.03 | −0.01 | the *level* is seasonal, the daily *change* is not |

All correlations are small: day-to-day crack changes are mostly noise. The features with a stable sign and a story (reversal, mean reversion) are the candidates for a simple model (Project 4 discusses model selection).

### E. Decision

Keep `change_lag1` and `gap_to_mean_60` as candidates; drop the unstable ones; verify every feature with the truncation test before using it in any analysis.

### F. Pitfalls and limits

- `rolling(...)` without `shift(1)`, `center=True`, or `shift(-1)`: the future enters the feature.
- Feeding prices with holiday `NaN`s into rolling windows: 20 days of `NaN` after every holiday.
- Selecting features on the whole sample and then reporting their performance on the same sample.
- Heating season explains the crack **level**, not its daily **change**: match the feature to the target.

### G. Interview defence

> **Q: "You built a 20-day rolling mean as a feature. How do you know it doesn't leak?"**
>
> **A:** I fix the forecast origin first — the morning of day t, before that day's settlement — so the information set is settlements up to t−1, and every price-based feature is shifted by one day after the rolling window. Calendar variables aren't shifted because they're known in advance. Then I check it: I rebuild the features on data truncated at a past date and verify they're identical to the full-data features up to that date. If anything changed, it was using the future. And I only keep features with an economic reason and a stable sign across sub-periods — here yesterday's move and the gap to the 60-day mean.
