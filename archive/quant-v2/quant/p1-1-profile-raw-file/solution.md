### A. Reasoning — why profile before cleaning

Cleaning code written before looking at the file encodes guesses: "drop duplicates" (which ones?), "convert to float" (it fails on `HOL`), "parse dates" (day or month first?). Profiling turns each guess into an observed fact with a count, and each fact becomes one explicit line in the loader of step 1.2.

### B. Theory

- **Type inference**: one non-numeric token makes a column text (`str` in pandas 3, `object` before).
- **Duplicates**: `duplicated()` compares whole rows; `duplicated(subset=["Date"])` compares dates. The difference between the two counts is the number of dates sent twice *with different values*.
- **Dates**: `pd.to_datetime(s, format="%d/%m/%Y")` is explicit; without a format pandas may read 03/04/2020 as 4 March.
- **Missing-value codes** carry meaning: a holiday (structural) is not a delivery failure (accidental). The PDF's rule: identify the cause of a missing value before choosing a treatment.

### C. Implementation

{{code}}

### D. Interpretation (this file)

| finding | value | consequence for the loader |
|---|---|---|
| rows | 790 | — |
| all columns read as text | `str` | declare `na_values=["HOL", "-"]` |
| identical rows | 5 | `drop_duplicates()` |
| repeated dates | 7 → 2 corrections | keep the latest `loaded_at` for a date |
| codes | Brent: `HOL`; WTI and Dubai: `-`, `HOL` | two kinds of missing value |
| dates in order | **False** | sort after parsing |
| range | 2019-01-02 → 2021-12-31 | three years, business days |

`df.head()` shows five clean-looking rows: none of these problems is visible in it.

### E. Decision

Each finding maps to one line of `load_crude_prices` (step 1.2): `na_values`, explicit date format, drop identical rows, resolve corrections by `loaded_at`, sort, assert one row per date.

### F. Pitfalls and limits

- Letting pandas guess date formats on day-first strings.
- Calling `drop_duplicates()` and believing the problem is solved: it does not handle a date sent twice with different values.
- Converting with `pd.to_numeric(errors="coerce")` **without** recording which codes became `NaN`: you lose the difference between a holiday and a delivery failure.
- A profile is a snapshot: re-run it on every new delivery.

### G. Interview defence

> **Q: "You receive a new price file. What do you do before any analysis?"**
>
> **A:** I write down what one row is — here one business day's settlement of three crude benchmarks in dollars per barrel, each with its own exchange, close and holiday calendar — and then I profile the raw file as it comes. On this file that showed text columns because of vendor codes, five days loaded twice, two dates re-sent with corrected values, day-first dates and a late batch appended at the end. Each of those becomes one explicit step in the loader, and I can count what each step changed.
