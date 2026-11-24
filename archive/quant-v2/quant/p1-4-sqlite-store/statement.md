> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

The desk wants the clean crude prices in a small local database, so that anyone can re-run the load safely and query it. No server, no framework: a SQLite file (here in memory) is enough for a research project. The first query: **monthly average Brent–WTI and Brent–Dubai spreads**.

### Objective

Store the clean prices with a structure that makes duplicates impossible and reloads harmless, then aggregate with SQL.

### Minimum theory

- `PRIMARY KEY (date)`: at most one row per date, enforced by the database.
- `INSERT OR REPLACE`: if the date exists, replace the row — re-running the load gives the same table (**idempotent**). A plain `INSERT` would fail or duplicate.
- A spread between two prices in the same unit is a price difference (USD/bbl): aggregate it by **averaging** (or taking the last value), never by summing.
- `NaN` from pandas is stored as `NULL`; SQL averages ignore `NULL`, so filter explicitly to compare like with like.

### Assumptions

The input is the clean dataset of step 1.3 (`data/p1_crude_prices_clean_synthetic.csv`): one row per date, the ×10 print removed, the negative WTI print kept.

### Your task

Implement `monthly_spreads_sql(prices)` with the standard library `sqlite3`:

1. Create an in-memory database and a table `crude_prices (date TEXT PRIMARY KEY, brent REAL, wti REAL, dubai REAL)`.
2. Insert every row (date as `"YYYY-MM-DD"`) with `INSERT OR REPLACE` — **twice** (to prove the load is idempotent).
3. Query, for days where all three prices exist: `month` (`substr(date, 1, 7)`), `brent_wti = AVG(brent - wti)`, `brent_dubai = AVG(brent - dubai)`, `n_days = COUNT(*)`, grouped and ordered by month.
4. Return the result as a `DataFrame` (`pd.read_sql_query`).

Then answer in the **Explain** tab.
