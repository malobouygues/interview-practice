### A. Reasoning — why two tests

A hypothesis test only controls the error of rejecting *its own* null. ADF protects "unit root": when it fails to reject, you have learned little. KPSS protects "stationary". If ADF does not reject **and** KPSS rejects, two tests built from opposite starting points point the same way — that is evidence. If they disagree in the "both reject" or "neither rejects" way, the disagreement itself is the diagnosis.

### B. Theory

- **KPSS** decomposes the series into a deterministic part, a random walk and a stationary error, and tests whether the random-walk variance is zero. H0: stationary (around a level / a trend). H1: unit root.
- Its p-value comes from a short table: statsmodels returns **0.01** for "0.01 or less" and **0.10** for "0.10 or more". Report "p ≤ 0.01", not "p = 0.01".
- Same deterministic terms in both tests, otherwise they answer different questions.
- KPSS tends to over-reject for very persistent stationary series; ADF has low power against them. That is exactly the "conflict" case.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Series | spec | ADF p | KPSS p | verdict |
|---|---|---|---|---|
| TTF level | c | 0.91 | ≤ 0.01 | unit root |
| TTF log returns | c | < 0.001 | ≥ 0.10 | stationary |
| trend-stationary | c | 0.86 | ≤ 0.01 | unit root — wrong specification |
| trend-stationary | ct | < 0.001 | ≥ 0.10 | stationary |
| persistent, 2,000 obs | c | < 0.001 | ≤ 0.01 | conflict |
| persistent, 40 obs | c | 0.52 | ≥ 0.10 | inconclusive |
| stationary + level shift | c | 0.47 | ≤ 0.01 | unit root — fooled by the break |

The TTF diagnosis is now solid: **level ≈ I(1)** (concordant), **log returns stationary** (concordant).

### E. Decision

- `stationary`: use the series as is (check the variance over time on a chart).
- `unit root`: look for breaks first (the level-shift row shows why); if none, treat as I(1): work in differences/returns *if the analysis requires stationarity*, and re-test the transformed series.
- `conflict`: re-test with `'ct'`, test sub-periods, check whether the variance changes; do not pick the test you like.
- `inconclusive`: say so; decide from the economic nature of the series and make conclusions robust to both readings.

### F. Limitations and pitfalls

- The table is a set of plausible readings, not the identification of the data-generating process. "Both reject = difference-stationary" style shortcuts are not theorems.
- Reading KPSS p = 0.01 as an exact value: the true p-value can be far smaller. With `alpha = 0.01`, the rule `p < alpha` then never rejects — compare the statistic with the 1 % critical value instead.
- Choosing the significance level after seeing the result: the 40-observation draw in the tests is "inconclusive" at 5 % and "stationary" at 10 %.
- Using different deterministic terms in the two tests.
- A structural break can make *both* tests point to a unit root (last-but-one row): always look at the chart.

### G. Interview defence

> **Q: "Why did you use KPSS in addition to ADF?"**
>
> **A:** Because their nulls are opposite. ADF's null is a unit root, so a high ADF p-value only says I can't reject it; KPSS's null is stationarity. On the TTF level ADF doesn't reject and KPSS rejects at 1 %, so two tests starting from opposite assumptions agree: the level behaves like a unit-root process. On returns it's the reverse. When they disagree — both reject or neither does — I don't pick one: both rejecting usually means a misspecified trend, a break or changing variance, and neither rejecting means the sample is too short to decide.
