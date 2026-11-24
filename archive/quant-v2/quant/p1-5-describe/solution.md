### A. Reasoning — why describe before modelling

Every later statistic inherits the shape of the data. Three questions decide what you can say: is the series a level or a change, is it dominated by a few observations, and is its dispersion stable? Describing the level, the returns and a spread side by side answers all three.

### B. Theory

- Mean vs median: the gap reveals asymmetry or extremes.
- Standard deviation of a **non-stationary level** depends on the window (it grows with the sample): it is not a risk measure. Dispersion is measured on returns.
- Quantiles are robust; skewness and kurtosis are not (a single day can make them).
- Conventions: pandas uses `ddof=1` and returns **excess** kurtosis; `scipy.stats.kurtosis` with defaults is not bias-corrected — say which one you use.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| | Brent level (USD/bbl) | Brent log return | Brent–WTI spread (USD/bbl) |
|---|---|---|---|
| n | 759 | 758 | 742 |
| mean / median | 55.90 / 57.26 | 0.0005 / 0.0014 | 3.92 / 3.70 |
| std | 14.53 | 0.0152 (≈ 24 % a year) | 2.26 |
| q05 – q95 | 27.4 – 77.8 | −2.3 % – +2.3 % | 2.18 – 6.51 |
| skew | −0.37 | −0.96 | 15.8 |
| excess kurtosis | −0.23 | 4.30 | 352 |

- **Level**: the 2020 collapse pulls the mean below the median. Its std of 14.5 USD/bbl says where this path went, not how risky Brent is.
- **Returns**: about 1.5 % a day, negatively skewed and fat-tailed — 7 days beyond 4 standard deviations (a normal distribution would give essentially none); the worst days are −7 % to −8 % (March–April 2020).
- **Spread**: a typical 3–4 USD/bbl, but one day (WTI −35.90) gives a 55 USD/bbl spread that makes the skew 16 and the kurtosis 352. Mean and std are dominated by one observation; the median and quantiles are not.

### E. Decision

Quote risk on returns; describe spreads with median and quantiles and report the event separately; never quote a normal-distribution tail probability for these returns.

### F. Pitfalls and limits

- Reporting the std of a price level as "volatility".
- Computing returns with `np.log(prices).diff()` on a series with holiday `NaN`s: every return across a holiday is lost (the sum of returns then no longer equals the total move).
- Over-reading the second digit of a kurtosis: it is itself extremely noisy.

### G. Interview defence

> **Q: "What's the average Brent–WTI spread in your data?"**
>
> **A:** The mean is about 3.9 dollars, but I wouldn't quote the mean: one day — the negative WTI expiry — produces a 55-dollar spread and drives the skewness to 16. The median is 3.7 and 90 % of days are between 2.2 and 6.5 dollars, so that's what I'd quote, and I'd mention the April 2020 event separately. For Brent itself I describe risk with daily returns, about 1.5 % a day with fat tails, not with the standard deviation of the price level.
