### A. Reasoning — why "0" is the most dangerous number in physical data

A price that is missing shows up as `NaN`; an import that is missing often arrives as `0`. Summed naively, a single non-report looks exactly like a collapse in demand — the kind of "signal" that ends up in a trader's morning note. The fix is economic before it is technical: a country does not stop importing diesel from every origin at once.

### B. Theory

- Long → wide: `groupby(["month", "importer"]).sum().unstack("importer")`. Absent rows become `NaN` automatically.
- Simultaneity: all origins at zero in the same month for the same reporter = a reporting failure, not a market fact (A03-A).
- Aggregation follows the nature of the variable: flows are summed, stocks take the end-of-period value, prices are averaged.
- `min_count` prevents a partial sum from being read as a total.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| month | naive sum | careful total |
|---|---|---|
| 2018-07 | 1,123.7 | 1,123.7 |
| **2018-08** | **830.5** | **NaN** (France did not report) |
| 2018-09 | 1,292.1 | 1,292.1 |
| **2019-12** | **1,172.2** | **NaN** (Germany not reported yet) |

The naive series shows a 26 % drop in August 2018 that never happened. Genuine zeros (India → Germany in six months, Saudi Arabia → UK in three) are kept: those countries reported and simply received no cargo from that origin.

### E. Decision

Use the careful total; if a continuous regional series is needed, either restrict to months with complete reports or estimate the missing country explicitly (and say so) — never zero.

### F. Pitfalls and limits

- `fillna(0)` on physical flows.
- Summing a ragged edge: the latest month always looks weak.
- The all-zero rule is an assumption: a country could in principle import nothing for a month (an embargo); check the documentation when it matters.

### G. Interview defence

> **Q: "European diesel imports dropped 26 % in August 2018 in your data. What happened?"**
>
> **A:** Nothing — France didn't report that month and the aggregator wrote zeros for every origin. A country doesn't stop importing diesel from all its suppliers at once, so an all-zero month is a missing report, not zero imports. I keep genuine zeros, like a month with no cargo from India, but I set non-reports to missing and only compute the regional total when every country has reported. Otherwise a reporting gap turns into a fake demand collapse — and the latest month always looks weak because of late reporters.
