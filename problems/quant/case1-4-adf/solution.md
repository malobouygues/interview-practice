### A. Reasoning — why this test, and why not just `adfuller(y)`

The question "does the TTF level have a unit root?" decides whether level statistics, correlations and regressions on the level can be trusted. ADF is the standard test for it. But its answer depends on a specification you choose (deterministic terms, lags) and on a null hypothesis you must read correctly — the p-value is meaningless without both.

### B. Theory

- Regression: Δy_t = [c] + [bt] + γ y_{t−1} + Σ φ_i Δy_{t−i} + e_t.
- **H0: γ = 0 (unit root)**. **H1: γ < 0** (stationary around 0 / c / c + bt).
- Statistic = t-stat of γ; under H0 it follows the Dickey-Fuller distribution, which is shifted to the left of Student's t: the 5 % critical value is about −2.87 with a constant (vs −1.65 for a one-sided t-test). Using Student tables would reject far too often.
- **Lags** whiten the residuals; too few → biased test, too many → lost power. AIC picks them.
- **Deterministic terms** set H1. Omitting a real trend biases the test towards *not* rejecting; including useless terms lowers power.
- **Power**: the test separates a unit root from a very persistent stationary process badly in short spans. Ten years of monthly data is little information about long-run behaviour, and sampling more often over the same ten years barely helps.
- **Breaks**: a stationary series with a shift in level looks like a series with permanent shocks.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| Series | spec | stat | 5 % crit | p | reading |
|---|---|---|---|---|---|
| TTF level | c | −0.39 | −2.87 | 0.91 | compatible with a unit root |
| TTF log returns | c | −27.8 | −2.87 | < 0.001 | unit root rejected |
| trend-stationary | c | −0.66 | −2.87 | 0.86 | *false* unit root — trend omitted |
| trend-stationary | ct | −22.8 | −3.42 | < 0.001 | rejected once the trend is in |
| stationary, 40 obs | c | −1.52 | −2.94 | 0.52 | not rejected: low power |
| stationary + level shift | c | −1.63 | −2.87 | 0.47 | not rejected: the break fools ADF |

### E. Decision

- **p < 0.05**: reject the unit root *under this specification*. It does not establish constant variance, absence of breaks, or predictability.
- **p > 0.05** (the TTF level): "the data do not allow me to reject a unit root" — **not** "the series has a unit root", and **not** "difference it". Next: check the deterministic terms against the chart (trend? → 'ct'), look for breaks (sub-periods), consider the sample length, and run KPSS (step 5). Difference only if the evidence agrees, the economics agree (a price) and the analysis needs it.

### F. Limitations and pitfalls

- Running ADF with default settings and differencing whenever p > 0.05.
- Reading a non-rejection as proof of H0 (the 40-observation and level-shift examples are both stationary).
- Testing ten specifications and keeping the one that gives the desired answer.
- Testing a seasonal series without dealing with the seasonality first.

### G. Interview defence

> **Q: "Your ADF on the price gives p = 0.91. So the price has a unit root?"**
>
> **A:** No — it means I can't reject a unit root. The null of ADF is the unit root, so a high p-value is absence of evidence against it, not evidence for it. The test has low power against very persistent stationary processes, and a structural break can make a stationary series look like a unit root. So I check the specification — constant only, because the chart shows no deterministic trend — look for breaks, and cross-check with KPSS, whose null is the opposite. For a price, a unit root is also what economic theory leads you to expect, so if KPSS rejects stationarity too, I'll treat the level as I(1) and work in returns.
