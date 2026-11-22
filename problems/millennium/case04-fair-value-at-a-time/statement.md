**Desk context**

Client requests arrive at arbitrary times that don't line up with your price dataset, so to quote you need the asset's reference price as of the request time. And you must refuse to quote when the most recent print is too old to trust, which may happen for an illiquid asset with all its gaps.

**Problem**

Implement `reference_price(prices, asset, ts, max_staleness_minutes)` which returns `{'price': <float or None>}`.

**Rules**

- `price` is the most recent valid (non-NaN, > 0) value of `asset` at or before `ts`.
- If no valid price exists at or before `ts`, `price` is `None`.
- If the last valid print is older than `max_staleness_minutes` before `ts`, `price` is `None`.
- Do the lookup efficiently: a sorted as-of lookup, not a per-call scan.

**Constraints**

- `ts` is a timestamp (string or `pd.Timestamp`). pandas available.
- Always return a dict with the single key `price`.

**Sample I/O**

```text
reference_price(prices, 'Asset_3', ...)
reference_price(prices, 'Asset_3', ...)
```

> *Note : le Sample I/O est incomplet dans la photo source (bord droit de l'écran hors cadre).*

**Notes**

- This is where the illiquid asset starts behaving differently, straight from the data.
