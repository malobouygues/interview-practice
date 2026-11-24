### A. Reasoning — right date, wrong number

3.2 fixed *when* a number arrives. Monthly demand adds a second problem: the number itself changes after publication. A historical study that uses today's database values gives the past desk better information than it had — the timing can be perfect and the content still be look-ahead.

### B. Theory (PDF A04-D point-in-time, A04-E look-ahead)

- **Publication lag**: demand for month M is first published at the end of M + 2. A decision in March sees December at best.
- **Revisions**: second estimate (M + 3), annual revision (August of the next year). The last vintage is what the database shows.
- **Genuine PIT**: as-of view of the vintages. **Pseudo PIT**: final values shifted by the lag. **Neither** (final values on the observation date): the worst case.
- Report what cannot be reconstructed: without vintages, quantify typical revisions and present the backtest as an upper bound.

### C. Implementation

`groupby("obs_month")["demand_kbd"].last()` after sorting by `vintage_date` gives the latest vintage per month — on all vintages (final) or only on those with `vintage_date < decision` (as known). A plain loop over decision dates; `pd.Period(month) - 12` finds the same month a year earlier.

### D. Interpretation (this dataset)

| decision | latest month | known | final | growth known | growth final |
|---|---|---|---|---|---|
| 15 Mar 2021 | 2020-12 | 18,746 | 19,034 | −6.32 % | −4.88 % |
| 15 Jul 2020 | 2020-04 | 16,920 | 17,056 | −15.34 % | −14.98 % |
| 15 Mar 2024 | 2023-12 | 19,843 | 19,904 | −0.37 % | −0.07 % |
| 15 Sep 2024 | 2024-06 | 20,394 | 20,599 | +0.42 % | +1.43 % |

Over one decision per month 2019–2024: final − known = **+127 kb/d** on average (**145** in absolute value); growth differs by **0.67 pp** on average. First estimates are systematically low, so pseudo-PIT growth is systematically more optimistic than what the desk saw.

### E. Decision

Use `growth_known_pct` — the value as known — in every model of 3.5–3.6 (the decision table already does). Never present a result built on final values as something the desk could have used.

### F. Pitfalls and limits

- `merge_asof` on `vintage_date` gives the right *month*, but `groupby().last()` on all vintages gives the wrong *value*: the as-of filter must come before the aggregation.
- “Usable the day after” is a convention; an intraday publication time would allow same-day use after the release.
- Forward-filling the latest known value to daily decisions is fine *after* its vintage date — it is how the decision table is built.
- Vintages are rarely kept by vendors: archive your own snapshots, or you will only ever have pseudo point-in-time.

### G. Interview defence

*“We don't have vintages. Can we still backtest?”* — Yes, but honestly: shift every series by its publication lag (pseudo point-in-time), measure how big revisions typically are on the period where you can, and state the result as an optimistic bound. Here the gap is about 0.7 point of growth on average — enough to create a signal that was never tradable.
