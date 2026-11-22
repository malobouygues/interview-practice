### A. Reasoning — why start here

A test or a model applied to a series you have not described is blind. Two questions come first: *what does one row represent* (a daily settlement price, €/MWh, business days — a price, not a flow) and *on which scale do the statistics mean something*. Computing the same summary on the level and on the returns makes the second question concrete.

### B. Theory

- **Mean vs median.** The median ignores how extreme the extreme values are; the mean does not. Mean > median ⇒ a long right tail.
- **Variance / standard deviation.** Average squared distance to the mean (std = square root, in €/MWh). Meaningful only if the series fluctuates around a stable mean with a stable spread.
- **Skewness.** Standardised third moment. Energy prices are typically right-skewed (spikes up, slow decay).
- **Excess kurtosis.** Standardised fourth moment minus 3. A normal distribution has 0; daily commodity returns typically have several units.
- **Conventions matter.** pandas uses the sample (bias-corrected) versions: `std` with `ddof=1`, `kurt()` = *excess* kurtosis. `scipy.stats.kurtosis` with defaults is not bias-corrected, so the numbers differ slightly — always say which convention you use.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| | Price level (€/MWh) | Daily log return |
|---|---|---|
| n | 782 | 781 |
| mean / median | 21.95 / 19.37 | 0.0008 / 0.0011 |
| std | 6.42 | 0.0209 (≈ 2.1 % a day) |
| skew | 1.35 | −0.40 |
| excess kurtosis | 1.05 | 4.42 |

- The **level** is right-skewed: a few expensive months pull the mean 2.6 €/MWh above the median.
- The level's std of 6.4 €/MWh is a description of *where this particular path wandered*; on a different three-year window it would be different, and it grows with the length of the sample. It is not a risk number.
- **Returns** are centred near zero, roughly symmetric, with **excess kurtosis 4.4**: the sample has 4 days beyond 4 standard deviations, where a normal distribution would expect 0.05 such days in 781.

### E. Decision

- Quote dispersion and risk on **returns** (≈ 2.1 % per day; ×√252 ≈ 33 % annualised), never on the level.
- Do not rely on normal-distribution tail probabilities for this contract.
- The skewed, wandering level suggests a stochastic trend → steps 3–5 test it formally.

### F. Limitations and pitfalls

- Sample statistics of a non-stationary series do not estimate a fixed population value.
- Kurtosis is itself very sensitive to a handful of observations; report it, do not over-interpret its second digit.
- Forgetting `dropna()` before `len()` (the first return is `NaN`), or mixing excess and raw kurtosis.
- Describing the level and concluding about "volatility" from it.

### G. Interview defence

> **Q: "Why didn't you just report the standard deviation of the price?"**
>
> **A:** Because the price level is not stationary — its standard deviation depends on the window and keeps growing as the sample gets longer, so it doesn't measure risk. I describe the level to understand the shape (it's right-skewed, mean above median), but I measure dispersion on daily log returns: about 2 % a day here, with excess kurtosis around 4, so the tails are much fatter than normal and a Gaussian VaR would understate the risk.
