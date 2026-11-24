> **Synthetic data** — simulated with fixed seeds; publication schedule and revision pattern are realistic, values are invented.

### Context

Monthly US oil demand (product supplied, kb/d) is published with a delay and **revised**: a first estimate about two months after the month, a second estimate a month later, and an annual revision the following August. Your file `data/p3_us_oil_demand_vintages_synthetic.csv` keeps every version — one row per `obs_month` × `vintage_date`, with `demand_kbd`.

### Objective

Reconstruct, for any past date, the demand history **as it was known on that date**.

### Minimum theory (PDF, A04-D)

- A **vintage** is the version of a value published at a given date. A **vintage table** (long format) stores all of them.
- **As-of view at t**: keep the rows with `vintage_date ≤ t`, then for each month take the **latest** estimate. This is exactly what an analyst saw on date t.
- The "latest" history downloaded today = the as-of view at today's date: revised values, indexed by observation month, **with no trace of the publication lag**.

### Assumptions

Vintage dates are the publication dates; values are usable from that day on.

### Your task

Implement `as_of(vintages, as_of_date)`:

1. Copy; convert `obs_month` (`format="%Y-%m"`) and `vintage_date` to datetimes.
2. Keep the rows with `vintage_date ≤ as_of_date`.
3. Sort by `vintage_date`, group by `obs_month`, take the `last()` `demand_kbd`.

Return the `pd.Series` indexed by `obs_month` (name `demand_kbd`). Answer in the **Explain** tab.
