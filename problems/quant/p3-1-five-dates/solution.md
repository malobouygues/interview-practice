### A. Reasoning — “the week of 17 June” is not a date you could trade

A database row carries one date by default — usually the observation date — and that is the trap: the figure for the week ending Friday 17 June 2022 did not exist for the market on 17 June. Point-in-time work starts by attaching to each number the moment it became *available*, in a single time zone, and by recognising which stored timestamps are artefacts of how the database was built.

### B. Theory (PDF A04-A, A04-D)

| date | question it answers | here |
|---|---|---|
| observation | what period is described? | `week_ending` |
| publication | when did the source release it? | `release_date` 10:30 New York |
| availability | when could *we* act on it? | publication in UTC |
| ingestion | when did *our* system store it? | `ingested_at` |
| vintage | which version of a revised value? | weekly: first release; monthly demand: 3.3 |

Calendars have exceptions (holidays, outages); backfills destroy the meaning of ingestion times; time zones move with daylight saving — on *both* sides of the Atlantic, on different dates.

### C. Implementation

`pd.to_datetime(date + " " + time)` gives a naive New York time; `tz_localize(NEW_YORK).tz_convert("UTC")` handles EST/EDT. The lag is a difference of dates (`.dt.days`). `diff()` after sorting by `week_ending` gives the weekly change; minus the consensus gives the surprise.

### D. Interpretation (this dataset)

- **314** reports. Publication lag: **5 days** for 278, **6 days** for 35 (Thursday releases after a Monday holiday or a holiday on Wednesday), **12 days** once — week ending **17 Jun 2022**, published **29 Jun 2022**.
- **61** records were ingested on **2 Mar 2020 09:00 UTC** (database creation): `ingested_at` is useless as an availability time for 2019 — the calendar is the only source.
- 10:30 New York = **14:30 UTC** in summer (204 releases), **15:30 UTC** in winter (110).
- Surprises are centred near zero with a standard deviation of about 3 million barrels: most of the weekly change is expected.

### E. Decision

From now on every join uses `available_at` (UTC). The week of 17 June 2022 becomes usable on 29 June 2022 at 14:30 UTC, not on 17 June — twelve days of information the database would otherwise “know” in advance.

### F. Pitfalls and limits

- Using `ingested_at` as availability would delay every 2019 report to March 2020 (too late) — the opposite error of using `week_ending` (too early).
- A fixed offset (+5 h) is wrong for half the year.
- The consensus has its own timestamp (published before the release); here we assume it always is — check it in a real dataset.
- Availability = publication assumes the desk receives the release instantly; a real feed adds seconds to minutes.

### G. Interview defence

*“Why do you need five dates? Isn't the publication date enough?”* — For a public release, publication and availability coincide, but the database doesn't store publication — it stores observation and ingestion. Observation is too early, ingestion can be months late after a backfill. I rebuild availability from the release calendar, in UTC, and I keep the others to audit the data: if ingestion is ever *before* availability, something is wrong.
