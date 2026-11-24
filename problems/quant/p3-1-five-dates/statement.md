> **Synthetic data** — weekly stock levels, consensus and release calendar simulated with fixed seeds. The calendar rules imitate a US weekly release; the numbers are invented.

### The desk asks

> “Can we use the weekly stock reports to understand WTI price reactions? I need to know what information was available when the market moved — not what the database says today. Start with the stock file: what do all these dates mean?”

### What you have

`data/p3_us_crude_stocks_weekly_synthetic.csv`, one row per weekly report (2019–2024):

| column | meaning |
|---|---|
| `week_ending` | the week the figure describes (Friday) |
| `release_date`, `release_time_et` | when the agency published it (New York time) |
| `crude_stocks_mbbl` | US crude stocks at the end of that week, million barrels |
| `consensus_change_mbbl` | analysts' expected weekly change, published before the release |
| `ingested_at_utc` | when the desk's database stored the record (UTC) |

### What to find out

For every report: when the market could first see it, in UTC; how long after the week it describes; which records' storage times are meaningless; and how much of each release was *news*.

### Minimum theory (PDF A04-A, the five timestamps)

- **Observation date**: the period described. **Publication**: when the source releases it. **Availability**: when a user can act on it (here = publication, converted to UTC). **Ingestion**: when *your* system stored it. **Vintage**: which version of a revised value (3.3).
- A **release calendar** has exceptions: holidays move releases, systems fail, data come late.
- A **backfill** loads history in one go: its ingestion time is the load date, not the market's date.
- Time zones: `pd.to_datetime(...).dt.tz_localize("America/New_York").dt.tz_convert("UTC")` — never a fixed `+5 h`.
- **Surprise** = actual change − consensus change: the part of the release the market did not expect.

### Assumptions

Availability = publication instant. A record is “backfilled” if it was ingested more than 2 days after its availability.

### Your task

Implement `add_availability(stocks)` (on a copy):

1. `week_ending` → datetime.
2. `available_at` = `release_date + release_time_et`, localised to New York, converted to UTC.
3. `ingested_at` = `ingested_at_utc` parsed as UTC.
4. `publication_lag_days` = days between the release date and `week_ending`; `backfilled` = `ingested_at − available_at > 2 days`.
5. Sort by `week_ending`; `stocks_change_mbbl` = weekly change of `crude_stocks_mbbl`; `surprise_mbbl` = change − `consensus_change_mbbl`.

Return the frame with a fresh index. Then the **Explain** tab.
