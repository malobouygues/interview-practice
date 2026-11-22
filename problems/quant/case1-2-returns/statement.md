> **Synthetic data** — simulated with a fixed seed so that the concepts are visible. Not market observations.

### Context

Step 1 showed that statistics on the TTF *level* describe a wandering path, while statistics on *returns* describe something comparable over time. Before testing anything, you need the right transformation — and there are three candidates, each with its own meaning.

### Objective

Build the three standard transformations of a price series in one table, and know which one to use for what.

### Minimum theory

| Transformation | pandas | Unit | Use it for | Never for |
|---|---|---|---|---|
| first difference | `p.diff()` | €/MWh | spreads, rates, anything that can be ≤ 0 | comparing periods where the price level changed a lot |
| % change | `p.pct_change()` | fraction | readable growth figures | adding up over time; bases close to 0 or negative |
| log return | `np.log(p).diff()` | log points | statistics on prices, aggregation over time | any series with values ≤ 0 |

Key identity: `log(P_T) - log(P_0)` is the **sum** of the daily log returns. Simple returns compound: `(1 + r_1)(1 + r_2)… - 1`.

### Assumptions

A log return requires **strictly positive** prices. An outright TTF price satisfies it; a spread (TTF − NBP, a calendar spread, a crack) does not have to, and real power or crude prices have been negative.

### Your task

Implement `make_returns(prices)`:

- `prices` — a `pd.Series` of prices (index = dates).
- Return a `pd.DataFrame` with the **same index** and exactly these columns, in this order: `price`, `diff`, `pct_change`, `log_return`. The first row of the three transformations is `NaN` (no previous price) — keep it.
- If any non-missing value of `prices` is **≤ 0**, raise a `ValueError` (a log return is undefined; the message should say to use `diff()` instead).
- Do not modify the input.

Then answer the question in the **Explain** tab.
