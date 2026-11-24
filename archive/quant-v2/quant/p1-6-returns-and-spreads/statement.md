> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

Statistics on crude prices are computed on **changes**, not levels (step 1.5). But "change" has three definitions, and two of them break on this dataset: WTI went negative, and the Brent–Dubai spread crosses zero. The right transformation depends on what the series is.

### Objective

Build the three standard transformations of a price series, know which one to use for what, and refuse the impossible cases loudly.

### Minimum theory

| transformation | pandas | unit | use it for | never for |
|---|---|---|---|---|
| first difference | `p.diff()` | USD/bbl | spreads, anything that can be ≤ 0 | comparing moves when the level changed a lot |
| % change | `p.pct_change()` | fraction | readable growth figures | adding up over time; bases ≤ 0 or near 0 |
| log return | `np.log(p).diff()` | log points | statistics on prices, aggregation over time | any series with values ≤ 0 |

`log(P_T) − log(P_0)` is the **sum** of the daily log returns; % changes compound: `(1 + r_1)(1 + r_2)… − 1`.

### Assumptions

Returns are measured between **consecutive observed prices**: a holiday is not a zero return, and the first price after a holiday carries a two-day move.

### Your task

Implement `make_returns(prices)` for a `pd.Series`:

1. Drop the missing values.
2. If any remaining price is **≤ 0**, raise a `ValueError` saying to use `diff()` instead.
3. Return a `DataFrame` indexed like the remaining prices, with columns `price`, `diff`, `pct_change`, `log_return` in this order (the first row of the three transformations is `NaN`).

Do not modify the input. (Use `table["pct_change"]`, not `table.pct_change`, to read a column whose name is also a method.) Then answer in the **Explain** tab.
