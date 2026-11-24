### Reference answer

**Bottom line:** the stock report moves WTI immediately and that is all we can use. There is no robust post-release signal.

**What we could know.** At any settlement, the desk knew the latest weekly report already published — released at 10:30 New York, normally five days after the week it describes, once twelve days late — and monthly demand two months behind, in its first-estimate version. Our database stores neither fact: it dates weekly figures by the week they describe, and keeps only the latest revision of demand. Used naively, it attaches a report on 929 of 1,510 days before it existed, and shows demand about 127 kb/d higher than what we actually saw.

**What that does to research.** Joined by observation date, the latest surprise appears to predict the next day's move with a t-stat of −4.4. That is the release-day reaction moved one day earlier — look-ahead, not a signal. With availability-based joins it disappears.

**What is real.** On release days WTI moves about −0.3 % per million barrels of surprise between 10:29 and the settlement: the information is priced within hours. After that, a drift appeared in 2019–2022 (t −4.8 naively, −2.9 once overlapping windows are accounted for), but it was concentrated in 2020–2022. Frozen and tested on 2023–2024, the model does worse than predicting no move (MAE 6.2 % vs 6.0 %); re-estimated every quarter, it still does, and its coefficient shrinks.

**Recommendation.** Don't trade the drift. Keep the point-in-time pipeline — availability timestamps, demand vintages, truncation tests, purged labels — as the standard for any future signal. Caveats: one market, synthetic history, and no causal claim either way.

### Why this answer works

- It answers both questions (information set; usefulness) in the first lines.
- It turns the technical findings into consequences (“a t-stat of −4.4 that was look-ahead”, “worse than predicting no move”).
- It distinguishes the robust result (the reaction) from the fragile one (the drift) and gives the out-of-sample comparison against a baseline.
- It ends with a recommendation and a process, not with a model.

### Common weaknesses

- Leading with HAC or merge_asof instead of the answer.
- Presenting HAC-adjusted significance as proof the drift is usable.
- Reporting out-of-sample MAE without a baseline.
- Claiming the reaction is “predictable” — it is only explainable once the number is out.
