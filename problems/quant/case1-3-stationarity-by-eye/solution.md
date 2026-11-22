### A. Reasoning — why look at blocks before testing

Every estimator you will compute later — a mean, a correlation, a regression coefficient — assumes there is *one* stable quantity to estimate. If the mean of the first year and the mean of the last year are far apart relative to the day-to-day spread, there is no single mean. Comparing blocks is the fastest way to see it, and it tells you which formal test to run and with which specification.

### B. Theory

- **Weak stationarity**: E[y_t] = μ, Var(y_t) = σ² < ∞, Cov(y_t, y_{t−k}) = γ_k for all t.
- **Random walk**: y_t = y_0 + Σ ε_s. Mean of a block = the level reached at that time, which itself wanders; Var(y_t) = tσ². Shocks never fade.
- **Trend-stationary**: y_t = a + bt + ε_t. Block means rise by b × block length, but deviations from the line have constant spread. Remedy: remove the line (detrend), *not* difference — step 6.
- Strict stationarity (the whole joint distribution is time-invariant) is rarely checkable and not needed here.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Series | block means | mean_shift | std_ratio | reading |
|---|---|---|---|---|
| white noise | 0.08, −0.09, −0.08, −0.01 | 0.17 | 1.13 | stationary |
| random walk | 3.9, 4.3, −9.4, −11.3 | 3.48 | 1.44 | means wander, shocks accumulate |
| trend-stationary | 3.2, 9.3, 15.5, 21.8 | 8.92 | 1.04 | means climb regularly, spread stable |
| TTF price | 17.5, 21.8, 17.4, 31.1 €/MWh | 5.01 | 4.21 | wanders like a random walk; spread larger when price is high |
| TTF log returns (4 blocks) | ≈ 0 each | 0.14 | 1.10 | looks stationary |

The TTF level has the random-walk signature: no level it returns to, and dispersion that scales with the price (another reason to use *log* returns). Its returns look stable.

### E. Decision

- Level: suspect a unit root → formal tests (steps 4–5) before any statistic on the level is trusted.
- Returns: candidate stationary series → confirm formally.
- A series whose means drift *regularly* with stable dispersion may be trend-stationary → test with a trend term (step 6).

### F. Limitations and pitfalls

- No significance level: "mean_shift = 0.5" is not a test result. A persistent but stationary series can show sizeable block differences in a short sample, and a random walk can look calm by chance.
- Means drifting does **not** distinguish a deterministic from a stochastic trend; the remedy differs (detrend vs difference).
- Only two moments: a series can be stable in mean and variance yet unstable in its dependence on the past.

### G. Interview defence

> **Q: "What does it mean for a price to have a unit root, in plain words?"**
>
> **A:** That shocks are permanent. Today's price is yesterday's price plus a surprise, so every surprise stays in the level forever; the variance keeps growing with the horizon and the price has no anchor to go back to. You see it when you cut the sample into blocks: the block means wander instead of fluctuating around one value. That's why I don't trust statistics on the level and work with returns — and why I then confirm it with ADF and KPSS rather than by eye.
