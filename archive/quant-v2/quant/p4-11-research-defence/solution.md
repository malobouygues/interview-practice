### Reference answer

> **Conclusion: since US exports were allowed, WTI and Brent are tied by a long-run equilibrium — a WTI discount of about 6 % with an elasticity close to one — and deviations close at about 11 % a day. The relationship changed at the end of 2015, so a "fair value" fitted on 2012–2019 mixes two regimes and is not a valid signal today.**
>
> The hypothesis was an arbitrage: two substitutable light sweet crudes, linked by exports and transport, should keep a stable discount. I worked on synthetic daily Brent and WTI prices for 2012–2019, with Dubai as a related benchmark and coffee as a control with no mechanism. I started with the exports-allowed regime, from mid-2016, a choice made before looking at the results and tested at the end.
>
> Prices behave as I(1): ADF cannot reject a unit root in log levels (p ≈ 0.15–0.19) and rejects strongly in returns. So I do not use OLS inference on levels — coffee on Brent gives t = 36 in levels and 0.8 in returns. In returns, WTI moves 0.89 % for a 1 % Brent move (95 % interval 0.86–0.92). That simple model beat the alternatives: Dubai is 95 % correlated with Brent, triples the standard error and comes out with a meaningless negative sign; coffee and lagged Brent add nothing; BIC prefers the simple model.
>
> For the levels, Engle-Granger gives a statistic of −7.4 against a −3.34 critical value: cointegrated. Coffee illustrates why the correct critical values matter: its naive residual p-value is 0.038, the correct one 0.50. The error-correction model gives a same-day pass-through of 0.89, a long-run elasticity of 0.98, and an adjustment of −0.115 a day (t ≈ −8), a half-life of about six business days.
>
> Stability: before 2016 the discount averaged about 16 % with a pass-through of 0.6; after, 6 % and 0.9. Each regime is strongly cointegrated, but the full sample is not (p ≈ 0.28), because one regression cannot fit two equilibria. A Chow test on returns at the export-ban date gives F ≈ 107, while placebo dates inside each regime show nothing.
>
> For the trader: the 2 % "richness" comes from averaging a 16 % and a 6 % discount — within the current regime, 0.06 is the equilibrium, so there is no signal. The 3 % cheapness after the outage is a genuine deviation; historically half of such a gap closes in about a week. But that is a statistical description, not a guaranteed profit. Any position should compare the expected move (about 1.5 % in a week) with costs and carry, be sized to the spread's daily noise, and have an exit if the gap keeps widening — because widening is also how a regime change starts. The first question is whether the outage blocks the arbitrage itself.
>
> Limits: synthetic data, a single relationship, a test with limited power, break dates as judgement, and no backtest or P&L claim. Next, I would re-test the relationship on recent data regularly, study Brent–Dubai and ULSD–gasoil the same way, and redo the work on real data with point-in-time vintages.

### What makes this a strong research defence

- **One clear conclusion**, then hypothesis → data → transformations → model → evidence → interpretation → limits → next steps.
- **Every method justified by the previous result** (I(1) → no levels OLS → cointegration → ECM → stability).
- **Rejected alternatives shown**, with the criterion used.
- **Numbers with units and their uncertainty**; statistical and economic significance kept apart.
- **The trader's two situations answered differently**, for reasons that come from the research.

### Common weaknesses

- "Cointegrated, so it will converge to the full-sample average."
- Quoting the levels R² or t-statistic as evidence.
- A list of tests without a conclusion, or a conclusion without limits.
- Recommending a trade without equilibrium level, time scale, costs and an exit.
