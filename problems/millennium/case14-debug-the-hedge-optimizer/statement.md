You sit on the risk desk. The systematic book is carrying a position in **Asset_3**, and the standard play is to hedge it with two correlated instruments, **Asset_1** and **Asset_2**, sizing the hedge so the combined position's return wobbles as little as possible. A junior built the `hedge_optimizer` helper, but the desk has stopped trusting it: the hedge ratios it produces look **unstable and far too large**, and the "leftover risk" number it reports never looks right. Find out why and fix it.

You are given a working (but broken) implementation. **Diagnose the defects and repair the function so it matches the specification below exactly.** Do not change the function name or signature.

**What the function must compute**

You hold an inventory in Asset_3 and want to hedge it using Asset_1 and Asset_2. The minimum-variance hedge is found by regressing the **returns** of the target asset on the **returns** of the two hedging instruments.

Follow this specification precisely; it is the single correct definition:

1. **Returns, not prices.** Convert each price column to **simple percentage returns**, `r_t = P_t / P_{t-1} - 1`, then drop the first row (which is undefined). Work entirely in return space; never regress on raw price levels.
2. **De-mean.** Centre the target returns and each instrument's returns by subtracting their means.
3. **Solve the least-squares hedge.** Find the coefficients `(b1, b2)` that minimise the variance of the hedged return, i.e. the ordinary least-squares fit of the de-meaned Asset_3 returns onto the de-meaned [Asset_1, Asset_2] returns. Use `numpy.linalg.lstsq` on the de-meaned data (no separate intercept term is needed once everything is de-meaned).
4. **Scale by inventory.** The hedge quantity for each instrument is `-b_i * inventory["Asset_3"]` (you trade against your exposure).
5. **Residual variance.** Form the hedged return series `hedged = (target returns, de-meaned) - (instrument returns, de-meaned) @ (b1, b2)` and report its **population variance**: the mean of the **squared, de-meaned** hedged returns. (Remember a variance is measured about the mean.)
6. **Rounding.** Round every hedge quantity and the residual variance to **4 decimal places**.
7. **Empty position.** If `inventory["Asset_3"] == 0` there is nothing to hedge: return a hedge of 0.0 for each instrument and `residual_variance` of 0.0.

**Input**

| Argument | Type | Description |
|---|---|---|
| `prices` | dict | Serialised price table. `prices["columns"]` is `["timestamp", "Asset_1", "Asset_2", "Asset_3"]` ; `prices["data"]` is a list of rows `[timestamp, p1, p2, p3]` in time order. |
| `inventory` | dict | `{"Asset_1": q1, "Asset_2": q2, "Asset_3": q3}`, current holdings. Only the Asset_3 quantity drives the hedge sizing here; Asset_1 / Asset_2 are the instruments. |

The `prices` dict is decoded into a `pandas.DataFrame` for you inside the function.

**Output**

Return a dict of exactly this shape (all numbers rounded to 4 dp):

```python
{
    "hedge": {"Asset_1": <float>, "Asset_2": <float>},
    "residual_variance": <float>
}
```

**Notes**

- The visible sample is a sanity check; the hidden cases exercise real books (long, short, mixed) over different price histories.
- Two things to scrutinise: **what** is being regressed and **on what scale**, and whether the leftover-risk number is really a variance.
