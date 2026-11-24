> **Synthetic data** — monthly US oil demand estimates with an invented revision pattern (first estimate, second estimate, annual revision).

### The desk asks

> “We've been explaining WTI moves with the demand growth in our database. Someone told me those numbers weren't the ones we had at the time. What did we actually know about demand on a given day — and how different was it?”

### What you have

`data/p3_us_oil_demand_vintages_synthetic.csv` — one row per **month × vintage**: `obs_month` (the month described), `vintage_date` (when that estimate was published), `demand_kbd`. Each month has a first estimate (end of month + 2), a second (one month later) and an annual revision (the following August).

### What to find out

For any decision date: the latest month the desk could know, the value it saw, the value the database shows today, and the year-on-year growth under both.

### Minimum theory (PDF A04-D, A04-E)

- **Vintage**: one published version of a value. The database usually keeps only the last one.
- **As-of view** at date d: for each month, the latest vintage published before d. The **latest available month** is the most recent month with at least one vintage before d.
- **Genuine point-in-time**: built from vintages. **Pseudo point-in-time**: final values shifted by the publication lag — the timing is right, the revisions are ignored.
- Without vintages, a backtest overstates what was knowable; quantify the typical revision and say so.

### Assumptions

A vintage dated D is usable from D + 1 day (`vintage_date < decision_date`). Growth = value of the latest month / value of the same month one year earlier − 1, both **as known at the decision date** (and both final, for the final growth).

### Your task

Implement `known_at(vintages, decision_dates)` returning one row per decision date with `decision_date`, `latest_month`, `demand_known_kbd`, `demand_final_kbd`, `growth_known_pct`, `growth_final_pct`:

1. Parse `vintage_date`; `final` = the last vintage of each month.
2. For each decision date: keep the vintages published before it; the latest vintage of each month; the latest month; its value and the value 12 months earlier → growth known.
3. The same month in `final` → final value and final growth.

Then compare pseudo and genuine point-in-time in the Test code pad and answer in the **Explain** tab.
