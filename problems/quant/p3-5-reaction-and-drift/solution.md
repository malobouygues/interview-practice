### A. Reasoning — two questions, two sampling designs

“How much does a surprise move the price?” is an event question: one observation per release, a window that starts just before the number is known. “Does the move continue afterwards?” is a forecasting question: at each settlement, use what is known, look at the next ten days. The second design samples every day, so its windows overlap — and the precision of its coefficients must be computed accordingly. Nothing here uses 2023–2024.

### B. Theory (PDF A09-D, A10-C)

- **Reaction window**: 10:29 → 14:30. Starting earlier (yesterday's settlement) would mix in moves that happened before the information existed.
- **Overlap**: with h = 10 and daily sampling, the forecast errors are correlated up to lag 9 by construction. OLS standard errors assume independence and are too small, especially for persistent regressors (demand growth, a surprise that stays the same for a week).
- **Newey-West HAC**: a weighted sum of autocovariances up to `maxlags`; `maxlags = h − 1 = 9` here.
- **Limits of HAC**: it is a correction of the *variance*, under the assumption that the model is otherwise right. It cannot detect that a feature was mis-timed (look-ahead), that two trending levels are unrelated (spurious regression, P4), or that the coefficient changed over time.

### C. Implementation

Filter both tables on the research period (by `release_date` and by `target_end_date`); one `sm.OLS(...).fit()` and one `.fit(cov_type="HAC", cov_kwds={"maxlags": ...})` per question; `sm.stats.durbin_watson(resid)`.

### D. Interpretation (this dataset, 2019–2022)

| reaction (208 releases) | coef | t | t (HAC 2) |
|---|---|---|---|
| surprise (per mb) | **−0.300 %** | −6.67 | −7.19 |

Durbin-Watson **2.08**. A 3 mb surprise moves WTI ≈ 0.9 % within hours.

| drift (991 days, 10-day forward) | coef | t (OLS) | t (HAC 9) |
|---|---|---|---|
| const | +0.69 % | 2.24 | **0.85** |
| surprise (per mb) | **−0.514 %** | −4.84 | **−2.86** |
| demand growth (per pp) | −0.132 % | −2.57 | **−1.35** |

Durbin-Watson **0.18**. HAC standard errors are 1.7–2.6 times the OLS ones. In sub-periods (surprise only, HAC): 2019–Apr 2020 t −0.87, May 2020–2021 −1.67, 2022 −1.63 — the drift is not uniform.

### E. Decision

Tell the trader: the reaction is large, fast and robust — the market prices the report within hours. The post-release drift is in-sample evidence only: weaker than it first looks once overlap is accounted for, uneven across sub-periods, and demand growth adds nothing robust. Whether it is tradable is decided out of sample (3.6).

### F. Pitfalls and limits

- Quoting the OLS t of −4.8 is quoting 991 overlapping observations as if they were independent.
- `maxlags` too small (e.g. 1) understates the correction; much too large adds noise. h − 1 is the natural floor here.
- The reaction regression is explanatory: the surprise is not known before 10:30, so it cannot be used to trade the reaction window itself.
- The pre-release snapshot is synthetic; with real data, the reaction often happens in seconds and the 10:29 price may already move on leaks of private estimates.

### G. Interview defence

*“You used HAC, so the drift is robust, right?”* — HAC makes the standard errors honest about the overlap I created by sampling daily; it doesn't say anything about whether the relationship is real or stable. If my surprise were mis-timed by a day, HAC would give me a perfectly 'robust' t-stat on a look-ahead bug. Robustness of inference and validity of the model are different questions — the second one needs the out-of-sample test.
