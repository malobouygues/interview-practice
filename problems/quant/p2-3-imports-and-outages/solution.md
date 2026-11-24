### A. Reasoning — a zero is a statement about the market

The trader's hypothesis is physical: less supply should leave traces in imports, refinery availability and stocks. Those series come in different shapes (long, event list, wide) and they encode absence differently. The work is to put them on one monthly key while keeping the difference between “nothing happened” (a real zero) and “nobody told us” (missing).

### B. Theory (PDF A03-A missing values, A01-B structure, A04-C frequency alignment)

- **Missingness mechanisms**: a non-reporting country is *missing*, and not at random (it can coincide with disruptions); a genuine zero is data. Treating missing as zero biases sums down; treating genuine zeros as missing biases averages up.
- **Ragged edge**: the latest period is incomplete because publication is late — expected, and different from an error.
- **Events to a regular frequency**: an outage list is a set of intervals; its monthly measure is the average capacity offline over the days of the month.
- **Normalisation**: stocks against their own seasonal 5-year average remove the seasonal pattern and the level.

### C. Implementation

`groupby(["month", "importer"]).agg(volume=sum, positive_origins=sum of a boolean)` then a mask; `pivot` to one column per importer; `sum(axis=1, min_count=4)`. Outages: a loop builds one row per day, `dt.to_period("M")`, `sum / days_in_month`, `reindex(...).fillna(0)` — legitimate *because* the list is complete. The daily crack: `index.to_period("M")` then `agg(["mean", "count"])`.

### D. Interpretation (this dataset)

- 42 zero rows: **12** from non-reporting (France 2018-08, Netherlands 2019-04, UK 2022-08, 4 origins each), **11** genuine (Germany–India, UK–Saudi), **19** Russian origins after the February 2023 embargo — genuine.
- Literal sums would show European imports at **830.5 kb/d** in August 2018 (July 1,124, September 1,292), **895** in April 2019, **917** in August 2022 — three fake collapses. The table leaves them blank; June 2023 is blank too (Germany not yet reported).
- Outages: **1,467 kb/d** offline on average in September 2017 (hurricane), 900 in February 2021 (winter storm), **650** in October 2022 (French strikes).
- Imports Feb–May 2023 averaged **1,263 kb/d** vs **1,345** in 2022 while Russia's share went from 52 % to 0: the embargo changed the origin more than the volume.
- Stocks: **−23.4 %** vs the 5-year average in September 2022 (+12.4 % in July 2020). The monthly crack peaked at **46.4 $/bbl** in August 2022 and touched −1.4 in July 2020. Correlation crack–stocks deviation: **−0.96**.

### E. Decision

The physical evidence points to stocks: the crack tracks the stock deficit closely, outages add spikes, and imports did not collapse. That is a correlation on 78 months — 2.4 tests how strong and how reliable the relationship is.

### F. Pitfalls and limits

- The “all origins at zero” rule would mis-classify a country that genuinely imported nothing — implausible here, possible for a small importer.
- Expanding outages assumes a constant `offline_kbd` over each outage; real restarts are gradual.
- `fillna(0)` on outage months is only valid because the list is complete; with an incomplete list it would invent quiet months.
- The monthly crack averages a different number of days per month (`crack_days`): months with many gaps are noisier.

### G. Interview defence

*“Imports fell 30 % in August 2018 — is that a supply shock?”* — No: France reported nothing that month and the aggregator wrote zeros for every origin. I check that a country reported at least one positive origin before I believe its zeros, and I only total Europe when all four countries are in. The real zeros — Russia after the embargo — I keep, because they are the information.
