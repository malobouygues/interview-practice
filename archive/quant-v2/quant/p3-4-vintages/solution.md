### A. Reasoning — why keep every version

A monthly series downloaded today is a *final* history: each month at its best estimate, dated by the month it describes. Nobody ever saw that table in real time — the latest months were missing (publication lag) and the visible ones were first estimates, later revised. Any historical analysis that claims "an analyst could have known" must rebuild the view of each date from the vintages.

### B. Theory (PDF, A04-D)

- Two levels of rigour: (1) respect publication lags; (2) also use the vintage known at the time. Level 2 needs a vintage table.
- As-of view: `vintage_date ≤ t`, then latest per observation month (`groupby(...).last()` after sorting by vintage date). In SQL: `WHERE vintage_date <= :t`, then keep the most recent row per month.
- Revisions can be **biased** (here first prints are systematically low): that bias leaks into any analysis using final data.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

- As of **2016-06-15**, the latest month visible is **March 2016**; April appears on 30 June.
- As of 2017-09-15, all of 2016 has been through its annual revision (published 31 August 2017).
- First release → final: **+145 kb/d on average** (std ≈ 100). A history built from final values is systematically higher than what analysts saw at the time.

### E. Decision

Use the as-of view for any question about what was known at a date (step 3.5). Store your own downloads with a timestamp from now on, so future research has vintages.

### F. Pitfalls and limits

- Using the latest download as if it had been known historically.
- Ignoring that a view mixes vintages (a recent month in first release next to an old month already revised).
- Vintage tables of public sources are not always complete; when they are missing, say "pseudo point-in-time".

### G. Interview defence

> **Q: "You have ten years of monthly demand data. Is your backtest point-in-time?"**
>
> **A:** Only if I use the vintages. A downloaded history gives final values indexed by the month they describe, which hides two things: the two-month publication lag, and revisions — in my data first estimates are revised up by about 145 kb/d on average. I keep a vintage table and, for each decision date, rebuild the view: everything published on or before that date, latest estimate per month. Without vintages I can only respect the publication lag on revised data, and I'd call that pseudo point-in-time, not point-in-time.
