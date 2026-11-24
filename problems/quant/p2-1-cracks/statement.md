> **Synthetic data** — prices simulated with fixed seeds; product names and units are realistic, the values are not observations.

### The desk asks

> “The diesel crack has widened materially — gasoil trades twenty-odd dollars over Brent more than it did a couple of years ago. Is that a tighter physical market, or are we looking at a data problem? Start by putting the crack history on one sheet. The vendor sends everything in one long file, and the units are all over the place.”

### What you have

`data/p2_products_daily_long_synthetic.csv` — one row per **date × product**: `date`, `product` (`brent`, `gasoil`, `ulsd`, `rbob`, `jet`), `unit`, `price`. 2017-01 to 2023-06.

| product | what it is | unit(s) in the file |
|---|---|---|
| brent | crude benchmark | USD/bbl |
| gasoil | European diesel (ICE Gasoil) | USD/t |
| ulsd | US diesel (NY Harbor ULSD) | USc/gal until end-2020, USD/gal after |
| rbob | US gasoline | USD/gal |
| jet | jet fuel, NW Europe | USD/t |

### What to find out

A daily table, one row per date, with every price in **USD/bbl** and the **crack** of each product against Brent — and a clear view of where the gaps are and why.

### Minimum theory (PDF A01-B, A02-C, A03-A/C)

- **Key**: the columns that identify a row. Here `(date, product)`. Exact copies can be dropped; two *different* prices for one key cannot be resolved silently.
- **Units before anything else**: 1 bbl = 42 gal; cents → dollars ÷ 100; tonnes → barrels with the product's density (gasoil ≈ 7.45 bbl/t, jet ≈ 7.88 bbl/t). Convert **row by row** from the `unit` column.
- **Long → wide**: `pivot(index="date", columns="product", values=...)`. A missing row becomes a `NaN` cell.
- **Frozen feed**: the same settlement repeated for several sessions is not a market; keep the first value, blank the copies.
- **Crack spread** = product price − crude price, both in USD/bbl: the refining margin of that product.
- **Gaps**: *leave* (honest, loses the day), *drop* incomplete dates (loses every day one series is missing), *forward-fill* (invents a value: one day may be defensible for a state, never for a whole frozen run).

### Assumptions

A run of **4 or more** identical consecutive prices in one series is a frozen feed. Nothing is filled at this stage.

### Your task

Implement `build_daily_table(raw)`:

1. Parse `date`; drop exact duplicate rows; `assert` that `(date, product)` is now unique.
2. `usd_bbl` = price × factor, with factors `USD/bbl` 1, `USD/gal` 42, `USc/gal` 0.42, and for `USD/t` 1 / (bbl per tonne of that product). Assert every row got a factor.
3. Pivot to wide (index `date`), columns in the order `brent`, `gasoil`, `ulsd`, `rbob`, `jet`.
4. In each column, blank the 2nd, 3rd… values of every run of ≥ 4 identical consecutive prices.
5. Add `gasoil_crack`, `ulsd_crack`, `rbob_crack`, `jet_crack` = product − brent.

Return the wide frame (index `date`). Compare the gap treatments in the Test code pad, then the **Explain** tab.
