> **Synthetic data** — a fictional Central-European power market, simulated with fixed seeds. Not market observations.

### The desk asks

> “Half the solar column is empty, some hours have no wind and the capacity column is almost blank. I need residual load (load minus wind minus solar) and the capacity margin. Can't you just forward-fill everything?”

### What you have

`data/p1_power_hourly_clean_synthetic.csv` — the output of 1.1: one row per delivery hour, indexed by `delivery_start_utc`, with `local_date`, `local_hour`, `price_eur_mwh`, `load_mw`, `wind_mw`, `solar_mw`, `available_capacity_mw`, `gas_eur_mwh`. The loader in the Test code pad rebuilds the UTC index.

### What to find out

For each variable, whether a blank is **structural** (the calendar or a reporting convention), a **failure** (data that should exist), or a **state** that legitimately stays valid for a while — and treat it accordingly.

### Minimum theory (PDF A03-A, arbre B)

- Missingness has a cause: position (start, middle, end), regularity (every night?), simultaneity across series. **Structural** blanks follow a rule; **failures** are irregular.
- A blank that means zero should become 0. A failure stays `NaN`, with a flag, so later steps can exclude or test it.
- `ffill(limit=n)` carries the last value for at most `n` rows. Only for a **state** variable (a level that holds until it changes), never for a flow or a price. Keep the **age** of the carried value: `capacity_age_h`.
- `groupby([...]).transform("median")` returns, on every row, a statistic of that row's group — here “how much solar does this hour of this month normally produce?”.

### Assumptions

- The vendor leaves `solar_mw` blank when output is zero. An hour is “daylight” if the median solar output of that **month × UTC hour** (blanks counted as 0) exceeds 500 MW. Group by the UTC hour: the sun ignores the clock change.
- Capacity is sent once a day, with the first hour of the local day. A value may be carried for **48 hours** at most; it is stale when it was sent on an **earlier local day**. (An age limit of 24 hours would not work: on the 25-hour October day, the last hour is 24 hours after a report that is still that day's.)
- Wind and price are never filled.

### Your task

Implement `treat_gaps(hours)` (work on a copy):

1. `solar_missing` = solar blank **and** daylight hour. Set the other solar blanks to 0.
2. `wind_missing` = wind blank (leave the values as they are).
3. `capacity_age_h` = hours since the last non-blank capacity (time of the row minus time of the last report, in hours).
4. Forward-fill `available_capacity_mw` with `limit=48`; `capacity_is_stale` = the local date of the last report is before the row's `local_date`.
5. Leave `price_eur_mwh` untouched. Return the frame with the four new columns.

Then answer the trader in the **Explain** tab.
