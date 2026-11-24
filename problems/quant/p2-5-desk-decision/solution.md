### Reference answer

**Mostly physical.** The crack widened because European distillate stocks fell far below normal — about 23 % under their 5-year average in September 2022 — and the crack tracks that deficit closely: roughly one dollar of crack per point of deficit, so a 20 % deficit is worth about 20 $/bbl. That estimate holds with heteroskedasticity-robust standard errors.

**Not a data problem.** The vendor data did have errors — a RBOB price sent in cents, a 0.00 gasoil print, a frozen feed, and import months where a non-reporting country appeared as zero — but each was found, repaired or blanked, and none of them is near the 2022 widening. The extreme daily moves that remain are real: the 2017 hurricane, the 2020 collapse, the New York Harbor squeeze in October 2022. We kept them on purpose: they are how the crack behaves when supply is short, which is exactly the question. Deleting or winsorising them would make the market look calmer than it is.

**What the statistics don't say.** This is an association over 78 months dominated by one tight cycle, not a proof of causality — stocks and cracks feed back on each other. The outage effect looks significant with naive standard errors but not with robust ones. The straight line under-predicts the crack when stocks are very low (the response is convex), and the residuals are autocorrelated. So the relationship supports the physical story; it is not yet a sizing tool.

**Watch next:** stocks against the 5-year average (a rebuild should compress the crack), outage announcements, and import volumes now that Russian barrels have been replaced. I'd fit a non-linear version before using any number for position sizing.

### Why this answer works

- Conclusion first, in the trader's units ($/bbl per point of stocks).
- Separates data errors (fixed, and irrelevant to the conclusion) from events (kept, and central to it).
- Says what robust inference does (honest uncertainty) and does not do (fix the shape of the model).
- Ends with monitorable variables and a clear limit on use.

### Common weaknesses

- Opening with methodology instead of the answer.
- “The R² is 0.93, so the model is good” — R² says nothing about whether the shape or the inference is right.
- Treating the 2022 values as outliers to be removed.
- Presenting HC3 as a fix for a misspecified model.
