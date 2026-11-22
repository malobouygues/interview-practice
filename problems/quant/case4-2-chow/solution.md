### A. Reasoning — why Chow, and why on returns

Step 4.1 *described* a change; a sceptic will ask whether 0.59 vs 0.89 could be sampling noise. The Chow test answers that for a date known in advance — here the end of the export ban, an event with a mechanism, not a date read off the chart. But the test is only as good as the regression it is applied to: its F distribution requires stationary variables and well-behaved errors, which is why it is run on daily returns, not on price levels.

### B. Theory

- Restricted model (H0): one line for the whole sample → SSR_p. Unrestricted (H1): one line per sub-period → SSR_1 + SSR_2 ≤ SSR_p always.
- F = [(SSR_p − SSR_1 − SSR_2)/k] / [(SSR_1 + SSR_2)/(n − 2k)]: the improvement in fit per extra parameter, relative to the residual variance. Under H0 (and the assumptions) F ∼ F(k, n − 2k).
- Assumptions: known date; stationary regressors; serially independent, homoskedastic errors — and the *same* error variance in both regimes.
- On I(1) levels the residuals are persistent (Case 2): SSR comparisons are dominated by slow drifts, and F explodes even when nothing changed.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Regression | date | F | p | reject |
|---|---|---|---|---|
| WTI on Brent, log returns, 2012–2019 | 2016-01-01 | 106.9 | < 0.001 | yes |
| same, post regime only (from mid-2016) | 2018-01-01 (placebo) | 0.08 | 0.92 | no |
| same, pre regime only (2012–2015) | 2014-01-01 (placebo) | 0.69 | 0.50 | no |
| **log levels**, post regime only | 2018-01-01 (placebo) | 66.8 | < 0.001 | yes — **invalid** |

- The short-run relationship changed at the end of the export ban: the pass-through rose from ≈ 0.59 to ≈ 0.89, far beyond sampling noise.
- At dates where nothing happened, the test correctly finds nothing — the placebos are the evidence that the procedure is not trigger-happy.
- On levels, the same placebo "rejects" with F = 67. Nothing changed at that date (4.1 shows identical statistics on both sides): the rejection is the spurious-regression problem again.

### E. Decision

- The regime change is statistically established for the short-run dynamics and economically explained (arbitrage opened).
- Use post-2016 parameters for anything current; report pre-2016 results as a different regime.
- Run Chow (or any break test) on a regression with stationary variables; for the level relation, compare sub-period cointegration results (4.1) rather than F-testing levels.

### F. Limitations and pitfalls

- Choosing the date from the data: searching for the date with the largest F makes the F distribution invalid (unknown-date break tests are outside this track).
- Ignoring the equal-variance assumption: if volatility differs strongly across regimes, the test is distorted.
- Applying it to I(1) levels (last row).
- A rejection says *that* the coefficients differ, not *which* one or *why* — look at the sub-period estimates and the economics.

### G. Interview defence

> **Q: "How would you test whether the Brent–WTI relationship changed after the export ban was lifted?"**
>
> **A:** The date is known in advance, so a Chow test fits: estimate the regression on the whole sample and separately before and after the date, and compare the residual sums of squares with an F test — the null is that the coefficients are the same in both periods. I run it on daily log returns, because the test needs stationary variables and well-behaved errors. At end-2015 F is about 107: the daily pass-through went from roughly 0.6 to 0.9. As a sanity check, placebo dates inside each regime give p-values of 0.5 and 0.9. Running the same test on price levels rejects even at a placebo date, which just shows it's invalid there.
