> **Synthetic data** — fictional market zones and weather stations, simulated with fixed seeds. Not observations.

### The desk asks

> “North-zone load was clearly up this January. Is demand growing, or was it just colder? Before you answer, give me something I can compare day by day and zone by zone: how cold or hot each day was, and how much power each zone used.”

### What you have

- `data/p1_zone_temperature_obs_synthetic.csv` — weather observations, **UTC**, long format: `observed_at_utc`, `zone`, `temperature_c`. Mostly one reading per hour at :50, sometimes an extra one at :20, sometimes none.
- `data/p1_zone_load_hourly_synthetic.csv` — hourly load by zone, **UTC**, long format: `delivery_start_utc`, `zone`, `load_mw` (average MW over the hour).
- `data/p1_zones_reference_synthetic.csv` — one row per zone: description, station, `hdd_base_c`, `cdd_base_c`.

### What to find out

One row per **zone × local market day** with the day's mean temperature, its heating and cooling degree days, and its load both as **average MW** and as **energy (MWh)** — with blanks where the day is not covered well enough.

### Minimum theory

- **Frequencies.** Irregular readings → regular hourly means first (`floor("h")` then a mean), then the day. Averaging raw readings would give extra weight to the hours with two readings.
- **Market day.** Group by the local calendar day of the market (`Europe/Paris`), not by the UTC date: 23:00 UTC on 1 January is 00:00 on 2 January in the market. Floor in UTC, convert, then label.
- **Degree days** (base temperatures per zone): `HDD = max(hdd_base − T_mean, 0)` — how far the day was *below* the heating threshold; `CDD = max(T_mean − cdd_base, 0)` — how far *above* the cooling threshold. Both are ≥ 0, in °C·day.
- **Average MW vs MWh.** Average MW = mean of the hourly MW of the day; MWh = average MW × hours in the day — 23, 24 or 25.
- **Coverage rules.** A daily mean from too few hours is worse than a blank.

### Assumptions

- Temperatures outside [−40, 50] °C are sensor codes: drop them.
- A day's temperature needs **≥ 18** hourly values; a day's load needs **≥ 90 %** of its hours. Otherwise the value is `NaN`.
- Hours in a local day: the time between its local midnight and the next one (both localised to `Europe/Paris`).

### Your task

Implement `daily_zone_table(temps, load, zones)`:

1. Temperatures: parse UTC, drop impossible values, floor to the UTC hour, mean per (zone, hour); add `local_date`; per (zone, local_date): `temp_mean_c` and `temp_hours` (count); blank `temp_mean_c` below 18 hours.
2. Merge the zone bases; `hdd`, `cdd` with `clip(lower=0)`.
3. Load: parse UTC, add `local_date`; per (zone, local_date): `load_avg_mw` (mean) and `load_hours` (count); `hours_in_day`; blank `load_avg_mw` below 90 % coverage; `load_mwh = load_avg_mw × hours_in_day`.
4. Outer-merge temperature and load on (`zone`, `local_date`), sort by zone and date, reset the index.

Columns, in this order: `zone`, `local_date`, `temp_mean_c`, `temp_hours`, `hdd_base_c`, `cdd_base_c`, `hdd`, `cdd`, `load_avg_mw`, `load_hours`, `hours_in_day`, `load_mwh`. Then the **Explain** tab.
