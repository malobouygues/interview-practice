The desk runs `clean_tape` over the raw market-data tape before any strategy reads it. It has been in production for months. Recently the traders have started reporting **occasional bad prints slipping through**: stale fills appearing at the wrong time, the odd zero or negative price reaching the book, and a few rows that simply look wrong. Most of the time the output looks fine, which is why nobody caught it sooner. Your job is to find out what the cleaner is getting wrong and fix it.

**The Job**

`clean_tape(prices)` already ships (it is in the editor). It is **supposed** to satisfy the spec below exactly. It does not. Diagnose where it diverges and repair it so that it meets the contract for every input, not just the easy ones.

**The Contract**

Given a raw price tape, `clean_tape` must return a cleaned table that obeys **all** of these rules, in this order:

1. **Sort** the rows ascending by `timestamp`.
2. **Drop duplicate timestamps**, keeping the **first** occurrence *after sorting*.
3. Treat any price that is **zero or negative** as **missing**.
4. **Forward-fill** each asset column from its last valid (post-sort) price.
5. A **leading** missing value with no prior valid price stays **null** (it cannot be filled).

Forward-fill means: if a price is missing, carry forward the most recent valid price for that asset. Each asset column is filled independently.

**Input Format**

`prices` is a `pd.DataFrame` with these columns:

| Column | Type | Description |
|---|---|---|
| `timestamp` | int | Milliseconds since session open |
| `Asset_1` | float | Mid price for asset 1 (may be missing / 0 / negative on bad prints) |
| `Asset_2` | float | Mid price for asset 2 |
| `Asset_3` | float | Mid price for asset 3 |

Rows may arrive **out of time order** and the same timestamp may appear **more than once**.

**Output Format**

Return a `pd.DataFrame` with the same columns (`timestamp`, `Asset_1`, `Asset_2`, `Asset_3`):

- One row per unique timestamp, sorted ascending by `timestamp`
- Zero / negative / missing prints repaired by forward-fill per the contract
- Index reset to 0, 1, 2, ...

Do **not** mutate the input DataFrame in place.
