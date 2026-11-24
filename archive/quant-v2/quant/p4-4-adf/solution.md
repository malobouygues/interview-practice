### A. Reasoning — why test before regressing levels

Whether OLS inference in levels means anything depends on whether the series are stationary. A price that behaves like a random walk has no stable mean or variance to estimate, and regressing one such series on another produces spurious significance (4.6). ADF is the test for a unit root — but its answer depends on a specification you choose and on a null hypothesis you must read correctly.

### B. Theory

- **H0: unit root**; **H1: stationary** (around 0, a level, or a trend).
- Dickey-Fuller distribution: shifted left of Student's t (5 % critical value ≈ −2.87 with a constant, ≈ −3.42 with a trend, ≈ −1.94 with none).
- Deterministic terms set H1: omitting a real trend biases towards non-rejection; useless terms lower power.
- Lags: AIC-chosen; check the conclusion is not driven by one lag choice.
- Power: weak against very persistent stationary processes and in short spans; a level shift makes a stationary series look non-stationary.
- I(d): number of differences needed. Prices ≈ I(1), returns ≈ I(0); an I(0) combination of I(1) series = cointegration.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| series | spec | p-value | reading |
|---|---|---|---|
| log Brent | c | 0.15 | unit root not rejected |
| log WTI | c | 0.19 | unit root not rejected |
| Brent / WTI returns | n | < 0.001 | stationary → prices ≈ **I(1)** |
| log spread Brent − WTI | c | < 0.001 | stationary → **I(0)** |
| random walk (simulated) | c | 0.73 | not rejected |
| trend-stationary | c / ct | 0.86 / < 0.001 | *false* unit root without the trend |
| stationary, 40 obs | c | 0.52 | not rejected: low power |
| stationary + level shift | c | 0.47 | not rejected: fooled by the break |

On the log spread, 0, 5 or 20 fixed lags all reject strongly: the conclusion does not depend on the lag choice.

### E. Decision

Both prices are treated as I(1) (consistent with theory for asset prices): **no ordinary OLS inference in levels**. The spread looks I(0): test cointegration formally (4.7). Never difference automatically after a non-rejection — check the trend, breaks and sample length first (4.5).

### F. Pitfalls and limits

- Reading p > 0.05 as "has a unit root" (or "must be differenced").
- Default settings without thinking about `c`/`ct`/`n`; trying all and keeping the convenient one.
- Ignoring breaks (Case 4.9 shows one in the longer sample).
- A non-rejection on a short sample says little either way.

### G. Interview defence

> **Q: "ADF on Brent gives p = 0.15. So Brent has a unit root?"**
>
> **A:** No — I can't reject a unit root, which isn't the same as proving one. ADF's null is the unit root and it has low power against slow mean reversion, and a structural break can make a stationary series look like a unit root. What I can say is that Brent and WTI behave like I(1) series — no rejection in levels, strong rejection in returns, which matches what you expect for prices — so I won't run OLS inference on the levels. But the log spread between them is clearly stationary, which is exactly what cointegration would predict, so the next step is an Engle-Granger test.
