> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

Step 1.1 found the problems of `data/p1_crude_prices_vendor_synthetic.csv`: text codes in the price columns, day-first dates, rows out of order, five days loaded twice and two dates re-sent with corrected values. Now write the loader the rest of the project will rely on.

### Objective

Turn the raw export into a typed, chronological, one-row-per-date `DataFrame` — with every decision visible in the code.

### Minimum theory

- `pd.read_csv(path, na_values=[...])` declares which text codes mean "missing".
- `pd.to_datetime(column, format="%d/%m/%Y")` parses day-first dates without guessing.
- `drop_duplicates()` removes identical rows; `drop_duplicates(subset="date", keep="last")` keeps one row per date — the **last one in the current order**, so the order must first be made meaningful.
- A **correction** is a later delivery of the same date: the row with the latest `loaded_at` is the vendor's final word.

### Assumptions

`HOL` and `-` are the only codes; `loaded_at` is reliable; missing prices stay missing (no filling in the loader).

### Your task

Implement `load_crude_prices(path)`:

1. Read the CSV with `na_values=["HOL", "-"]`.
2. Rename the columns to `date`, `brent`, `wti`, `dubai` (keep `loaded_at`).
3. Parse `date` with `format="%d/%m/%Y"` and `loaded_at` with `pd.to_datetime`.
4. Drop identical rows.
5. Sort by `date` then `loaded_at`, and keep the **last** row for each date.
6. Index by `date`, keep the columns `brent`, `wti`, `dubai` (floats), and assert that the index is unique and increasing.

Return the `DataFrame`. Then answer in the **Explain** tab.
