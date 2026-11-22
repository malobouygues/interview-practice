# Datasets — Quantitative Methods track

**Every file here is SYNTHETIC.** The values are simulated with fixed random seeds by
`generate_data.py`. Dates, units, calendars and orders of magnitude are realistic so that the
economic reading makes sense, and a few well-known kinds of episode are *imitated* (a negative WTI
expiry print, a Gulf Coast refinery outage, the end of the US crude export ban). No value is a
market observation and nothing is downloaded. The seeds were chosen so that each phenomenon taught
by the exercises is visible.

Several files are **deliberately imperfect**: the imperfections are the subject of the exercises.

| File | Project | Structure | What is built in |
|---|---|---|---|
| `p1_crude_prices_vendor_synthetic.csv` | 1 | raw vendor export, daily 2019–2021, wide: `Date` (dd/mm/yyyy), Brent / WTI / Dubai (USD/bbl), `loaded_at` | text codes `HOL` (holiday) and `-` (not delivered), UK / US holiday calendars, 5 rows loaded twice, 2 dates re-sent with corrections, a late batch appended out of order, a ×10 fat-finger Brent print, a genuine negative WTI expiry print |
| `p1_crude_prices_clean_synthetic.csv` | 1 | clean layer: `date`, `brent`, `wti`, `dubai` | the raw file after the rules of exercises 1.2–1.3 (reproduced and checked by `tools/check_all.py`) |
| `p2_products_daily_synthetic.csv` | 2 | daily 2017–2019, wide: Brent (USD/bbl), ULSD and RBOB (USD/gal), ICE Gasoil and NWE jet (USD/t) | seasonal cracks (diesel winter peak, gasoline driving season), a refinery-outage shock, US / UK holidays, jet starting in 2018 and missing on the last 3 days, a gasoil feed frozen for 6 days, a ×10 RBOB print, 2 dates delivered twice, gasoil settling before Brent / NYMEX |
| `p2_products_treated_synthetic.csv` | 2 | the products after the gap treatment of exercise 2.2 | one row per date, stale run removed, ≤ 2-day forward fill (the RBOB error is still in it: exercise 2.5) |
| `p2_diesel_imports_monthly_synthetic.csv` | 2 | monthly 2017–2019, **long**: `month`, `importer`, `origin`, `volume_kbd` | genuine zeros, two non-reported months written as zeros, a country not yet reported for the last month |
| `p3_us_crude_stocks_weekly_synthetic.csv` | 3 | weekly 2016–2019: `week_ending`, `release_date`, `release_time_et`, `crude_stocks_mbbl`, `ingested_at` | Wednesday 10:30 releases (Thursday after a Monday holiday), history backfilled on 2019-01-07 |
| `p3_wti_daily_synthetic.csv` | 3 | daily 2016–2019: `date`, `wti_usd_bbl` | a price reaction to stock surprises on release days |
| `p3_us_oil_demand_vintages_synthetic.csv` | 3 | monthly 2015–2019, **vintage table**: `obs_month`, `vintage_date`, `demand_kbd` | first estimate at month end + 2, second estimate a month later, annual revision each August; first prints biased low |
| `p3_diesel_crack_monthly_synthetic.csv` | 3 | monthly 2015–2019: `month`, `diesel_crack_usd_bbl` | responds to true (not yet published) demand growth |
| `p4_crude_research_daily_synthetic.csv` | 4 | daily 2012–2019: `brent`, `wti`, `dubai` (USD/bbl), `coffee` (US¢/lb) | Brent random walk; WTI error-corrects towards a discount that changes on 2016-01-01 (16 % → 6 %, pass-through 0.60 → 0.90, adjustment 5 % → 10 % a day); Dubai ≈ Brent; coffee independent |
| `p4_diesel_demand_monthly_synthetic.csv` | 4 | monthly 2010–2019: `month`, `demand_kbd` | linear trend + fixed winter seasonal profile + short-memory noise (trend-stationary) |

The exercises read these files with relative paths such as
`pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")` —
the judge copies the files a problem needs into `data/` of its working directory.
