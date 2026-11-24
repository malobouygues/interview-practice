### A. Reasoning — why Chow, and why on returns

Step 4.9 *described* a change; a sceptic asks whether 0.59 vs 0.89 could be noise. The Chow test answers for a date known in advance — here a policy change with a mechanism. But the test is only as good as the regression it is applied to: its F distribution needs stationary variables and well-behaved errors, so it is run on daily returns, not on price levels.

### B. Theory

- Restricted model (one line, H0) vs unrestricted (one line per sub-period): SSR_pre + SSR_post ≤ SSR_pooled always.
- F = improvement per extra parameter ÷ residual variance; F(k, n − 2k) under H0 and the assumptions.
- Assumptions: known date; stationary regressors; independent, homoskedastic errors with the same variance in both regimes.
- On I(1) levels the residuals are persistent: SSR comparisons pick up slow drifts and F explodes even when nothing changed.

### C. Implementation

{{code}}

The three regressions are written out one by one: they are the test.

### D. Interpretation (this dataset)

| regression | date | F | p | reject |
|---|---|---|---|---|
| WTI on Brent, log returns, 2012–2019 | 2016-01-01 | 106.9 | < 0.001 | yes |
| same, post regime only | 2018-01-01 (placebo) | 0.08 | 0.92 | no |
| same, pre regime only | 2014-01-01 (placebo) | 0.69 | 0.50 | no |
| **log levels**, post regime only | 2018-01-01 (placebo) | 66.8 | < 0.001 | yes — **invalid** |

The short-run relationship changed at the end of the export ban; at dates where nothing happened the test finds nothing; on levels it "finds" a break at a placebo date — the spurious-regression problem again.

### E. Decision

The regime change is statistically established for the short-run dynamics and economically explained. Use post-2016 parameters for anything current.

### F. Pitfalls and limits

- Choosing the date from the data (searching for the largest F) invalidates the F distribution.
- Ignoring the equal-variance assumption.
- Applying the test to I(1) levels.
- A rejection says the coefficients differ, not which one or why.

### G. Interview defence

> **Q: "How would you test whether the Brent–WTI relationship changed after the export ban was lifted?"**
>
> **A:** The date is known in advance, so a Chow test fits: estimate the regression on the whole sample and separately before and after the date, and compare residual sums of squares with an F test — the null is identical coefficients. I run it on daily log returns, because the test needs stationary variables and well-behaved errors. At end-2015 F is about 107: the daily pass-through went from roughly 0.6 to 0.9. Placebo dates inside each regime give p-values of 0.5 and 0.9; on price levels the same test rejects even at a placebo date, which just shows it's invalid there.
