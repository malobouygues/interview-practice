> **Synthetic data** — a fictional power market, simulated with fixed seeds. Not market observations.

### The desk asks

> “We had several very high day-ahead prices during cold, low-wind periods. Can you investigate whether weather and renewable generation explain these price spikes, or whether something else is happening?”

This is the question from the start of the project. You now have trusted hourly data (1.1–1.2), zone weather (1.3–1.4) and a picture of normal behaviour (1.5).

### What you have

- `data/p1_power_hourly_treated_synthetic.csv` — hourly prices, load, wind, solar, available capacity (carried ≤ 48 h), gas.
- `data/p1_zone_daily_synthetic.csv` — daily HDD by zone (1.3).

### What to find out

Which days had spikes, what the market looked like on those days — weather, wind, spare capacity — and whether one explanation covers them all.

### Minimum theory

- **Residual load** = load − wind − solar: what dispatchable plants (gas, coal, nuclear, hydro) must cover.
- **Margin** = available dispatchable capacity − residual load. The **merit order** is steep near the end: as the margin goes to zero, the marginal plant is the most expensive one, then scarcity pricing.
- Weather enters *through* the margin: cold raises load, still air removes wind; an outage removes capacity in any weather.
- With fat tails, use **rank correlations** (`corr(method="spearman")`).
- An **attribution rule** must be written down before looking at the result, and be simple enough to check by hand.

### Assumptions

- Spike day: daily maximum price ≥ **300 €/MWh**.
- National HDD: simple average of the three zones' HDD.
- Normal capacity: median daily capacity of the same calendar month (both years).
- Rules: “cold and still” if HDD ≥ 12 and the day's average wind < 4,000 MW; else “low available capacity” if capacity < 90 % of normal; else “unexplained”.

### Your task

Implement `explain_spikes(hours, daily)`:

1. Hourly: `residual_load_mw`, `margin_mw`.
2. Daily (group by `local_date`): `max_price`, `mean_price`, `min_margin_mw`, `wind_mean_mw`, `capacity_mw` (mean), `gas_eur_mwh` (mean); add `hdd` (zone average) and `capacity_ratio` (capacity / median of its calendar month).
3. `rank_correlations`: Spearman correlation of `max_price` with `hdd`, `wind_mean_mw`, `min_margin_mw`, `capacity_ratio` (a Series indexed by those names).
4. `spike_days`: the days with `max_price >= 300`, with a `driver` column from the rules above.

Return `{"spike_days": ..., "rank_correlations": ...}`. Then give the trader your answer in the **Explain** tab — it is the conclusion of the project.
