> **Synthetic data** — invented volumes, outages and stocks with realistic orders of magnitude; the embargo and strikes imitate known episodes.

### The desk asks

> “If the crack widening is physical, it should show up somewhere: fewer imports, refineries offline, low stocks. Put the physical side next to the crack, month by month. And be careful — the import statistics are full of zeros.”

### What you have

- `data/p2_diesel_imports_monthly_synthetic.csv` — **long**: `month`, `importer` (UK, France, Germany, Netherlands), `origin` (USA, Russia, Saudi Arabia, India), `volume_kbd`. When a country does not report, the aggregator writes **0 for every origin**.
- `data/p2_refinery_outages_synthetic.csv` — one row per outage: `refinery`, `region`, `start`, `end`, `offline_kbd`, `cause`. The list is complete.
- `data/p2_distillate_fundamentals_monthly_synthetic.csv` — **wide**: `month`, `refinery_utilisation_pct`, `distillate_stocks_mb`, `stocks_5y_avg_mb`.
- `data/p2_products_repaired_synthetic.csv` — the daily table after 2.2 (index `date`, prices and cracks in USD/bbl).

### What to find out

One row per month with European imports (and how much came from Russia), refinery capacity offline, stocks against their 5-year average, and the average gasoil crack — with real zeros kept and fake ones removed.

### Minimum theory (PDF A03-A, A01-B, A04-C)

- **Zero vs missing vs non-reporting**: a zero is an observation (“no cargo”); a blank is the absence of one. A whole country at zero in one month is a *reporting* event, not a market one. An absent row at the end of the sample is the **ragged edge** (not yet published).
- `groupby(...).agg(...)` then `pivot` to move from long to wide; `sum(axis=1, min_count=4)` returns `NaN` unless 4 values are present.
- **Events → months**: expand each outage to its days (`pd.date_range(start, end)`), then average by month: kb/d offline on average over the month (sum of daily kb/d ÷ days in month).
- **Monthly alignment**: `to_period("M")` gives one key for daily and monthly data.

### Assumptions

- An importer-month where no origin is positive did not report. Total imports require all four importers.
- Russian imports are summed over reporting importers only, and blanked when the total is blank.
- `stocks_vs_5y_pct = 100 × (stocks / 5-year average − 1)`.

### Your task

Implement `monthly_table(imports, outages, fundamentals, daily)` returning a frame indexed by `month` (monthly Period) with the columns, in order: `importers_reporting`, `imports_kbd`, `imports_from_russia_kbd`, `outages_kbd`, `refinery_utilisation_pct`, `stocks_vs_5y_pct`, `gasoil_crack` (monthly mean), `crack_days` (count of priced days). Months: those of the imports file. Then the **Explain** tab.
