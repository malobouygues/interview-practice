### Reference answer

> **Finding: day-to-day changes in the US diesel crack are mostly noise. Two candidate explanatory variables have a stable, economically sensible effect — yesterday's move, which tends to partly reverse, and how far the crack is from its 60-day average, which tends to close. The crack level itself is strongly seasonal: about 19.5 USD/bbl in January against 14 in summer, the heating season.**
>
> All products were first converted to USD per barrel — ULSD and RBOB from gallons (×42), gasoil and jet from tonnes (÷7.45 and ÷7.88) — before computing any crack. Gaps were treated by cause: the jet series is left missing before it existed and on the last unpublished days. Holiday gaps on one side of the Atlantic carry the last settlement for at most two days, and every such value is flagged. A gasoil feed frozen for six days in October 2018 was treated as missing after its first value. One row per date was enforced on the date index: a plain `drop_duplicates()` would have deleted eleven distinct empty holiday rows. In the European import data, an apparent 26 % fall in August 2018 was a country that did not report; non-reports are missing, not zero.
>
> Extremes were flagged with a robust score computed only on past data, then classified with evidence. An RBOB print ten times too large, unconfirmed and reversed the next day, was removed. The August 2017 refinery outage, confirmed across products, was kept and annotated: it is real risk, not noise. The classic z-score would have missed that event entirely, because the error inflated the standard deviation.
>
> Every feature is computed for an origin on the morning of day t, from settlements up to t−1: price-based features are shifted by one day, calendar variables are not. A truncation test — rebuilding the features on data cut at a past date — gives identical values. Volatility, the rolling gasoil correlation and the heating-season dummy were dropped: their relation with daily changes is not stable across 2017–18 and 2019.
>
> One trap: yesterday's NYMEX move "predicts" today's gasoil move (correlation 0.36), but only because ICE Gasoil settles two hours earlier — it is not a tradable lead. The correlations involved are small, the data are synthetic, and the cleaning thresholds are judgement calls; next, I would test these variables in a simple, parsimonious regression and check their stability across sub-periods.

### What makes this a strong answer

- **Conclusion with magnitudes**, distinguishing the level (seasonal) from the daily change (mostly noise).
- **Every data decision justified by its cause**, with the counter-example it avoided.
- **Information set stated and verified** (shift + truncation test).
- **Honest about weak signals** and about the settlement-time artefact.

### Common weaknesses

- "I cleaned the data and removed outliers" — no causes, no evidence, no counts.
- Keeping features because their in-sample correlation is the largest.
- Presenting the one-day ULSD → gasoil correlation as a trading signal.
