Our market-making desk prices a two-sided quote for every incoming request, then nudges it to manage inventory and refuses anything that would breach our position limits. The logic (`price_quote`) has shipped and mostly looks fine. But over the last week two things have gone wrong: our **inventory skew is making our book worse, not better** (we keep adding to positions we already hold), and we are **taking trades right at the risk cap that we should be turning away**. Find out where the quoter diverges from the desk's rules and fix it.

**The Job**

`price_quote(data)` already ships (it is in the editor). It is **supposed** to satisfy the spec below exactly. It does not. Diagnose where it diverges and repair it so that it meets the contract for every request, not just the easy ones.

**The Contract**

You receive one quote request and the desk's current state. Decide what to do and, if you quote, at what price. Apply the rules **in this order**:

**1. Projected inventory.** Work out the position you would hold *after* this trade:

```text
projected = current_inventory(asset) + signed_quantity
```

where `signed_quantity = +quantity` for a BUY and `-quantity` for a SELL. A BUY adds to inventory; a SELL subtracts. All risk decisions are made against this **post-trade** position, not the position you hold now.

**2. Limits.**

```text
hard_limit = base_limit
soft_limit = soft_frac * hard_limit
```

- If `abs(projected) >= hard_limit` → **reject** the request. Return `quote = null`, `action = "reject"`. (A trade landing *exactly on* the cap is a breach and must be refused.)
- Else if `abs(projected) > soft_limit` → **widen** (we still quote, but defensively). `action = "widen"`.
- Else → **accept**. `action = "accept"`.

**3. The quote price.** Start from `reference` and apply the half-spread, then the inventory skew.

- A BUY is an **ask**: `reference + half`.
- A SELL is a **bid**: `reference - half`.
- `half = half_spread` on an **accept**, and `half = 2 * half_spread` on a **widen** (we double the half-spread to defend the book).

**4. Inventory skew.** We skew the quote to lean *against* the inventory we are already carrying, so that we discourage adding to it:

```text
skew = skew_coeff * current_inventory(asset)
```

The skew is computed off the inventory we hold **now** (pre-trade). Being **long** (positive inventory) must pull the quote **down**: a lower ask and a lower bid both make us less eager to buy and keener to sell. Being **short** (negative inventory) must pull the quote **up**. Concretely, on **both** sides:

```text
BUY  (ask): quote = reference + half - skew
SELL (bid): quote = reference - half - skew
```

Round the final quote to **4 decimal places**.

**Input Format**

`data` is a dict :

| Field | Type | Description |
|---|---|---|
| `params.soft_frac` | float | Soft-limit fraction of the hard limit |
| `params.base_limit` | float | The hard inventory limit (absolute units) |
| `params.skew_coeff` | float | Per-unit inventory skew coefficient |
| `request.side` | str | `"BUY"` or `"SELL"` |
| `request.asset` | str | Asset symbol, e.g. `"Asset_X"` |
| `request.quantity` | float | Requested trade size (positive) |
| `request.reference` | float | Reference (mid) price to quote around |
| `request.half_spread` | float | Base half-spread |
| `inventory` | dict | Map of asset to current signed position (long > 0, short < 0) |
| `liquidity_score` | float | Liquidity context for the asset (provided; not required by the contract) |

An asset with no entry in `inventory` is held flat (position 0).

**Output Format**

Return a dict :

```python
{"quote": <float rounded to 4 dp, or None>, "action": "accept" | "widen" | "reject"}
```

`quote` is `None` only when the request is rejected.

> *Note : dans le code fourni, la ligne `data = {...}` est coupée au bord droit dans la photo source ; la fin de la valeur `liquidity_score` n'est pas lisible. Elle est complétée ici par `liquidity_score}`.*
