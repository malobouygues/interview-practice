> **Synthetic data** — simulated with fixed seeds; not trade statistics.

### Context

Part of the diesel-crack story is physical: how much diesel Europe imports, and from where. `data/p2_diesel_imports_monthly_synthetic.csv` is a **long** table, one row per `month` × `importer` × `origin`, with `volume_kbd` in thousand barrels per day. The aggregator that publishes it writes `0` when a country **did not report** — and sometimes a country simply has no rows yet for the latest month.

### Objective

Build a wide monthly table of imports by country and a regional total that is never computed on missing reports.

### Minimum theory

- **Long** format: one observation per row, keys in columns — typical of downloads. **Wide** format: one column per series — typical of analysis. `groupby([...]).sum()` then `unstack()` goes from long to wide.
- **Flows** (barrels per day over a month) are **summed** across origins and countries; prices are averaged.
- **Missing ≠ zero**: a genuine zero is one origin with no cargo while the country reports others; a country at 0 from **every** origin in the same month did not report.
- `df.sum(axis=1, min_count=n)` returns `NaN` unless at least `n` values are present.

### Assumptions

A country never imports exactly zero from all four origins in a month: an all-zero month is a non-report.

### Your task

Implement `total_imports(imports)` for the long `DataFrame`:

1. Convert `month` with `pd.to_datetime(..., format="%Y-%m")` (work on a copy).
2. Sum `volume_kbd` by `month` and `importer`, then `unstack("importer")`: one row per month, one column per country (alphabetical order).
3. Replace exact zeros (a country at 0 from every origin) with `NaN`.
4. Add a column `total` = the sum across countries with `min_count` = number of countries.

Return the wide `DataFrame` (index = month). Answer in the **Explain** tab.
