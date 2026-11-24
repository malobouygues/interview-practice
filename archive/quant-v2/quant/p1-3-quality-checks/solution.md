### A. Reasoning — why explicit rules, and why per series

"Remove outliers" is not a quality control: in energy, extremes are often exactly the risk you want to study. A control must say *what* it detects, *why* that is impossible or suspicious for this series, and *what* you do about it. The same number (a negative price) is an error for Brent and a real event for WTI's front month.

### B. Theory

- Three outcomes per anomaly (A02-C): **correct** a certain error, **investigate** an unknown cause, **document** a real feature of the data.
- A jump test compares a value with its own **recent past**: `rolling(5, min_periods=3).median().shift(1)`. The `shift(1)` keeps the check free of the value itself (and of the future); the median keeps it robust to the bad print.
- Confirmation by related markets: a genuine move appears in related benchmarks; an isolated factor-10 jump that disappears the next day is a typing error.

### C. Implementation

{{code}}

A loop over the flagged values keeps each rule readable; the log is built at the end with one `DataFrame` call.

### D. Interpretation (this file)

| date | series | value | issue | action |
|---|---|---|---|---|
| 2020-04-20 | wti | −35.90 | negative WTI print | keep and document |
| 2021-03-15 | brent | 549.70 | jump vs last 5 days | set to NaN |

- **2021-03-15**: Brent prints 549.70 while WTI is 52.69 and Dubai 52.54, and Brent is back near 55 the next day: a decimal shift. Set to NaN and log it.
- **2020-04-20**: WTI −35.90 while Brent is 19.06; the next day WTI is positive again. A storage-driven expiry squeeze: keep it, and remember that log returns and percentage changes are undefined around it (step 1.6).

### E. Decision

Apply the actions (the test code does it) and keep the log next to the dataset. The corrected file is `data/p1_crude_prices_clean_synthetic.csv`, used from step 1.4 on.

### F. Pitfalls and limits

- `prices[prices > 0]` on every column: deletes a real event.
- A full-sample mean/std z-score as the reference: contaminated by the outlier and uses future data.
- Correcting without logging: the correction disappears with the next delivery, and nobody can audit the result.
- Thresholds (×2, ×0.5, 5 days) are judgement calls: state them, and check the results are not sensitive to them.

### G. Interview defence

> **Q: "Your data has a negative oil price. Do you drop it?"**
>
> **A:** Not without knowing which oil price. Brent or Dubai at zero or below would be a data error. WTI's front-month contract actually went negative at expiry when storage was full, so a negative WTI print can be genuine: I keep it and document it. I check against the other benchmarks on the same day: here Brent and Dubai were positive and WTI recovered the next day, consistent with a contract-specific squeeze. By contrast, a Brent print ten times its recent level, with WTI and Dubai unchanged, is a decimal error, and I set it to missing with a logged reason.
