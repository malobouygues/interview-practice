A market-making desk values its book off an **as-of price lookup**: given a timestamp, what was the fair value of an asset at that moment? The desk's `fair_value_at` helper is mispricing positions under some market conditions, and risk is flagging the discrepancies. The previous author has moved on. Your job: diagnose why it misprices and fix it so every condition is handled correctly.

**The Contract**

Implement `fair_value_at(ts, asset, prices, max_staleness_minutes)` so it returns the asset's fair value **as of** a query time, following the rules below exactly.

The code you start with already runs and returns plausible numbers, but it is **subtly wrong**. Read the spec, work out which conditions it mishandles, and correct it.

**What "fair value as of `ts`" means**

1. **As-of (backward) lookup**: return the price from the **most recent bar at or before `ts`**. You never look into the future.
2. **Skip nulls**: a bar can have a missing (null/NaN) price. When finding the most recent valid price, skip null bars and keep walking back to the last bar that actually has a price.
3. **Staleness clamp**: if the most recent valid bar is **older than** `max_staleness_minutes` before `ts`, the quote is stale: return null. (Exactly `max_staleness_minutes` old is still acceptable.)
4. **Before the first print**: if `ts` is earlier than every bar in the series, there is nothing to look back to: return null.
5. **Exact match**: if a bar's timestamp equals `ts` exactly, that bar is used (when its price is valid).

The input series is **not guaranteed to arrive in time order**.

**Input Format**

| Argument | Type |
|---|---|
| `ts` | str |
| `asset` | str |
| `prices` | pd.DataFrame |
| `max_staleness_minutes` | int |

**Output Format**

Return a dict:

```python
{"price": <float>}   # the fair value as of ts
{"price": None}      # if no usable price
```

**Hints**

- `pd.to_datetime(...)` parses both the column and the query time so you can compare them.
- A duration in minutes: `(a - b).total_seconds() / 60.0`
- Test your fix against unsorted input, missing prices, and a query that lands exactly on a bar.
