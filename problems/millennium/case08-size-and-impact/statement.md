**Desk context**

Filling a big order for an illiquid asset pushes the price, and the push accumulates across back-to-back requests — the thinner the asset, the harder it moves. Quote a sequence of requests in one asset, carrying that impact forward.

**Problem**

Implement `quote_stream_with_impact(reference, requests_for_asset, liquidity_score, impact_params)` which returns the list of quoted prices (one per request, rounded to 9 dp). `requests_for_asset` is a list of `{'side', 'quantity'}`. Carry a running offset starting at 0.

**Rules**

- Quote off `reference + offset` : `+ half_spread` for BUY, `- half_spread` for SELL.
- After each request: `offset += k * signed_qty * (1 - liquidity_score + 1e-6)`, then `offset *= decay`.
- `signed_qty` is `+quantity` (BUY) or `-quantity` (SELL); `impact_params` has `half_spread`, `k`, optional `decay`.

**Constraints**

- Order matters: each fill shifts the base for the next quote. numpy available.

**Sample I/O**

```python
quote_stream_with_impact(20.0, [{'side':'BUY','quantity':2500}]*3, 0.0,
                         {'half_spread':0.1,'k':2e-5,'decay':0.9})
-> [20.1, 20.145000045, 20.185500086]
```

**Notes**

- A liquid asset (score ~1) barely moves; an illiquid one (~0) moves a lot.
