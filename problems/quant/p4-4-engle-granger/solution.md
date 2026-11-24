### A. Reasoning — an equilibrium is a mechanism with parameters, and parameters can change

The physical link between Brent and WTI is arbitrage: if WTI is cheap enough relative to Brent, someone moves or substitutes barrels. That justifies testing for cointegration. But the strength of the arbitrage depends on what is allowed — and until end-2015 US crude could not be exported freely. So the question is not only “is there an equilibrium?” but “which one, when?”.

### B. Theory

- **Engle-Granger**: OLS of log WTI on log Brent, then a unit-root test on the residuals with EG critical values; rejecting H0 = the gap is stationary.
- **Long run vs short run**: the levels regression gives the equilibrium; the regression in changes gives the day-to-day pass-through; the ECM links both through the speed of adjustment α.
- **Structural change at a known date** (A05-D, A06): sub-period estimates; Chow F on a stationary regression; placebo dates to check that the test does not reject everywhere. Chow assumes equal variance — volatility regimes can make it over-reject.
- **Averages across regimes** describe no period in particular.

### C. Implementation

Daily changes computed once, before splitting; a dict of three samples and one loop (`coint`, two OLS fits, the mean spread); SSRs of the short-run regressions; the Chow formula and `stats.f.sf(F, k, n − 2k)`.

### D. Interpretation (this dataset)

| period | days | EG stat | EG p | long-run β | mean spread ($/bbl) | pass-through (SE) |
|---|---|---|---|---|---|---|
| full sample | 2,087 | −4.53 | 0.001 | 0.929 | **9.36** | 0.737 (0.011) |
| before 2016 | 1,044 | −5.34 | < 0.001 | 0.974 | **15.86** | **0.588** (0.014) |
| from 2016 | 1,043 | −8.88 | < 0.001 | 0.994 | **2.85** | **0.904** (0.016) |

- Chow at 1 Jan 2016: **F = 113.3**, p ≈ 10⁻⁴⁷.
- Placebos: 2017-06 **F 0.14** (p 0.87), 2018-01 **F 0.07** (p 0.93); 2014-07 F 2.50 (p 0.08); 2014-01 **F 3.84 (p 0.02)** — Brent volatility doubled in mid-2014, which violates Chow's equal-variance assumption.
- Optional ECM: before 2016 α = **−0.055** (t −6.4), half-life **12.3 days**, γ 0.59; from 2016 α = **−0.118** (t −9.2), half-life **5.5 days**, γ 0.90.

### E. Decision

Yes, there is an equilibrium — and it changed when exports opened: a discount of about 3 $/bbl, closed twice as fast, with WTI following Brent almost one-for-one. Any spread trade must use post-2016 parameters; the 2013 15-dollar discount and the full-sample 9-dollar “average” are history. Monitor what could change the regime again: export capacity, pipeline constraints, Gulf Coast disruptions (the 2017 hurricane shows up as a one-day WTI drop).

### F. Pitfalls and limits

- A full-sample EG rejection does not mean one stable equilibrium: the residuals carry a level shift at the break.
- The break date is known here (a policy change); searching for the “best” date in the data would require different critical values.
- Differencing each sub-period separately drops the change across the break from the second period but not from the pooled regression: the two sides of the F ratio then use different days (F 114.4 instead of 113.3 here — harmless, but not a Chow test).
- Chow on the levels regression would be invalid (non-stationary errors before cointegration is established); it is applied to the regression in changes.
- The ECM is an extension: two-step estimation, constant parameters within each regime, no other drivers (transport costs, quality).

### G. Interview defence

*“Cointegration is significant over 2012–2019, so mean-revert the spread to its average.”* — To which average? The full-sample mean of 9.36 $/bbl sits between a 15.86 regime and a 2.85 regime and describes neither. The cointegration is real, but its parameters changed when the export ban ended, and the Chow test says so with F = 113. I'd only trade around the post-2016 equilibrium, sized on its half-life of about five days, and watch the arbitrage capacity that created it.
