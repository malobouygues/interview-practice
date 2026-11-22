**Desk context**

Keep an honest tally of your position, cash and what you're worth right now. The trap is the side: the market maker takes the opposite side of the client.

**Problem**

Implement `track_book(filled_requests, prices)` which returns `{'inventory': {asset: qty}, 'cash': float, 'pnl': float}`. `filled_requests` has columns `asset`, `side`, `quantity`, `fill_price` ; `prices` is a clean frame used to mark inventory at its last row.

**Rules**

- Start flat. Client BUY => maker sold: `inventory -= qty`, `cash += fill_price * qty`. Client SELL => maker bought: `inventory += qty`, `cash -= fill_price * qty`.
- `pnl = cash + sum(inventory[a] * last_price[a])`. Round cash and pnl to 6 dp.
- Inventory keys are the asset columns of `prices`.

**Constraints**

- pandas available. `filled_requests` may be empty (then the book is flat).

**Sample I/O**

```text
fills: BUY 100 @100.05 then SELL 100 @99.95 of Asset_1; marks at 100
track_book(...) -> {'inventory': {'Asset_1':0,'Asset_2':0,'Asset_3':0}, 'cash': ...}
```

> *Note : le Sample I/O est coupé au bord droit dans la photo source ; les valeurs de cash et pnl manquent.*

**Notes**

- The buckets must reconcile exactly: cash + mark-to-market == pnl.
