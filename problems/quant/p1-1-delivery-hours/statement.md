> **Synthetic data** — a fictional Central-European power market (three zones, CET/CEST clock), simulated with fixed seeds. Not market observations.

### The desk asks

> “We had several very high day-ahead prices during cold, low-wind periods. Before anyone tells me a story about the weather, I want the hourly file loaded properly. The vendor export is messy — I don't want to find out next month that we counted some hours twice or lost others.”

### What you have

`data/p1_power_hourly_vendor_synthetic.csv`, the vendor's export for 2023–2024, one row per delivery hour *as the vendor sent it*:

| column | meaning |
|---|---|
| `delivery_start_local` | start of the delivery hour, market wall-clock time (`2023-10-29 02:00`) |
| `utc_offset` | offset of that wall-clock time from UTC: `+01:00` (winter, CET) or `+02:00` (summer, CEST) |
| `price_eur_mwh` | day-ahead price of the hour |
| `load_mw`, `wind_mw`, `solar_mw` | average MW during the hour (actuals) |
| `available_capacity_mw` | dispatchable capacity (sent once a day — exercise 1.2) |
| `gas_eur_mwh` | gas price of the day |
| `loaded_at_utc` | when the vendor wrote **this version** of the record |

### What to find out

How many delivery hours the file really contains, which version of each record to trust, and a table with **exactly one row per delivery hour** on a clock that has no ambiguity.

### Minimum theory (PDF A01-C, A02-C, A03-C)

- A **delivery period** is an interval (here one hour); the timestamp is its start. The **local market date** is the label traders use; **UTC** is the only clock with no gaps and no repeats.
- Daylight saving: on the last Sunday of March 02:00 → 03:00 local (a **23-hour** day); on the last Sunday of October 03:00 → 02:00 (a **25-hour** day — the 02:00 hour exists twice, once at `+02:00`, once at `+01:00`).
- Two rows can be **exact copies** (the same record sent twice → drop one) or **two versions** of the same key (a correction → keep the latest `loaded_at`). The key must be unambiguous *before* you deduplicate on it.
- Tools: `pd.to_datetime(text, format="%Y-%m-%d %H:%M%z", utc=True)`, `.dt.tz_convert("Europe/Paris")`, `.dt.tz_localize(None)`, `.dt.normalize()`, `drop_duplicates()`, `sort_values` + `drop_duplicates(subset=..., keep="last")`.

### Assumptions

The market clock is `Europe/Paris`. A later `loaded_at_utc` always supersedes an earlier one.

### Your task

Implement `load_market_hours(path)`:

1. Read the CSV. Build `delivery_start_utc` from `delivery_start_local + utc_offset` (UTC, tz-aware) and parse `loaded_at_utc` (UTC).
2. Drop exact duplicate rows.
3. For each `delivery_start_utc`, keep the row with the latest `loaded_at`.
4. Add `local_date` (local calendar day, naive, midnight) and `local_hour` (0–23) from the UTC time converted to the market clock.
5. Return the frame indexed by `delivery_start_utc` (sorted), with the columns `local_date`, `local_hour`, `price_eur_mwh`, `load_mw`, `wind_mw`, `solar_mw`, `available_capacity_mw`, `gas_eur_mwh`.

Use the Test code pad to look at the raw file first (`head`, `info`, `describe`, `duplicated`), then answer the trader in the **Explain** tab.
