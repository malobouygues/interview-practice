**Desk context**

Some clients trade right before the market moves your way; others trade right before it moves against you. The second kind are **toxic** — every time you fill them you're taking a considerable amount of risk. The desk quantifies this with **markout**: the mark-to-market PnL of each fill measured a fixed horizon later, from the market maker's side. Aggregate it per client and you can see whose flow to widen on.

**Problem**

Implement `client_markout(fills, prices, horizon_minutes)` returning `{client_id: {'avg_markout': float, 'toxic': bool}}`.

The market maker takes the **opposite** side of the client. For each fill, measure the MM's PnL `horizon_minutes` after the trade, using the asset's price at (or most recently before) that future time.

**Formula**

- `P_h` = the asset's price **as-of** (fill timestamp + `horizon_minutes`).
- Client BUY (MM sold): `markout = (fill_price - P_h) * quantity`.
- Client SELL (MM bought): `markout = (P_h - fill_price) * quantity`.

Per client, average the markout over their fills (round to 6 dp). A client is **toxic** when their average markout is negative, i.e. the MM loses on their flow.

**Rules**

- `fills` columns: `client_id`, `timestamp`, `asset`, `side`, `quantity`, `fill_price` (`side` is the client's direction).
- `prices` is the clean tape (`timestamp` + one column per asset). Use an **as-of** lookup for `P_h` (most recent price at or before fill time + horizon). If the horizon runs past the end of the tape, use the last available price.

**Constraints**

- pandas available. Every fill's asset appears in `prices`.

**Sample I/O**

```python
# Asset_1 is rising: a client who BUYS (MM ends up short) is toxic;
# one who SELLS is benign
client_markout(fills, prices, 5)
-> {'CLIENT_A': {'avg_markout': -50.0, 'toxic': True},
    'CLIENT_B': {'avg_markout': 50.0, 'toxic': False}}
```

**Notes**

- Markout is from the **market maker's** perspective: a negative number means the client picked you off.
