**Desk context**

Cap how much you hold, far less for an illiquid asset, and lean your quotes back toward flat. For each request, decide accept, widen, or reject.

**Problem**

Implement `decide_request(inventory, request, liquidity_score, params)` which returns `{'action': 'accept'|'widen'|'reject', 'quote': float|None}`. `request` carries `asset`, `side`, `quantity`, `reference`, `half_spread` ; `params` has `base_limit`, `soft_frac`, `skew_coeff`.

**Rules**

- `hard = base_limit * liquidity_score`, `soft = soft_frac * hard`.
- `signed = -quantity` (BUY) / `+quantity` (SELL); `projected = inventory.get(asset, 0) + signed`.
- If `abs(projected) > hard` => reject (quote is `None`).
- Else quote with `skew = -skew_coeff * inventory.get(asset, 0)` : BUY `reference + half_spread + skew`, SELL `reference - half_spread + skew`. If `abs(projected) > soft` => action `'widen'` and add an extra `half_spread` (+ for BUY, - for SELL); else `'accept'`. Round quote to 6 dp.

**Constraints**

- `inventory` may omit the asset (treat as 0).

**Sample I/O**

```python
decide_request({'Asset_1':0},
               {'asset':'Asset_1','side':'BUY','quantity':100,'reference':100....},
               1.0, {'base_limit':50000,'soft_frac':0.6,'skew_coeff':0.0001})
-> {'action':'accept','quote':100.05}
```

> *Note : la ligne du request est coupée au bord droit dans la photo source ; la valeur de reference et le champ half_spread ne sont pas entièrement lisibles.*

**Notes**

- The position cap scales with liquidity, so the illiquid name fills up (and starts rejecting) far sooner.
