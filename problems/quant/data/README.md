# Quantitative Methods — datasets

**Every file here is SYNTHETIC.** Values are simulated with fixed seeds by `generate_data.py`; dates,
units, calendars and orders of magnitude are realistic so that the economic reading makes sense, and
some well-known episodes are *imitated* (a Gulf Coast hurricane, the 2020 price war and lockdowns, a
2022-style distillate squeeze, the end of the US crude export ban, a cold and windless winter week).
None of it is market data. The power market, its zones and weather stations are fictional. Nothing is
downloaded.

```bash
python3 problems/quant/data/generate_data.py      # rewrites every CSV below (about 2 seconds)
```

Two kinds of files:

- **raw files**, deliberately imperfect — each defect has an economic reason to exist and is the subject of an exercise;
- **derived layers** (`*_clean_*`, `*_treated_*`, `*_wide_*`, `*_repaired_*`, `*_daily_*`, `*_monthly_table_*`, `p3_release_events`, `p3_decision_table_daily`): what a correct answer to an earlier exercise returns, so that later exercises can start from it. P1 and P2 layers are produced by running the **reference solution** of the exercise that builds them; the two P3 tables are built by the desk's pipeline in `generate_data.py` with the rules of exercises 3.1–3.3. `tools/check_all.py` re-derives every layer and checks it matches.

numpy does not promise identical random streams across major versions; the committed CSVs are the reference.

---

## Project 1 — Gas & Power (fictional Central-European market, `Europe/Paris` clock, 2023–2024)

**How it is generated.** Daily temperatures per zone = climatology (annual sine) + a shared European anomaly (first-order autoregressive) + a zone anomaly, with planted episodes: a mild January 2023, a colder January–February 2024 with a **cold, still spell 8–19 Jan 2024**, a cold week in December 2023, two heat waves. Daily load per zone = base level (−2.5 % in 2024: weaker underlying demand) × weekday factor (−12 % at weekends) + β_HDD·HDD + β_CDD·CDD + noise, spread over the hours with a load profile. Wind follows a weather state that is low in cold anticyclonic spells; solar follows a daylight bell × season × clouds. Available dispatchable capacity is a daily state with summer maintenance and an **outage of 8 GW on 2–13 Oct 2023**. Price = merit order on utilisation (residual load / capacity) × gas price, with scarcity pricing above ~80 % utilisation and a few negative hours in sunny, windy, low-load hours.

| zone | HDD base | CDD base | true sensitivity (MW per °C·day) | meaning |
|---|---|---|---|---|
| NORTH | 15.5 °C | 20.0 °C | 260 heating / 40 cooling | electric heating, almost no cooling days |
| CENTRAL | 16.0 °C | 22.0 °C | 180 / 150 | largest zone, mixed |
| SOUTH | 17.0 °C | 21.0 °C | 60 / 320 | air conditioning |

Units: load in **MW** (average power over the hour or the day); energy in **MWh** = average MW × hours (23, 24 or 25 per local day). Daily temperature = mean of hourly means on the **local** market day (≥ 18 hours required). Degree days: `HDD = max(base − T, 0)`, `CDD = max(T − base, 0)`, per zone. **Reference weather** for weather adjustment = the 30-year normals file (mean daily HDD/CDD of that zone and calendar month, simulated from the same climate without special episodes).

