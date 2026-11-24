### A. Reasoning — a predictive result is only as honest as its join

The analyst's t-stat of −4.4 is exactly what a release-time mismatch produces: the join attaches each weekly figure from the Friday it describes, so on Tuesday the table already contains the number the market will only see on Wednesday at 10:30. The “prediction” is the price reaction to the release, shifted one day earlier. The defence is mechanical: join on availability, backward, and assert that nothing comes from the future.

### B. Theory (PDF A04-B, A04-E, A04-F)

- **Backward as-of join**: for each decision, the last value with key ≤ decision time. With the availability key, it is the last report already published.
- **Tolerance**: an upper bound on the age of a matched value — a missing value is better than a silently stale one.
- **Validation**: assertion (`available_at ≤ decision_time`), age distribution, manual inspection of rows around known irregularities (the late release of June 2022).
- **Look-ahead bias**: any feature using information unavailable at the decision time. A backward join on the *observation* date is still look-ahead.

### C. Implementation

Decision time = settlement in New York → UTC (same clock as `available_at`). Sort both sides, `merge_asof(..., direction="backward", tolerance=pd.Timedelta(days=10))`, then `age_days` and the assertion on matched rows.

### D. Interpretation (this dataset)

- 1,510 settlements. Age of the matched report: **5 to 14 days**, mean 7.9; 13–14 days on 23–24 June 2022, because the week of 17 June was published only on 29 June. On **27–28 June 2022** the last published report was more than 10 days old: the tolerance leaves those two days blank. (The first 5 days of 2019 have a report but no surprise: the first report has no previous week.)
- The `week_ending` join uses a not-yet-published report on **929 of 1,510** days.
- On the eve of releases: `week_ending` join → correlation **−0.245**, t **−4.43**, R² 6 %; `available_at` join → **−0.077**, t −1.35. The analyst's signal is the 10:30 reaction, relabelled.
- Over all days the correct join still shows a weak negative correlation (−0.10): a genuine post-release drift in 2020–21 — the subject of 3.5–3.6.

### E. Decision

Reject the analyst's result: it is look-ahead bias, not a strategy. Use the backward, availability-keyed table for anything predictive; keep the assertion in the pipeline.

### F. Pitfalls and limits

- `direction="nearest"` or `"forward"` would attach future reports directly.
- Joining on `release_date` *without the time* would attach a 10:30 report to a decision taken at 08:00 the same day.
- The join guarantees timing, not content: a revised value attached on the right date is still look-ahead (3.3).
- The 10-day tolerance is a judgement: it bridges most of the June 2022 delay and blanks its last two days rather than carrying a 12-day-old report.

### G. Interview defence

*“Your join is correct, but your result is weaker. Why trust it over a t-stat of −4.4?”* — Because the −4.4 uses information that did not exist at the time of the decision: it's measuring how the market reacted to the release, not predicting it. If I traded it, I'd be trying to buy before a number that the backtest already knew. The weaker number is the honest one; what's left of it still has to survive HAC errors and an out-of-sample test.
