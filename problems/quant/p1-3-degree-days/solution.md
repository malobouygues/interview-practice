### A. Reasoning — build the comparison table before comparing anything

The trader's question (“colder, or more demand?”) is a comparison across days with different weather. It needs, for each zone and market day, one number for the weather and one for demand, both defined consistently. Getting there means three alignments: irregular readings → hours, UTC → market day, hours → day (23, 24 or 25 of them).

### B. Theory

- **Frequency first** (A01-C, A04-C): aggregate to a common, regular frequency before combining. Readings at :50 plus occasional :20 are not hourly data; their plain mean over-weights the hours with two readings.
- **Market day** (A04-A): the day is a label of the *market's* clock. Floor in UTC (no ambiguity), convert, then label.
- **Degree days** (A07, physical demand): load responds to the *distance* below a heating threshold and above a cooling threshold. HDD and CDD turn a V-shaped relation into two straight lines. The base is a property of the zone (insulation, heating technology, air conditioning), so it is documented per zone.
- **Units**: average MW is a power level, MWh an energy quantity; MWh = MW × hours.

### C. Implementation

`dt.floor("h")` → `groupby(["zone", "hour_utc"]).mean()` → `tz_convert` → `groupby(["zone", "local_date"]).agg(mean, count)`. Degree days with `.clip(lower=0)` (which keeps `NaN` as `NaN`). Hours in a day: `(next local midnight − local midnight) / 1 h` after `tz_localize("Europe/Paris")` — midnights are never ambiguous.

### D. Interpretation (this dataset)

- Correlation of daily load with raw temperature: NORTH **−0.95**, CENTRAL **−0.77**, SOUTH **−0.04**. In SOUTH, heating (HDD, corr 0.26) and cooling (CDD, corr 0.53) cancel in a straight-line fit: raw temperature “explains nothing” while degree days explain a lot.
- NORTH has only **4** cooling days in two years (max CDD 1.25): its cooling sensitivity will be hard to estimate (1.4).
- 29 Oct 2023, CENTRAL: **12,993 MW** average over **25 h = 324,813 MWh**; 26 Mar 2023: 13,830 MW over 23 h = 318,080 MWh. The MWh difference is partly the clock.
- Blank by rule: NORTH 14 and 15 Feb 2023 (station outage: 1 and 10 hourly values), SOUTH 5 Mar 2024 (16 of 24 load hours); NORTH 19 Jul 2023 keeps its average from 23 of 24 hours, and its MWh scales it to 24 hours. One **99.9 °C** reading (SOUTH, 4 Jul 2023) is a sensor code.

### E. Decision

Use `load_avg_mw` (comparable across days) as the demand variable for the weather regression; quote MWh only for energy totals. Feed HDD and CDD, not temperature, to the model. Keep the three blank zone-days out of the estimation rather than repairing them.

### F. Pitfalls and limits

- Grouping temperatures by `observed_at.dt.date` uses UTC days: one or two hours of every market day land on the wrong day.
- A daily temperature from 10 readings that all fall in the afternoon is biased warm — hence the coverage rule.
- One station per zone is a strong simplification: real desks weight several stations by population or load.
- The base temperatures are part of the model: a wrong base shifts HDD and biases the sensitivity estimated in 1.4.

### G. Interview defence

*“Why degree days rather than temperature and temperature squared?”* — A quadratic forces a symmetric U around one minimum; demand has a flat zone between the heating and cooling thresholds and two different slopes. Degree days encode exactly that with two interpretable coefficients — MW per °C below the heating base, MW per °C above the cooling base — which is what the desk wants to talk about.
