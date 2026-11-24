> **Synthetic data** — fictional zones; weather normals simulated from the same synthetic climate. Not observations.

### The desk asks

> “North-zone load was up more than 5 % this January compared with last year. Is that demand growth I should trade on, or was it just colder? And are the other zones telling the same story?”

### What you have

- `data/p1_zone_daily_synthetic.csv` — the output of 1.3 (zone, local_date, `temp_mean_c`, `hdd`, `cdd`, `load_avg_mw`, …).
- `data/p1_weather_normals_synthetic.csv` — the desk's **30-year normals**: for each zone and calendar month, `normal_temp_c`, `normal_hdd` and `normal_cdd` (mean daily degree days of that month in a normal year).

### What to find out

How many MW each zone's load moves per degree day of heating and of cooling — and, with that, what January–February load *would have been* in each year under normal weather.

### Minimum theory

- Per zone: `load_avg_mw = a + b_hdd · HDD + b_cdd · CDD + c · weekend + error`, estimated by OLS. `b_hdd` is in **MW per °C·day below the heating base**; `b_cdd` in MW per °C·day above the cooling base. Read the 95 % confidence interval (`conf_int()`), not just the point.
- That interval assumes independent errors. **Durbin-Watson** (`sm.stats.durbin_watson(resid)`, rows in time order) ≈ 2 means no day-to-day autocorrelation; well below 2, errors persist and the OLS interval is too narrow.
- A coefficient is only **identified** if the data vary in that direction: a zone with almost no hot days cannot tell you its cooling sensitivity.
- **Weather-adjusted load** (weather-normalised):
  `effect = b_hdd · (HDD − normal_HDD) + b_cdd · (CDD − normal_CDD)` and `adjusted = actual − effect`.
  It answers: “what would load have been with the same day, the same economy, but normal weather?” The reference weather must be stated; here it is the zone's 30-year normal for that calendar month.

### Assumptions

Days with a missing load or degree day are dropped from the estimation. Weekend = Saturday or Sunday (`dayofweek >= 5`). One regression per zone over 2023–2024.

### Your task

Implement `weather_adjusted_load(daily, normals)`:

1. Parse `local_date`; add `month` and `is_weekend` (0.0 / 1.0); merge the normals on (`zone`, `month`).
2. For each zone (sorted): drop rows with a missing `load_avg_mw`, `hdd` or `cdd`; sort by `local_date`; fit OLS of `load_avg_mw` on a constant, `hdd`, `cdd`, `is_weekend`. Record `zone`, `b_hdd`, `b_hdd_low`, `b_hdd_high`, `b_cdd`, `b_cdd_low`, `b_cdd_high`, `b_weekend`, `r2`, `n_days`, `durbin_watson` of the residuals, `cdd_days` (days with CDD > 0).
3. For the same rows: `weather_effect_mw` and `load_adjusted_mw` as above; keep `zone`, `local_date`, `hdd`, `normal_hdd`, `cdd`, `normal_cdd`, `load_avg_mw` plus the two new columns.
4. `winter_comparison`: rows of January and February, grouped by zone and year, mean of `hdd`, `load_avg_mw`, `load_adjusted_mw`.

Return `{"coefficients": ..., "daily": ..., "winter_comparison": ...}` (frames; `daily` with a fresh index). Then the **Explain** tab.