| file | what it is | planted on purpose | what a correct analysis shows | mistake it exposes |
|---|---|---|---|---|
| `p1_power_hourly_vendor_synthetic.csv` | hourly market data, **local time + UTC offset**, 17,553 rows | 6 exact copies; 3 corrected records (a ×10 price 772.50 → 77.25, two digits swapped, a missing solar value), each re-loaded later (`loaded_at_utc`); two 25-hour and two 23-hour days; solar blank at night (vendor convention); wind feed failures (14 Nov 2023, 6 Feb 2024); 2 missing prices; capacity sent once a day, missed on 8 May 2023 and 2–6 Sep 2024 | 17,544 delivery hours; the 772 €/MWh “spike” is a vendor error | deduplicating on local time (deletes the second 02:00 hour); trusting the first version; forward-filling a price or a failed feed |
| `p1_power_hourly_clean_synthetic.csv` | output of 1.1 (UTC index) | — | — | — |
| `p1_power_hourly_treated_synthetic.csv` | output of 1.2 | — | 8,845 structural solar blanks = 0, 5 failures; capacity carried ≤ 48 h with its age | grouping daylight by *local* hour (13 hours flagged instead of 5); a 24-hour age limit for a stale capacity (146 hours instead of 144: wrong on the 25-hour days) |
| `p1_zone_load_hourly_synthetic.csv` | hourly load by zone, **UTC**, long | SOUTH missing 8 hours on 5 Mar 2024 (rows absent); NORTH one blank hour on 19 Jul 2023 | coverage rules blank the day instead of averaging what is there | grouping by UTC date; summing MW as if it were MWh on DST days |
| `p1_zone_temperature_obs_synthetic.csv` | weather observations, **UTC**, irregular (:50 and some :20 readings) | NORTH station outage 14–15 Feb 2023; one `99.9` sensor code | daily means from hourly means on the local day; SOUTH load vs temperature −0.04 but vs CDD +0.53 | averaging raw readings; regressing on raw temperature |
| `p1_zones_reference_synthetic.csv` | zone definitions and base temperatures | — | — | one universal base temperature |
| `p1_weather_normals_synthetic.csv` | 30-year normals by zone × month | — | weather-adjusted load: Jan–Feb 2024 actual +0.9 % to +5.4 %, adjusted −1.4 % to −3.7 % | normals computed from the two sample years |
| `p1_zone_daily_synthetic.csv` | output of 1.3 | — | NORTH has 4 cooling days: its CDD coefficient is not identified (CI −142 to +401) | — |

The spike investigation (1.6) finds 14 days ≥ 300 €/MWh: 10 cold and still, 4 during the October outage in mild weather (including the maximum, 2,026 €/MWh). The capacity margin ranks with spikes at −0.80, HDD at +0.39.

## Project 2 — Oil products (daily 2017-01 → 2023-06; monthly)

**How it is generated.** Monthly fundamentals first: distillate stocks against their 5-year average (a 2020 glut, a deep 2022 deficit), refinery utilisation, outages from an event list. The monthly gasoil crack = a convex function of the stock deficit + outages + a shock whose **variance grows when stocks are tight**. Daily cracks interpolate the monthly level and add fat-tailed (Student t) noise; Brent follows an anchored path with a price-war drop on 9 Mar 2020. Product prices = Brent + crack, then converted to each product's quoting unit.

| file | what it is | planted on purpose | what a correct analysis shows | mistake it exposes |
|---|---|---|---|---|
| `p2_products_daily_long_synthetic.csv` | **long**: date, product, unit, price | ULSD in **USc/gal until end-2020**, USD/gal after; gasoil and jet in **USD/t** (7.45 and 7.88 bbl/t); 3 duplicated rows; UK/US holiday gaps (absent rows); jet starts 2018-03; last 3 jet days unpublished; **frozen gasoil feed** 8–15 Oct 2018; **RBOB 14 May 2019 sent in cents** under a USD/gal label; **gasoil 0.00** on 25 Nov 2021; genuine shocks: hurricane (28 Aug 2017), price war (9 Mar 2020), jet collapse (2020), invasion (Feb–Mar 2022), New York Harbor squeeze (31 Oct 2022); one doubtful jet print (15 Jun 2021) | crack history in USD/bbl; one unit error moves the 2019 RBOB crack average from 10.1 to 45.0 | converting by product name; deleting or winsorising extremes; scoring before fixing gross errors (masking: hurricane z = 1.2 instead of 10.2) |
| `p2_market_events_synthetic.csv` | the desk's event log | — | 11 extremes kept as logged events | — |
| `p2_products_wide_synthetic.csv` | output of 2.1 | — | — | — |
| `p2_products_repaired_synthetic.csv` | output of 2.2 (unit error corrected, 0.00 blanked) + cracks | — | — | — |
| `p2_diesel_imports_monthly_synthetic.csv` | **long**: month, importer, origin, kb/d | genuine zeros (no cargo); **Russian origins at 0 from Feb 2023 (embargo, genuine)**; non-reported months written as 0 for every origin (France 2018-08, Netherlands 2019-04, UK 2022-08); Germany 2023-06 absent (ragged edge) | fake import “collapses” of 20–35 % disappear; volumes barely fall after the embargo, origins change | treating non-reporting as zero |
| `p2_refinery_outages_synthetic.csv` | one row per outage (complete list) | hurricane, fires, strikes, maintenance | months without an outage are a real 0 kb/d | — |
| `p2_distillate_fundamentals_monthly_synthetic.csv` | **wide**: utilisation, stocks, 5-year average | — | stocks −23 % vs 5-year average in Sep 2022 | — |
| `p2_monthly_table_synthetic.csv` | output of 2.3 | — | OLS: −1.09 $/bbl per point of deficit; White p = 0.002; HC3 SEs × 1.5; residuals curved | reading HC3 as a fix for a misspecified (convex) relationship |

