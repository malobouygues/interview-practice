### A. Reasoning — the same blank means three different things

A blank in `solar_mw` at 02:00 means “zero” (a reporting convention). A blank in `wind_mw` means “the feed failed”. A blank in `available_capacity_mw` at 15:00 means “the daily figure was sent this morning and still holds”. One blanket `ffill()` treats all three the same way — and invents data exactly where the trader's question is most sensitive.

### B. Theory (PDF A03-A, arbre B)

Diagnose before treating: **position** (start, middle, end of the sample), **regularity** (every night? every Sunday?), **simultaneity** (several columns at once?). Then:
- structural / convention → replace by its meaning (here 0);
- failure → keep `NaN`, add an indicator, measure the sensitivity of results to it;
- state variable → carry it with a **limit** and an **age**, because an old state may no longer hold.
Never fill a **price** from its neighbours: it is the outcome you want to explain.

### C. Implementation

- `typical = solar.fillna(0).groupby([month, utc_hour]).transform("median")` puts on each row the normal output of that month and UTC hour; `daylight = typical > 500`.
- `report_time = Series(index).where(capacity.notna()).ffill()` → the time of the last report on every row; `(index - report_time) / 1 h` is the age.
- `ffill(limit=48)` counts rows; the index is hourly UTC, so rows = hours.
- `report_date = local_date.where(reported).ffill()` → the local day the carried value belongs to; stale = `report_date < local_date`. The carried date is only used to judge the value, never as data.

### D. Interpretation (this dataset)

- Solar: **8,850** blanks → **8,845** structural (set to 0) + **5** failures (12 Jun 2024, 10:00–14:00 local). Grouping by *local* hour would flag 13 hours: 8 false failures at 17:00 in the last days of October, when the clock change makes that hour dark.
- Wind: **15** failures (14 Nov 2023 08:00–19:00, 6 Feb 2024 03:00–05:00) — left `NaN`.
- Capacity: **16,819** blanks → **95** after the 48-hour carry; **144** hours are stale (sent on an earlier local day); the 2–6 Sep 2024 publication outage reaches an age of **143 h** and stays blank after the limit. An “age ≥ 24 h” rule would flag **146**: the two extra hours are 23:00 on 29 Oct 2023 and 27 Oct 2024, the last hour of a 25-hour day, when the value is still that day's.
- Price: **2** blanks (16 May 2024, 03:00 and 04:00), untouched.

### E. Decision

Residual load is computed only where wind and solar are known (15 + 5 hours excluded, flagged); the capacity margin uses carried values but every result that depends on a stale capacity can be filtered with `capacity_is_stale`. None of the excluded hours is a spike hour, so the investigation is not affected — but that is a statement to *check*, not to assume.

### F. Pitfalls and limits

- `fillna(0)` on wind turns a feed failure into a windless hour: on a cold day it would manufacture a “cold and still” episode.
- Interpolating a price across a gap uses the *next* price: look-ahead, and an invented auction result.
- The 500 MW daylight threshold is a judgement call: dawn and dusk hours with a few MW are treated as zero — harmless for residual load, wrong for a solar-yield study.
- `ffill(limit=48)` on a non-hourly index would count rows, not hours.

### G. Interview defence

*“Why not forward-fill the wind for 12 hours? It's only 0.07 % of the data.”* — Because the 0.07 % is not random: it is one November day, and if that day turns out to matter, a filled value would be an invented observation sitting in the middle of the evidence. A missing value with a flag is honest and cheap; a filled one is a silent assumption. I fill states and conventions, I flag failures, and I report how many of each.
