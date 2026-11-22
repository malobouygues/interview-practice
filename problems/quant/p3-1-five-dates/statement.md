> **Synthetic data** — simulated with fixed seeds; the release calendar is realistic, the values are invented.

### Context

New project: you want to study how US crude inventories relate to WTI — **with only the information the desk actually had at each date**. The weekly stock report (`data/p3_us_crude_stocks_weekly_synthetic.csv`) has one row per week:

| column | meaning |
|---|---|
| `week_ending` | the Friday the stock level refers to |
| `release_date`, `release_time_et` | when the agency published it (usually the following Wednesday 10:30 New York, Thursday after a Monday holiday) |
| `crude_stocks_mbbl` | US commercial crude stocks, million barrels |
| `ingested_at` | when the value entered **your** database (history before 2019 was backfilled on 7 Jan 2019) |

### Objective

Make every timestamp of this dataset explicit and compute the moment each value became usable.

### Minimum theory (PDF, A04-A)

| timestamp | question it answers |
|---|---|
| observation | which period does the value describe? |
| publication | when did the source release it? |
| availability | when could I first use it? (publication + access delay) |
| ingestion | when did it enter my database? |
| vintage | which version of the value is it? (revised data have several) |

Rule: **index the economics on the observation date, join and backtest on the availability date.**

### Assumptions

All times are New York time (the agency's and NYMEX's clock), kept as naive timestamps; the report is usable at its release time (no extra access delay); weekly stock reports are not revised (one vintage).

### Your task

Implement `add_availability(stocks)` for the raw `DataFrame` (strings as read by `pd.read_csv`, work on a copy):

1. Convert `week_ending`, `release_date`, `ingested_at` to datetimes.
2. `available_at = release_date + release_time` (use `pd.to_timedelta(stocks["release_time_et"] + ":00")`).
3. `publication_lag_days` = days between `week_ending` and `release_date` (int).
4. `backfilled` = `ingested_at − available_at` greater than 7 days (bool).
5. Assert that every `available_at` is after its `week_ending`.

Return the columns `week_ending`, `crude_stocks_mbbl`, `release_date`, `available_at`, `ingested_at`, `publication_lag_days`, `backfilled`. Answer in the **Explain** tab.
