> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

Back to the research question: what moves the US diesel crack day to day? Before any model, you need candidate **explanatory variables** — and each must be computable **at the moment the decision is taken**, using only information available then. The desk's morning meeting is at 08:00 London: day t's settlement is not known yet.

### Objective

Build a small, economically motivated feature set for the daily change of the diesel crack, with an explicit information set, and screen which features deserve to be kept.

### Minimum theory

- **Forecast origin**: the morning of day t. **Information set**: settlements up to t−1. **Target**: `crack_change_t = crack_t − crack_{t−1}`.
- `shift(1)` moves a value to the next row: a feature on row t built from data up to t−1. Rule (PDF, A07-C): **shift before (or after) rolling, never a window that includes t**.
- `rolling(20).mean()`, `.std()`, `rolling(60).corr(other)`: local statistics over the last n rows.
- Calendar variables (month, season) are known in advance: no shift.
- **Screening**: keep a feature only if it has an economic reason *and* a stable relationship with the target across sub-periods.

### Assumptions

Prices come from the treated file of step 2.2 (gaps filled ≤ 2 days, so rolling windows are not broken by holidays). Cracks in USD/bbl: diesel = ULSD×42 − Brent, gasoil = gasoil/7.45 − Brent.

### Your task

Implement `build_features(cracks)` for a `DataFrame` indexed by date with columns `diesel_crack`, `gasoil_crack`. With `change = diesel_crack.diff()` and `gasoil_change = gasoil_crack.diff()`, return a `DataFrame` (same index) with columns, in order:

| column | definition |
|---|---|
| `crack_change` | `change` (the target, not a feature) |
| `change_lag1` | `change.shift(1)` |
| `mean_change_20` | `change.rolling(20).mean().shift(1)` |
| `vol_change_20` | `change.rolling(20).std().shift(1)` |
| `gap_to_mean_60` | `(diesel_crack − diesel_crack.rolling(60).mean()).shift(1)` |
| `corr_gasoil_60` | `change.rolling(60).corr(gasoil_change).shift(1)` |
| `month` | month of the index (int) |
| `heating_season` | 1 for November–March, else 0 (int) |

One of the tests rebuilds the features on data **truncated** at a past date and checks they are identical to the full-data features on those dates. Answer in the **Explain** tab.
