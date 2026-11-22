### Reference answer

> I'd object: today's spread isn't 2 % away from fair value — the fair value is wrong, because it averages two different regimes.
>
> Until end-2015 US crude exports were banned. WTI was a landlocked crude and traded at roughly a 16 % discount to Brent, following it loosely day to day. Once exports were allowed, the arbitrage route opened: the discount settled around 6 % and WTI started tracking Brent much more closely. The data say the same thing. Before vs after 2016, the average log spread is 0.17 vs 0.06 and the daily pass-through 0.59 vs 0.89. A Chow test on daily returns at the export-ban date gives F ≈ 107, while placebo dates inside each regime show nothing (p of 0.5 and 0.9). And the full-sample cointegration test itself is a warning sign: Engle-Granger gives p ≈ 0.28 over 2012–2019, although each regime on its own is strongly cointegrated — the pooled regression is forcing one equilibrium onto two.
>
> The 0.08 "fair value" is a mix of 0.17 and 0.06 that never existed in either regime. Estimated on the current regime, the equilibrium is about 0.06 — where the spread is today — so there's no signal. Deviations in this regime close at about 11 % a day (half-life ≈ 6 days): a genuine 2 % dislocation would usually be gone within a couple of weeks.
>
> The right procedure is to ask first which events could change the arbitrage (logistics, regulation), estimate the relationship within the current regime, test its stability at those dates with a test on stationary variables, and re-test regularly on recent data. What I'm not sure about: real breaks are gradual, so the exact date matters less than the regimes; a new constraint could be starting a third regime right now; and all of this describes how the spread behaved — it isn't a backtested trading strategy.

### What makes this a strong interview answer

- **Conclusion first**, then evidence, mechanism, implication and limits — the structure a PM expects.
- **Integrates the whole path**: integration order and cointegration, the danger of pooling, a known-date test on stationary variables, placebo checks, the ECM speed for the time scale.
- **Economics drives the statistics**: the break date comes from a policy change with a clear mechanism, not from scanning the chart.
- **Actionable**: says what the correct model implies for today (no signal) and how to monitor going forward.
- **Honest about uncertainty** without hiding behind it.

### Common weaknesses

- "Cointegrated, so it mean-reverts to the full-sample average" — ignoring that the equilibrium itself moved.
- Citing the Chow test without the placebo checks, or running it on price levels.
- Treating the break date as a statistical finding rather than an economic one.
- Recommending a trade without translating the model into an equilibrium level and a time scale.
