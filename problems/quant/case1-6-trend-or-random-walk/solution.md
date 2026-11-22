### A. Reasoning — why the word "trend" is not enough

Two series can drift upward for opposite reasons. Diesel consumption grows with activity along a fairly stable path: a cold winter pushes it up for a few months, then it returns to the path. A price absorbs every piece of news permanently. The remedy follows from the mechanism — remove a line in the first case, take differences in the second — and choosing wrongly damages the data in a measurable way.

### B. Theory

- **Trend-stationary**: y_t = a + bt + u_t, u stationary. Detrending recovers u. Differencing gives Δy_t = b + u_t − u_{t−1}: still stationary, but noisier (Var(Δu) = 2(1 − ρ₁)Var(u)) and with an artificial negative dependence — *over-differencing*.
- **Difference-stationary**: y_t = y_{t−1} + b + ε_t. Differencing recovers the shocks. Detrending leaves Σε (a random walk around a line): still non-stationary.
- **ADF 'c' vs 'ct'**: with a deterministic trend, 'c' typically fails to reject (the omitted trend looks like a unit root) while 'ct' rejects. With a stochastic trend, neither rejects.
- **Deterministic seasonality** (same profile each year) is removed by monthly means — here computed on the *detrended* series, so that later months are not credited with more trend than earlier ones. A seasonality whose shape drifts would call for a seasonal difference instead.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| | Diesel demand (kb/d) | TTF monthly average (€/MWh) |
|---|---|---|
| trend per year | +12.9 | +5.0 (a fitted line, meaningless for a random walk) |
| seasonal amplitude | 79.5 (winter peak) | 3.1 (noise) |
| ADF p, 'c' | 0.97 | 0.41 |
| ADF p, 'ct' | < 0.001 | 0.08 |
| std detrended | 11.6 | 4.7 |
| std differenced | 15.6 | 1.9 |
| decision | **detrend** | **difference** |

- Demand: the non-stationarity "seen" by ADF with a constant was the omitted trend. Differencing would raise the dispersion by about a third (15.6 vs 11.6) and discard the level.
- TTF: detrending leaves a residual more than twice as dispersed as the monthly changes — the line does not capture a stochastic trend.

### E. Decision

- Demand → model deviations from trend and season (or include a trend in whatever model comes next); do not difference it by reflex.
- TTF → differences / log returns.
- Then re-test the transformed series (ADF + KPSS) and be able to rebuild the level for communication.

### F. Limitations and pitfalls

- A trend can bend or break (2008, 2020): a linear trend over a period containing a break produces misleading residuals; test sub-periods.
- With only 36 monthly points (TTF), the 'ct' p-value of 0.08 is close to the threshold: the decision leans on the economics (a price) as much as on the test.
- Differencing automatically after an ADF non-rejection is one of the most common errors: it is the wrong answer for a trend-stationary series and for a break.
- Testing a seasonal series without removing the seasonality.

### G. Interview defence

> **Q: "Both series trend. Why do you difference the price but detrend the demand?"**
>
> **A:** Because they're different kinds of trend. After removing the seasonal profile, ADF on demand doesn't reject with a constant but rejects strongly once I add a time trend — the non-stationarity was a deterministic trend, shocks die out, so I remove the trend. On the price, ADF rejects with neither specification: the trend is stochastic and shocks are permanent, so I difference. Differencing demand would over-difference it — its dispersion goes up by a third — and detrending the price leaves a residual that still wanders. The economics agree: consumption follows activity, a price has no anchor.
