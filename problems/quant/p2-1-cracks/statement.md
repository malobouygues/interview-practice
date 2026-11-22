> **Synthetic data** — simulated with fixed seeds; seasonal patterns and a hurricane-type shock are imitated, values are invented.

### Context

You move to the oil-products desk. The research question of this project: **what moves the US diesel crack, and which explanatory variables can be built from imperfect product data without look-ahead?** The daily file `data/p2_products_daily_synthetic.csv` (2017–2019) contains, each in its **trading unit**:

| column | market | unit |
|---|---|---|
| `brent_usd_bbl` | ICE Brent | USD per barrel |
| `ulsd_usd_gal` | NYMEX ULSD (diesel / heating oil) | USD per US gallon |
| `rbob_usd_gal` | NYMEX RBOB (gasoline) | USD per US gallon |
| `gasoil_usd_t` | ICE Gasoil (European diesel) | USD per metric tonne |
| `jet_usd_t` | NWE jet fuel | USD per metric tonne |

A **crack spread** is the price of a product minus the price of crude: the gross margin of refining that product.

### Objective

Convert every product to USD/bbl and compute the main cracks.

### Minimum theory

- 1 barrel = **42 US gallons**. Mass → volume depends on density: about **7.45 bbl per tonne** of gasoil/diesel, **7.88 bbl/t** of jet.
- `diesel crack = ULSD×42 − Brent`, `gasoline crack = RBOB×42 − Brent`, `gasoil crack = gasoil/7.45 − Brent`, `jet crack = jet/7.88 − Brent`.
- **3-2-1 crack** = (2 × gasoline + 1 × diesel − 3 × crude) / 3: a refinery's margin per barrel of crude.

### Assumptions

Brent is the crude reference for every crack (a simplification for US products, often quoted against WTI). Conversion factors are standard averages.

### Your task

Implement `crack_spreads(products)` for a `DataFrame` indexed by date with the five columns above. Return a `DataFrame` with the same index and the columns `diesel_crack`, `gasoline_crack`, `gasoil_crack`, `jet_crack`, `crack_321` (USD/bbl). Missing inputs give missing cracks.

The raw file has two dates delivered twice: the test code keeps one row per date before calling you (step 2.2 explains why `drop_duplicates()` is the wrong tool here). Answer in the **Explain** tab.
