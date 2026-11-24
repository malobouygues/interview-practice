### A. Reasoning — the crack is only as good as its two legs

A crack spread subtracts two prices. If either leg is in the wrong unit, stale, or from another day, the spread is wrong in a way that looks like a market move. So before asking whether the crack widened, make sure every number is a USD/bbl settlement of the right product on the right date — and know exactly where numbers are missing.

### B. Theory (PDF A01-B structure, A02-C quality, A03 cleaning order)

- **Key and duplicates**: an exact copy is noise; two values for one key is a conflict that needs a rule (latest version, preferred source…) — or a stop.
- **Order of operations** (A03-C): types → key → units → frozen values/outliers → missing values last. Outlier detection on mixed units would flag 1,009 ULSD rows.
- **Density conversions**: a tonne of gasoil is ≈ 7.45 barrels, a tonne of jet ≈ 7.88 — the factor is product-specific.
- **Long vs wide**: long is how vendors store; wide is how you compute spreads. The pivot is where absent rows become visible `NaN`.
- **Gap treatments** (A03-A): the right one depends on *why* the value is missing (holiday, not yet born, not yet published, frozen feed) and on what the variable is.

### C. Implementation

`map` on the unit column gives the factor; a boolean mask fixes the per-tonne rows with the product's density. `pivot` reshapes. A run of identical values is found with `same = s == s.shift(1)`, `run_id = (~same).cumsum()`, `run_length = s.groupby(run_id).transform("count")`. Cracks are plain subtractions, so `NaN` propagates — on purpose.

### D. Interpretation (this dataset)

- 7,893 rows → 3 copies → 7,890 unique `(date, product)` → **1,671 dates**.
- ULSD: **1,009** rows in USc/gal (to end-2020), 627 in USD/gal.
- Gaps after the pivot: Brent 32, gasoil 37 (incl. 5 frozen), ULSD 36, RBOB 36, jet 329 (starts 1 Mar 2018, last 3 days unpublished). ULSD crack: 68 gaps (US *or* UK holiday).
- Frozen gasoil 8–15 Oct 2018: October mean gasoil crack **17.98** on 18 days with the run blanked; **18.56** with an unlimited forward fill.
- Dropping incomplete dates keeps **1,308 / 1,671** (all of 2017 lost because jet did not exist yet).
- Annual mean gasoil crack: 13.0 (2017), 16.1 (2019), 4.5 (2020), **35.4 (2022)**, 27.7 (2023 H1) — the widening is visible. RBOB 2019 shows **45.0**: one unit error (8,732 $/bbl on 14 May 2019) is still inside.

### E. Decision

Keep the table with gaps blank and cracks only where both legs exist. Do not interpret any crack level yet: one obvious unit error is present and the extreme values have not been investigated (2.3).

### F. Pitfalls and limits

- `drop_duplicates(subset=["date", "product"])` would have silently kept one of two conflicting prices — the assertion makes the conflict visible.
- Forward-filling Brent over UK holidays computes ULSD cracks against yesterday's Brent: 30 such cracks here.
- The frozen-run rule (≥ 4) can blank a genuinely flat market — rare for daily settlements, but possible for illiquid assessments.
- The densities are standard approximations; contract specifications vary slightly.

### G. Interview defence

*“Why not simply drop the rows with missing data?”* — Because the gaps are not random: jet didn't exist before March 2018, holidays differ between London and New York, the last days are not yet published. Dropping incomplete dates throws away 22 % of the history and all of 2017 for a question about diesel, where jet is irrelevant. I keep gaps visible and compute each spread where its own two legs exist.
