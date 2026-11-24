> **Synthetic data** — simulated with fixed seeds; settlement-time effects are imitated, values are invented.

### Context

A colleague notices that when NYMEX ULSD moves, ICE Gasoil seems to follow **the next day**, and suggests trading European diesel on yesterday's US move. Before anyone trades it, you check the claim — and its mechanics. Settlement times: ICE Gasoil **17:30 London**; NYMEX ULSD **14:30 New York** (19:30 London); ICE Brent **19:30 London**.

### Objective

Compute a cross-correlation table at several lags, read the sign convention correctly, and decide whether the lead is real.

### Minimum theory

- `x.shift(k)` on row t holds `x_{t−k}`. So `corr(x.shift(k), y)` measures whether **x moved k days before y** (k > 0: x leads; k < 0: y leads).
- A lead between **settlement prices** can come from **settlement times**: news arriving after one market's close appears in the other's price the same day and in the first market's price the next day.
- Lead-lag is measured on **changes**: trending levels correlate at every lag.

### Assumptions

Daily log returns on the treated prices (`data/p2_products_treated_synthetic.csv`), on dates where both series are observed.

### Your task

Implement `lead_lag_table(x, y, max_lag)` for two `pd.Series` with the same index. For each `k` from `−max_lag` to `max_lag`, compute `x.shift(k).corr(y)`. Return a `pd.Series` named `"corr"`, indexed by `k` (index name `"lag"`), in increasing order of `k`.

Answer in the **Explain** tab.
