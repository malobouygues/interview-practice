### A. Reasoning — an extreme value is a question, not an answer

A daily move of +20 % in a product price is either the most important observation of the year (a refinery shut, a harbour squeezed) or a typing error. Statistics can only say that it is *unusual*; deciding *what* it is needs levels, neighbours, related markets and the event log. And because one gross error distorts every statistic computed on the same series, the work has to be iterative.

### B. Theory (PDF A03-B, A05-B)

- **Three scores, three behaviours**: the z-score uses mean and std (both inflated by the extremes it is looking for → masking); the modified z-score uses median and MAD (robust); the IQR rule uses quartiles (robust, but with fat tails it flags many ordinary days at 1.5·IQR — hence 3·IQR here).
- **Errors vs events** (A03-B): impossible values, scale errors, frozen values, duplicates are *errors* → correct or blank. Statistically extreme but economically valid moves are *events* → keep. Unclear cases → keep, annotate, measure sensitivity.
- **Winsorisation** caps values at a percentile: it treats errors and events the same way, leaves errors partly in and removes part of the events. It is a modelling choice for a specific estimator, never a cleaning default.

### C. Implementation

Pass 1 works on levels with `observed.shift(1)` and `shift(-1)` on the non-missing values (so a holiday does not break the comparison). Pass 2 recomputes returns *after* the repairs. Pass 3 is a plain loop over candidates: the event log filtered by date and `markets.str.contains(series)`, sister returns looked up on the same date.

### D. Interpretation (this dataset)

| decision | count | examples |
|---|---|---|
| `correct_unit` | 1 | RBOB 14 May 2019: 8,732 $/bbl = ×100 the neighbours (cents) |
| `set_missing` | 1 | gasoil 25 Nov 2021: 0.00 |
| `keep_event` | 11 | hurricane 28 Aug 2017 (RBOB +19 %, ULSD +12 %); 9 Mar 2020 price war (Brent −24 %); jet in the lockdowns; NY Harbor squeeze 31 Oct 2022 (ULSD +20 %, gasoil +3 %) |
| `keep_market_move` | 11 | 2 Jan 2019, 14 Apr 2020, 7 Jul 2021: all products together |
| `keep_doubtful` | 1 | jet 15 Jun 2021: +10.8 %, sisters +2 %, no event, half reversed next day |

- **Masking**: with the cents error inside, RBOB's return std is **0.162** (0.019 after the fix) and the hurricane day's z is **1.2**; its modified z is **12.0** either way.
- **Effect of the errors**: RBOB 2019 average crack **45.0 → 10.1** $/bbl; gasoil November 2021 average crack **18.21 → 22.51**.
- **Doubtful point**: June 2021 jet crack 17.32 with it, 16.83 without (crack that day 27.71 vs 17.95 and 21.38 around it).
- Flags by method: similar counts here once the errors are fixed (jet: z 8, modified z 7, IQR 10) — the methods disagree most *before* the repairs.

### E. Decision

Correct one record, blank one, keep 23 with a reason each. Do not winsorise. The 2022 widening of the diesel crack is a **regime** (every day of 2022 is high), not a set of outliers — no score flags it, and no cleaning should touch it.

### F. Pitfalls and limits

- Using next-day information (reversal, the next neighbour) is fine for historical cleaning; in real time you would have to wait a day to confirm an error.
- The event log is the desk's memory: an event missing from it turns a real move into “doubtful”. Keep the log maintained.
- “Confirmed by sister markets” can be wrong if the vendor's error affects several products at once (same feed).
- Threshold 6 on the modified z-score is a choice; report how many candidates another threshold would add.

### G. Interview defence

*“Why not delete the extreme observations? They will dominate your regression.”* — Because some of them are exactly what the trader is asking about. A hurricane that shuts Gulf Coast refineries *is* the supply-shock signal. I correct what is demonstrably an error, blank what is impossible, keep events with their label, and if one point still drives a result I show the result with and without it — that is information for the decision, not a reason to hide the point.
