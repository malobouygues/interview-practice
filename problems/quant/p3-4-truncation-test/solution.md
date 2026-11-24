### A. Reasoning — test the pipeline, not the intention

Every look-ahead bug was written by someone who meant well. A truncation test does not care about intentions: if the value attached to 17 June changes when you delete what arrived after 27 June, then the 17 June value was built with information from the future. It is cheap, generic (any builder) and catches leaks that code review misses.

### B. Theory (PDF A04-E, A04-F, A07-F)

- **Invariance under truncation**: a causal feature at date t is a function of data available at t only, so deleting later data cannot change it.
- **Where leaks hide**: the join key (observation vs availability), global statistics (mean, std, scaling, imputation fitted on the full sample), centred or two-sided windows, `bfill`, interpolation, revised data.
- **Labels** look forward by definition; for them the rule is different: a training row can only be used once its label is fully realised before the estimation origin (purging).
- **Coverage of the test**: a leak that depends on the calendar (between a Friday and the next Wednesday) needs a cutoff inside that window.

### C. Implementation

Two calls of the builder; boolean filters for the truncation; `full.loc[truncated.index]` aligns the rows; `(a == b) | (a.isna() & b.isna())` then `.all(axis=1)` gives unchanged rows.

### D. Interpretation (this dataset)

| builder | cutoff Mon 27 Jun 2022 | cutoff Thu 30 Jun 2022 |
|---|---|---|
| `correct_features` | **0** / 878 | 0 / 881 |
| `joined_on_week_ending` | **6** / 878 (from 17 Jun 2022) | **0** / 881 |
| `standardised_on_full_sample` | **868** / 878 | 870 / 881 |
| `centred_average` | **123** / 878 (from 29 Dec 2021) | 115 / 881 |

- The full-sample standardisation contaminates almost every row: one global statistic is enough.
- The centred window contaminates the last half-year before any cutoff.
- The week-ending leak is invisible on Thursday 30 June: every report describing a week before that date was already published. On Monday 27 June, the weeks of 17 and 24 June were not (published 29 June) — six rows change.
- Manual check: on 22–24 June the correct builder attaches the week of 10 June (published 15 June); 27–28 June are blank (tolerance); on 29 June it attaches the week of 24 June, published the same morning together with the late week of 17 June.

### E. Decision

Accept only builders that pass at a set of cutoffs (month-ends *and* days between a week's end and its release). The decision table used in 3.5–3.6 is built like `correct_features`; its 10-day target is purged in 3.6.

### F. Pitfalls and limits

- Passing at one cutoff proves little; failing at one cutoff proves a leak.
- The test cannot detect revised values if the database only stores the latest vintage — truncating rows does not restore old versions (3.3).
- Comparing floats exactly is fine here because both builds run the same code on the same inputs; across environments, compare with a tolerance.

### G. Interview defence

*“We used merge_asof backward, so there's no look-ahead.”* — The join is one place a leak can hide, not the only one. Here, a centred rolling mean and a z-score on the full sample both pass through a correct merge_asof and still leak, and a week-ending join only shows up if you cut on the right day. I'd run the truncation test at several cutoffs as part of the pipeline, and I'd purge the labels separately.
