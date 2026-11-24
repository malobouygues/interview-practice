### A. Reasoning — compare demand at equal weather

Two winters with different temperatures cannot be compared on raw load: the colder one will show “growth” even if every household and factory used less power at a given temperature. The fix is to estimate how load responds to weather, then remove from each day the part due to *abnormal* weather. What remains can be compared across periods.

### B. Theory (A05 relationships, A08 simple models, A11 interpretation)

- **The model.** `load = a + b_hdd·HDD + b_cdd·CDD + c·weekend + e`. Signs expected: b_hdd > 0, b_cdd > 0, c < 0. Units: MW of daily average load per °C·day.
- **Inference.** The 95 % interval `[b − 1.96·SE, b + 1.96·SE]` says which values are compatible with the data. A wide interval crossing zero = the data do not measure the effect. This formula assumes independent errors: check Durbin-Watson before trusting a *narrow* interval.
- **Identification.** A coefficient is estimated from the variation of its regressor. Four days with CDD > 0 are four data points.
- **Weather normalisation.** Choose a reference weather (here the 30-year normal of the zone and month), compute the weather effect *relative to it*, subtract. The result is a counterfactual — model-dependent, never observed.

### C. Implementation

`merge` the normals on (zone, month); one `sm.OLS(...).fit()` per zone in a plain `for` loop; `conf_int()` gives the bounds; `sm.stats.durbin_watson(model.resid)` on rows sorted by date; the adjustment uses the zone's own coefficients; `groupby(["zone", "year"]).mean()` for the comparison.

### D. Interpretation (this dataset)

| zone | b_hdd (MW / HDD) | b_cdd (MW / CDD) | weekend | R² | DW |
|---|---|---|---|---|---|
| NORTH | 261.0 [258.7, 263.2] | 129.6 [−141.6, 400.9] — 4 CDD days | −1,067 | 0.99 | 0.72 |
| CENTRAL | 174.1 [170.4, 177.8] | 112.2 [54.2, 170.1] — 22 days | −1,665 | 0.95 | 0.61 |
| SOUTH | 60.2 [57.8, 62.6] | 321.0 [311.7, 330.4] — 147 days | −822 | 0.93 | 0.78 |

Durbin-Watson of **0.61–0.78**: the errors persist from one day to the next, so the intervals above are **too narrow** — autocorrelation-robust errors make the heating intervals about 2 to 3 times wider, depending on the number of lags kept. The point estimates, the adjusted load and the conclusions do not move. About half of the persistence is the lower 2024 level, which the regression leaves in the residuals (with a 2024 dummy, DW rises to 0.9–1.15).

January–February, average MW (actual → weather-adjusted):

| zone | 2023 | 2024 | actual change | adjusted change |
|---|---|---|---|---|
| NORTH | 12,689 → 12,879 | 13,379 → 12,697 | +5.4 % | −1.4 % |
| CENTRAL | 15,953 → 16,248 | 16,095 → 15,653 | +0.9 % | −3.7 % |
| SOUTH | 7,328 → 7,413 | 7,406 → 7,204 | +1.1 % | −2.8 % |

2024 was colder (NORTH HDD 18.8 vs 15.5 per day; CENTRAL 16.8 vs 12.6; SOUTH 13.6 vs 8.9). The whole rise in actual load is weather; at normal weather, demand fell in every zone. (Synthetic check: the generator used 261/40, 180/150 and 60/320 MW per degree day and a 2.5 % lower 2024 level — the heating slopes are recovered; NORTH's cooling slope cannot be.)

### E. Decision

Tell the trader: “No demand growth — the January increase is the cold. Weather-adjusted, demand is 1–4 % lower than a year ago in all three zones.” Do not use NORTH's cooling coefficient for anything; for a northern heat wave, borrow information (CENTRAL's slope, or a longer history) and say so.

### F. Pitfalls and limits

- Normals computed from the same two years would put the cold 2024 winter into the “normal” — use an external, longer reference.
- One regression over two years assumes a constant level; a structural decline is left in the residuals and slightly pulls the slopes (CENTRAL 174 vs 180 in the generator).
- Autocorrelation-robust errors are no cure for NORTH's cooling slope: computed from 4 warm days, they give an interval of about [58, 202] that looks significant and misses the true 40. Too little data cannot be repaired by a standard-error formula.
- Linear degree days ignore wind chill, humidity, holidays and lagged effects (cold buildings take days to warm).
- The adjusted series inherits the model's errors: a 2 % change is within what a mis-specified base temperature could produce.

### G. Interview defence

*“What does weather-adjusted load tell you that actual load doesn't?”* — It separates two drivers that move together in winter: weather and underlying demand. Actual load answers “how much power was used”; adjusted load answers “how much would have been used in a normal winter”, which is what you need to judge a trend. I'd always show both, state the reference weather, and give the sensitivity with its interval — a 261 MW per HDD estimate on 729 days is solid even after allowing for autocorrelated errors, a 130 MW per CDD estimate on 4 days is not.
