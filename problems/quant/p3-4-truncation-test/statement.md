> **Synthetic data** — the weekly stocks and WTI settlements of 3.1–3.2.

### The desk asks

> “Before you show me any model, convince me that the inputs couldn't see the future. The quant team says their features are fine because they joined everything “as of” the right date. I'd like a test, not a promise.”

### What you have

The weekly reports (with `available_at`, `surprise_mbbl`, as in 3.1) and the daily settlements. A **feature builder** is any function `build_features(stocks, prices)` returning a frame indexed by `date` with one column per feature. The Test code pad defines four builders of the same two features — the latest surprise, and the stock level against the average of the previous 52 reports:

| builder | what it does |
|---|---|
| `correct_features` | backward join on `available_at`, trailing 52-report average |
| `joined_on_week_ending` | the same features, joined on the week the report describes |
| `standardised_on_full_sample` | correct join, surprise divided by its full-sample standard deviation |
| `centred_average` | correct join, a *centred* 52-report average |

### What to find out

A test that tells, for any builder, whether past rows depend on information that arrived later.

### Minimum theory (PDF A04-E look-ahead, A04-F validation, A07-F avoiding leaks)

- **Truncation test**: build the features (1) on everything, (2) on the data *as available at a cutoff*; on the dates both builds contain, the values must be identical. A difference = look-ahead.
- “Data available at the cutoff” = reports with `available_at ≤ cutoff`, prices with `date ≤ cutoff`.
- Typical leaks: a wrong join key, a statistic computed on the full sample (mean, std, min-max scaling), a centred or backward-filled window, a forward-looking interpolation.
- **Features vs labels**: a forecast *target* is meant to look forward; it is controlled by purging the training rows (3.6), not by this test.
- One cutoff can miss a leak that only appears on some days of the week: test several.

### Assumptions

`cutoff` is a UTC timestamp string (`"2022-06-27 23:59"`). Two values are equal if they are equal or both missing.

### Your task

Implement `truncation_test(build_features, stocks, prices, cutoff)`:

1. `full = build_features(stocks, prices)`.
2. Truncate: `stocks` with `available_at <= cutoff`; `prices` with `date <= cutoff` (date part); `truncated = build_features(...)`.
3. On the dates of `truncated`, compare with `full` row by row (NaN = NaN counts as equal).
4. Return `{"rows_compared": ..., "rows_changed": ..., "first_changed": <first changed date or None>}`.

Run it on the four builders and two cutoffs in the Test code pad, check three rows by hand, then the **Explain** tab.
