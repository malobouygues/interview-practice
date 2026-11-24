### A. Reasoning — why the colleague's chart overstates the link

The chart compares the crack of a month with demand growth **of that same month**, taken from today's revised history. On the day the crack was set, that demand figure did not exist: it was published two months later, and revised a year after that. The honest comparison uses, for each month-end, the demand growth an analyst could compute that day.

### B. Theory (PDF, A04-D, A11)

- Information set at t = as-of view at t. Real-time growth is computed *inside* that view.
- Two sources of overstatement: **publication lag** (using a value not yet published) and **revisions** (using a better value than the one available).
- Errors-in-variables: noisier real-time data mechanically weaken measured relationships; revised data make them look stronger than they were usable.
- Vocabulary: point-in-time (lags + vintages) / pseudo point-in-time (lags respected, revised data) / neither.

### C. Implementation

{{code}}

The loop over decision dates mirrors the real process: each month-end, look at what is published, compute, record.

### D. Interpretation (this dataset)

| comparison | correlation with the diesel crack |
|---|---|
| final growth of the **same** month (colleague's chart) | **0.83** |
| growth known at the **month-end** (point-in-time) | **0.59** |

- Real-time growth differs from the final growth of the same month by ≈ **0.7 pp** on average and has the **opposite sign in 10 of 46** months.
- The gap is mainly the publication lag (month m vs month m−2), plus revision noise.
- The relationship exists in real time, but it is clearly weaker than the chart suggests.

### E. Decision

Report the point-in-time figure (≈ 0.6) as the usable relationship; present the 0.83 only as a description of history with hindsight, explicitly labelled.

### F. Pitfalls and limits

- Calling an analysis on revised, observation-dated data "historical evidence of predictive power".
- Forgetting that real-time growth mixes vintages.
- Correlation is still not causality, and 46 monthly observations with overlapping year-on-year windows are few — the effective sample is smaller.

### G. Interview defence

> **Q: "Demand growth and the diesel crack are 0.83 correlated. Is demand data a good indicator for the crack?"**
>
> **A:** That 0.83 compares each month's crack with the same month's demand growth from today's revised data — numbers that were published two months later and revised afterwards. Rebuilding what was known at each month-end from the vintages, the correlation is about 0.59: real, but much weaker. Most of the difference is the publication lag; revisions add noise — real-time growth even has the wrong sign in about one month in five. So I'd say the relationship is there, but the usable information is the 0.6, not the 0.83.
