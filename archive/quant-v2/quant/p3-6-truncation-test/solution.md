### A. Reasoning — why a test rather than a code review

Leakage hides in reasonable-looking lines: a centred window "for smoothness", a z-score "to normalise", a maximum "to rescale". Reading the code catches some of them; a mechanical test catches all leaks of this kind at once, including the ones in code you did not write. Its logic is simple: a feature known at a past date cannot change when you learn what happened afterwards.

### B. Theory (PDF, A04-E, A07-F)

- Truncation test: features(full data) and features(data ≤ cutoff) must agree on dates ≤ cutoff.
- Leak types it detects: windows including future rows (`center=True`), negative shifts, statistics fitted on the full sample (mean, std, min, max, normalisation), backward fill, interpolation.
- Leak types it **cannot** detect: wrong timestamps in the raw data (observation date used as availability), revised values used as if known — those are properties of the inputs, handled with availability dates and vintages.
- Sensitivity: some leaks only show for some cutoffs (here `share_of_max` leaks only if the sample maximum comes after the cutoff): test several cutoffs.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| builder | cutoff | features that change |
|---|---|---|
| leaky | 2017-12-29 | ma_5_centered, zscore_full_sample, share_of_max, return_tomorrow |
| leaky | 2019-06-28 | ma_5_centered, zscore_full_sample, return_tomorrow |
| fixed | 2017-12-29 | none |

`return_lag1` passes in both builders. `share_of_max` passes at the 2019 cutoff only because the sample maximum (September 2018) is already in the truncated data — a leak can be invisible at one cutoff and obvious at another.

### E. Decision

Run the truncation test on every feature pipeline, at several cutoffs, before any statistical result is reported; keep it as an assertion in the project's checks.

### F. Pitfalls and limits

- Testing a single cutoff (see `share_of_max`).
- Comparing with `==` on floats instead of `allclose` with `NaN`s treated as equal.
- Believing a passed truncation test makes the analysis point-in-time: inputs can still be revised or mis-dated.

### G. Interview defence

> **Q: "How do you test that your features don't leak future information?"**
>
> **A:** With a truncation test: I build the features on the full history, build them again on data cut at a past date, and check that every feature is identical on the dates both versions share. If a historical value changes when I remove the future, it was using the future. On a deliberately leaky builder it flags the centred moving average, the full-sample z-score, the price divided by the sample maximum, and a shift of minus one. It doesn't replace availability dates and vintages — if the raw data are revised or mis-dated, the test can't see it.
