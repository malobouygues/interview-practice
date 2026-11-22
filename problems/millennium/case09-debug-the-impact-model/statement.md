A market-making desk quotes a stream of client requests for the same asset. Each fill pushes the market, so the desk carries a running **market-impact** state that biases the next quote and slowly mean-reverts. The quoting engine below was meant to implement this, but the impact quotes **drift on multi-order sequences**: single quotes look fine, yet once several requests arrive in a row the numbers wander off. Diagnose and fix it.

**What You Need To Do**

Implement `quote_impact_stream(reference, impact_params, liquidity_score, requests_for_asset)` so it returns the **list of quote prices**, one per request, exactly matching the model below. A buggy implementation is provided as your starting point. Find and fix what makes multi-order sequences drift.

**Input**

Arguments:

| Key | Type | Meaning |
|---|---|---|
| `reference` | float | The fair reference price R for the asset |
| `impact_params` | dict | `{"k": float, "decay": float, "half_spread": float}` |
| `liquidity_score` | float | L in [0, 1]. 1 = perfectly liquid (impact contribution ~0); 0 = fully illiquid (full impact) |
| `requests_for_asset` | list | Ordered requests, each `{"side": "BUY"...}` |

**Output**

A list of float quote prices, one per request, **in request order**.

**The Impact Model (follow this exactly)**

Maintain a single signed running state `accumulated_impact`, starting at 0.0. It is **positive** under net buying pressure and **negative** under net selling pressure, and it mean-reverts toward zero between requests.

For each request, **in order**:

**1. Signed spread**: `signed_spread = +half_spread` for a BUY, `-half_spread` for a SELL.

**2. Quote** (uses the state as it stands *before* this order):

```text
quote = reference + signed_spread + accumulated_impact
```

**3. Add this order's impact to the state**, let `side_sign = +1` for BUY, `-1` for SELL:

```text
impact_term = k * quantity * (1 - liquidity_score)
accumulated_impact = accumulated_impact + side_sign * impact_term
```

**4. Mean-revert the state**, multiply the **whole accumulated state** by `decay` *before the next request*:

```text
accumulated_impact = accumulated_impact * decay
```

**5. Record** `quote` and move to the next request.

Return the list of recorded quotes.

**Worked Example**

`reference = 200.0`, `k = 0.01`, `decay = 0.5`, `half_spread = 0.0`, `liquidity_score = 0.0`, three BUYs of quantity 100 :

| # | quote (uses state before order) | impact_term | state after add | state after decay |
|---|---|---|---|---|
| 1 | 200.0 + 0 + 0.0 = 200.0 | 0.01\*100\*1 = 1.0 | 0 + 1.0 = 1.0 | 1.0\*0.5 = 0.5 |
| 2 | 200.0 + 0 + 0.5 = 200.5 | 1.0 | 0.5 + 1.0 = 1.5 | 1.5\*0.5 = 0.75 |
| 3 | 200.0 + 0 + 0.75 = 200.75 | 1.0 | 0.75 + 1.0 = 1.75 | 1.75\*0.5 = 0.875 |

Result: `[200.0, 200.5, 200.75]`.

*A common wrong implementation decays only the new order's term rather than the whole state, double-counts the spread on the very first quote, or forgets that liquidity scales the impact; any of these makes the third quote (and beyond) drift.*

**Notes**

- Quote at step n must reflect the state **before** order n's own impact is added (the first quote therefore carries no impact).
- `liquidity_score = 1` makes every `impact_term` zero, so the state never moves; quotes are just reference ± half_spread.
- Outputs are compared element-wise as a list (rounded to 9 dp), so ordinary floating-point arithmetic is fine.
