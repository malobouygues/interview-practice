### A. Reasoning — why "it trends" is not a diagnosis

Diesel consumption grows with activity along a stable path: a cold winter lifts it for a few months, then it returns to the path. A price absorbs news permanently. The remedy follows from the mechanism — remove a line in the first case, take differences in the second — and the wrong choice damages the data in a measurable way.

### B. Theory

- Trend-stationary: detrending recovers the stationary part; differencing gives `b + u_t − u_{t−1}` — stationary but noisier, with artificial negative dependence (over-differencing).
- Difference-stationary: differencing recovers the shocks; detrending leaves a random walk around a line.
- ADF 'c' vs 'ct': a deterministic trend makes 'c' fail and 'ct' reject; a stochastic trend makes both fail.
- Seasonal profile estimated on the detrended series, so that December is not credited with eleven more months of trend than January.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| | diesel demand (kb/d) | Brent monthly average (USD/bbl) |
|---|---|---|
| trend per year | +12.9 | −2.9 (a fitted line, meaningless) |
| seasonal amplitude | 79.5 (winter peak) | 6.9 (noise) |
| ADF p, 'c' / 'ct' | 0.97 / < 0.001 | 0.34 / 0.87 |
| std detrended / differenced | **11.6** / 15.6 | 18.3 / **4.2** |
| decision | **detrend** | **difference** |

### E. Decision

Model demand as deviations from trend and season; model Brent in returns. Re-test transformed series and keep the ability to rebuild levels for communication.

### F. Pitfalls and limits

- Differencing every series after an ADF non-rejection.
- A linear trend over a sample with a break (2008, 2020) produces misleading residuals: test sub-periods.
- With short samples (e.g. three years of monthly prices) the 'ct' test has little power: lean on the economics.
- Testing a seasonal series without removing the seasonality.

### G. Interview defence

> **Q: "Both series trend. Why do you difference Brent but detrend demand?"**
>
> **A:** Because they're different kinds of trend. After removing the winter seasonal profile, ADF on demand doesn't reject with a constant but rejects strongly once I add a time trend — the trend is deterministic and shocks die out, so I remove the line. On Brent, ADF rejects with neither specification: the trend is stochastic, shocks are permanent, so I work in returns. Differencing demand would raise its dispersion by a third and throw away the level; detrending Brent leaves a residual four times more dispersed than monthly changes — the line explains nothing.
