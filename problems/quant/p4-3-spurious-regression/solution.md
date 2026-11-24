### A. Reasoning — the regression is answering a question nobody asked

Two prices that wander will usually wander apart or together over some stretch of eight years; a levels regression then finds a “relationship” in the shared shape of their paths. The intern's t-stat measures that, not a link between coffee and oil. The cure is to ask the question on the right object: daily changes for co-movement, and an Engle-Granger test — with its own critical values — for a long-run equilibrium, *if* there is a mechanism.

### B. Theory (PDF A06-E, A08-C, A10-C)

- With I(1) regressors and non-stationary errors, OLS t-statistics diverge as the sample grows: significance is guaranteed and meaningless.
- **DW**: residual autocorrelation at lag 1; a levels regression with DW ≈ 0 has residuals close to a random walk.
- **Engle-Granger**: (1) OLS in levels, (2) unit-root test on the residuals with EG critical values (more negative than ADF's, because the cointegrating coefficient was estimated). H0: no cointegration.
- **Mechanism first**: Brent and WTI are linked by physical arbitrage (shipping, refinery substitution, export capacity); coffee and WTI by nothing.

### C. Implementation

`np.log`, then a loop over the two partners: OLS in levels (params, tvalues, rsquared), `sm.stats.durbin_watson`, `adfuller(resid, regression="c")[1]` for the naive p-value, `coint(y, x)` for the EG p-value; the same OLS on `diff().dropna()`.

### D. Interpretation (this dataset)

| pair | form | coef | t | R² | DW | residual ADF p (naive) | EG p |
|---|---|---|---|---|---|---|---|
| WTI ~ coffee | levels | 1.87 | **68.6** | **0.69** | **0.016** | **0.059** | **0.17** |
| WTI ~ coffee | changes | 0.005 | 0.25 | 0.000 | 1.97 | — | — |
| WTI ~ Brent | levels | 0.93 | 521.8 | 0.99 | 0.046 | < 0.001 | **0.001** |
| WTI ~ Brent | changes | 0.74 | 66.4 | 0.68 | 2.12 | — | — |

- Coffee: R² (0.69) far above DW (0.016); the relationship disappears in changes; EG does not reject. The naive residual test (p 0.059) nearly declared a coffee–oil equilibrium.
- Brent: low DW in levels too (0.046) — DW alone cannot separate spurious from cointegrated; EG rejects and changes co-move strongly.

### E. Decision

Kill the coffee note. For Brent–WTI, a long-run relationship is plausible economically *and* supported statistically over the full sample — but the full-sample relationship averages two regimes (4.4).

### F. Pitfalls and limits

- “The residuals are stationary at 6 %” with ordinary ADF p-values is the classic false positive; the EG critical values exist for this reason.
- EG is sensitive to which variable is on the left in small samples, to structural breaks and to the deterministic terms.
- A regression in changes answers a short-run question; it throws away the long-run information that cointegration keeps — the two are complements (ECM, 4.4).
- Spurious relations can also appear between stationary but highly persistent series in short samples.

### G. Interview defence

*“R² is 0.69 and t is 69 — how can that be nothing?”* — Because both series are random walks and the sample is one particular path of each. With non-stationary residuals the t-statistic doesn't follow a t distribution; it grows with the sample size whether or not there's a link. The checks are cheap: DW of 0.016, no relation in daily changes, and an Engle-Granger p-value of 0.17. And there's no economic channel from coffee to oil — I wouldn't have run the test in the first place.
