> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

The products file has gaps everywhere: US and UK holidays on different days, a jet series that starts in March 2018, three days not yet published at the end, a gasoil feed that froze for a week in October 2018, and two dates delivered twice. Every later statistic (returns, rolling features, correlations) depends on how these are handled.

### Objective

Apply an explicit, defensible treatment to each kind of gap and keep a trace of every imputed value.

### Minimum theory

| gap | example | treatment |
|---|---|---|
| leading | jet before March 2018 (series not born) | leave missing |
| trailing | last days not yet published (ragged edge) | leave missing |
| short interior | one exchange closed for a holiday | carry the last price, **at most 2 days**, flagged |
| stale run | the same price 4+ days in a row (frozen feed) | keep the first, the copies are missing |

- `ffill(limit=2, limit_area="inside")` fills at most two consecutive values and only between two valid prices.
- **Never** `bfill()` or interpolation in a research dataset: both use the *next* price, i.e. the future.

### Assumptions

A liquid futures price never settles at exactly the same value four days running; two days of carried-forward price is acceptable for daily research.

### Your task

Implement `treat_gaps(products)` for the raw `DataFrame` indexed by date. Return a `dict`:

1. Keep **one row per date** with `products[~products.index.duplicated(keep="first")]`, sorted by date.
2. For each column, a run of **4 or more identical consecutive values**: keep the first, set the others to `NaN` (hint: `same_as_previous = s == s.shift(1)`; a run id is `(~same_as_previous).cumsum()`; its length is `s.groupby(run_id).transform("count")`).
3. `treated = prices.ffill(limit=2, limit_area="inside")`.
4. Return `{"prices": treated, "filled": prices.isna() & treated.notna()}` — `prices` being the frame after steps 1–2.

The result is provided as `data/p2_products_treated_synthetic.csv` for the next steps. Answer in the **Explain** tab.
