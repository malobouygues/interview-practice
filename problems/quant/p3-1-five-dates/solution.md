### A. Reasoning — why five dates

"The data on date t" is ambiguous until you say *which* date. The stock level of a week is measured on Friday, released the next Wednesday, usable from 10:30 that morning, stored in your database whenever you happened to download it, and — for revised series — exists in several versions. Joining on the wrong one either uses information before it existed (look-ahead) or shifts it to a meaningless date. Point-in-time work starts by writing all of them down.

### B. Theory (PDF, A04-A and A01-B)

- Observation → the economics (which week). Availability → joins and backtests (what was known when).
- Publication follows a **release calendar**, not a fixed lag: here Wednesday, Thursday after a Monday holiday.
- Ingestion ≠ availability: a **backfill** stores years of history on one day; ingestion timestamps are only a proxy for availability for data collected in real time.
- One clock: convert everything to one time zone before comparing timestamps.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

- 209 weeks; publication lag **5 days** for 193 weeks, **6 days** for 16 (releases delayed by a Monday holiday, e.g. week ending 15 Jan 2016 → Thursday 21 Jan).
- **156 of 209** rows were backfilled on 7 Jan 2019: their `ingested_at` says nothing about when the market knew them.
- Week ending 15 Jan 2016: observed Fri 15 Jan, published and available Thu 21 Jan 10:30, ingested 7 Jan 2019, single vintage.

### E. Decision

Use `available_at` as the time key for every join of this table with prices (step 3.2); keep `week_ending` for charts and economic statements ("stocks in the week to 15 January").

### F. Pitfalls and limits

- Joining on `week_ending`: the value appears 5–6 days before its release.
- Using `ingested_at` as availability for backfilled history.
- A file of "monthly data dated the 1st" suggests availability on the 1st; it is usually weeks later.
- Real release calendars have exceptions (government shutdowns, holidays); a computed rule must be checked against the official calendar.

### G. Interview defence

> **Q: "What's the difference between the observation date and the availability date, and why does it matter?"**
>
> **A:** The observation date is the period the number describes — US stocks for the week ending Friday. The availability date is when you could first use it — the release, the following Wednesday at 10:30 New York, or Thursday after a holiday. For economic charts I index on the observation date, but every join with prices and every backtest uses availability; otherwise the stock number appears five or six days before it existed. I also don't use my database's ingestion time as a proxy: most of this history was backfilled in 2019.
