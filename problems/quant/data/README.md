# Datasets — Quantitative Methods track

**All four files are SYNTHETIC.** They are simulated with fixed random seeds by
`generate_data.py`. Dates, units and orders of magnitude are realistic so that the
economic reading makes sense, but no value is a market observation. The seeds were
chosen so that each phenomenon taught by the exercises is visible in the sample.

| File | Rows | Columns | Used in | What is built in |
|---|---|---|---|---|
| `ttf_daily_synthetic.csv` | 782 business days, 2017–2019 | `date`, `ttf` (€/MWh) | Case 1 | log price = random walk with fat-tailed shocks (stochastic trend) |
| `diesel_demand_monthly_synthetic.csv` | 120 months, 2010–2019 | `month`, `demand_kbd` (kb/d) | Case 1, step 6 | linear trend + fixed seasonal profile + short-memory noise (trend-stationary) |
| `crude_daily_synthetic.csv` | 913 business days, Jul 2016 – Dec 2019 | `date`, `brent`, `wti` ($/bbl), `coffee` (US¢/lb) | Cases 2–3 | Brent random walk; WTI error-corrects towards a 6 % discount to Brent; coffee independent of both |
| `crude_history_synthetic.csv` | 2,087 business days, 2012–2019 | `date`, `brent`, `wti` ($/bbl) | Case 4 | same construction, with a regime change on 2016-01-01: 16 % → 6 % discount, short-run pass-through 0.60 → 0.90, adjustment speed 5 % → 10 % per day |

`crude_daily_synthetic.csv` is exactly the tail (from 2016-07-01) of
`crude_history_synthetic.csv`, plus the coffee column: Case 4 extends the sample you
studied in Cases 2 and 3. The regime change is *inspired by* the end of the US crude
export ban (December 2015) described in the source document; its size and dynamics are
invented.

The exercises read these files with relative paths such as
`pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")` —
the judge copies the files a problem needs into `data/` of its working directory.