## Project 3 — Crude: point-in-time (2019–2024)

**How it is generated.** Weekly stocks = previous level + consensus change + a surprise (σ = 3 mb). Releases on Wednesday 10:30 New York, Thursday after a Monday holiday or a holiday on the Wednesday, and once **12 days late** (week ending 17 Jun 2022, published 29 Jun 2022). The desk's database was created on 2 Mar 2020: earlier records are **backfilled**. WTI = anchored path + mean-reverting noise (volatility 5 % a day in spring 2020, 3 % in 2022) + a **permanent reaction of −0.4 % per mb of surprise between 10:30 and the settlement** + a **post-release drift that exists only from May 2020 to Dec 2021**. Monthly demand is published at the end of M+2, revised at M+3 and again each August; first estimates are biased low.

**Out-of-sample design.** Decision origin = each 14:30 New York settlement. Features = what was known at that moment: the surprise of the latest report already published (backward as-of join on availability, tolerance 10 days) and demand growth **as known** (latest vintage before the day). Target = log WTI return to the settlement 10 trading days later (`target_end_date`). Estimation: rows whose target ended by 31 Dec 2022 (labels purged at the split); test: 2023–2024, used once. Walk-forward: expanding window re-estimated at each quarter start, on rows whose target ended before the origin.

| file | what it is | what a correct analysis shows | mistake it exposes |
|---|---|---|---|
| `p3_us_crude_stocks_weekly_synthetic.csv` | weekly reports: week, release date/time (New York), level, consensus, ingestion time (UTC) | lags of 5 (278), 6 (35) and 12 days (1); 61 backfilled records; 10:30 New York = 14:30 or 15:30 UTC | using `week_ending` (too early) or `ingested_at` (too late) as availability |
| `p3_wti_daily_synthetic.csv` | daily settlements | — | — |
| `p3_wti_release_snapshots_synthetic.csv` | WTI at 10:29 New York on release days | reaction −0.30 % per mb (t −6.7) | measuring the reaction from yesterday's settlement |
| `p3_us_oil_demand_vintages_synthetic.csv` | month × vintage | a March decision knows December; revisions +127 kb/d on average | using today's (revised) values for past decisions |
| `p3_release_events_synthetic.csv` | one row per release (pipeline) | — | — |
| `p3_decision_table_daily_synthetic.csv` | one row per trading day (pipeline) | drift t −4.8 (OLS) → −2.9 (HAC); out of sample the model is worse than predicting zero (MAE 6.21 % vs 5.98 %) | random splits; unpurged labels; quoting overlapping-window t-stats |

The `week_ending` join attaches a not-yet-published report on 929 of 1,510 days and “predicts” the release-day move (t −4.4).

## Project 4 — Crude research panel (daily 2012–2019) and diesel demand (monthly 2010–2019)

**How it is generated.** Brent = log random walk with **volatility regimes** (1.2 % a day to mid-2014, 2.6 % to early 2016, 1.6 %, 2.5 % in late 2018, 1.7 %) and a slump drift mid-2014 → Jan 2016. WTI = error correction around log WTI = a + log Brent with a **regime change on 1 Jan 2016** (end of the export ban): discount 16 % → 6 %, short-run pass-through 0.60 → 0.90, adjustment 5 % → 10 % of the gap per day; a one-day WTI-specific drop on 28 Aug 2017 (hurricane). Dubai = Brent + a small stationary differential. Coffee = an independent random walk (seed chosen so that its path happens to trend like WTI). Diesel demand = linear trend + fixed seasonal profile + short-memory noise (each month keeps 20 % of the previous deviation).

| file | what a correct analysis shows | mistake it exposes |
|---|---|---|
| `p4_crude_research_daily_synthetic.csv` | level correlation Brent–WTI 0.996 but WTI–coffee 0.82 too; in returns 0.82 vs 0.006; coffee regression t = 69, DW 0.016, nothing in changes, Engle-Granger p 0.17 (naive residual ADF p 0.059); Brent–WTI cointegrated in each regime, discount 15.9 → 2.9 $/bbl, Chow F 114 | correlating levels; testing residuals with ADF critical values; one full-sample equilibrium |
| `p4_diesel_demand_monthly_synthetic.csv` | ADF with `c` p 0.98, with `ct` p < 0.001: trend-stationary; seasonal differencing gives ACF −0.49 at lag 12 | differencing after one ADF run with the wrong deterministic terms |
