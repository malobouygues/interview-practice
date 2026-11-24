> **Synthetic data** — simulated with fixed seeds; dates, units and calendars are realistic, the values are not market observations.

### Context

You join a crude desk. A data vendor sends `data/p1_crude_prices_vendor_synthetic.csv`: three years (2019–2021) of daily settlements for **Brent** (ICE, London close), **WTI** (NYMEX, New York close) and **Dubai** (a Middle East sour assessment, Singapore close), all in **USD/bbl**, plus a `loaded_at` column (when each row was loaded into the vendor's export).

The vendor's note says: *"HOL = exchange holiday. – = value not available."*

Nothing you compute later can be better than this file. The first job is to **look at it as it really is** — before telling pandas what it should be.

### Objective

Write a function that profiles the raw file and reports every structural problem you will have to handle in step 1.2.

### Minimum theory

- `pd.read_csv(path)` *guesses* types. A single text code in a price column ("HOL") turns the whole column into text.
- **Identical duplicate rows** (the same day loaded twice) are not the same problem as **a repeated date with different values** (a correction, or two sources).
- Dates written `dd/mm/yyyy` are ambiguous for pandas (03/04/2020 could be 3 April or 4 March): always parse them with an explicit format.
- A **data dictionary** records, for each column: meaning, unit, source, frequency, calendar, and the meaning of missing values and zeros.

### Assumptions

The vendor's codes are the only text values in the price columns; `loaded_at` is reliable.

### Your task

Implement `profile_raw_file(raw)`, where `raw = pd.read_csv(path)` read **without any option**. Return a `dict`:

| key | content |
|---|---|
| `n_rows` | number of rows (int) |
| `dtypes` | `{column: str(raw[column].dtype)}` for every column |
| `exact_duplicate_rows` | number of rows identical to an earlier row (`raw.duplicated()`) |
| `repeated_dates` | number of rows whose `Date` already appeared earlier |
| `non_numeric_codes` | for each of the three price columns, the **sorted list** of distinct values that `pd.to_numeric(..., errors="coerce")` cannot convert |
| `dates_in_order` | whether the dates, parsed with `format="%d/%m/%Y"`, are increasing |
| `first_date`, `last_date` | earliest and latest parsed date as `"YYYY-MM-DD"` |

Do not modify `raw`. Then write the data dictionary in the **Explain** tab.
