### A. Reasoning — why this join is where point-in-time is won or lost

Weekly data and daily prices must be put side by side for any analysis. `merge_asof` is the right tool for different frequencies — but it only promises that the right-hand key is not after the left-hand key. Whether that means "known at the time" depends entirely on which key you give it.

### B. Theory (PDF, A04-B, A04-F)

- `direction="backward"`: never a future row. `"forward"`/`"nearest"` would use the future.
- Key = **availability**: the join reproduces what a trader saw at 14:30.
- `tolerance`: a maximum age; beyond it `NaN` (an interrupted series should not be silently carried).
- Post-join checks: `available_at ≤ decision_time` (assertion), age distribution, number of unmatched rows, row count unchanged.
- Frequencies: the weekly value is carried until the next release — no interpolation, which would use the next week's value.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

- 1,042 daily rows; the first two days of 2016 have no published report yet → `NaN`.
- Age of the matched report: 5 to 12 days (Wednesday release → 5 days; the following Tuesday → 11 days, 12 after a delayed release).
- Joined on `week_ending` instead, the table uses a **not-yet-published** report on **630 days out of 1,042** — every Friday, Monday and Tuesday sees next Wednesday's number.

### E. Decision

Use this table for every stock–price analysis of the project; keep `age_days` to check staleness.

### F. Pitfalls and limits

- Joining on the observation date (`week_ending`), or on the ingestion date of backfilled data.
- Forgetting to sort (merge_asof raises an error) or duplicated keys on the right (only the last one is used — deduplicate first).
- `direction="nearest"` "to be safe": it uses the future half the time.
- A backward join on the right key with the **latest revised** values is still not point-in-time if the series is revised (step 3.4).

### G. Interview defence

> **Q: "How do you merge weekly inventory data with daily prices?"**
>
> **A:** With a backward as-of join on the availability timestamp: for each settlement I take the last report released before 2:30 pm New York, with a tolerance so a missed release gives a missing value rather than a stale one. Then I assert that no matched value was published after the decision time and look at the age distribution — here 5 to 12 days. If you join on the week-ending date instead, the number appears five or six days before it was published; in my data that's 630 days out of 1,042 using information nobody had.
