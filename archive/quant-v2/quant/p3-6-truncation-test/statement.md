> **Synthetic data** — simulated with fixed seeds; not market observations.

### Context

A feature pipeline can leak in ways that are invisible in the results until production: a centred window, a normalisation fitted on the whole sample, a mistyped `shift(-1)`. The PDF's generic detector is the **truncation test**: rebuild the features using only the data up to a past date, and compare with the features built on the full history.

### Objective

Implement the truncation test and use it on a deliberately leaky feature builder and on its corrected version.

### Minimum theory (PDF, A04-E)

1. Build the features on the complete dataset.
2. Build them again on the data **truncated** at a cutoff date.
3. On the dates up to the cutoff, compare the two.
4. A feature whose historical values change when the future is removed **depends on the future**: look-ahead.

Typical culprits: `rolling(..., center=True)`, `shift(-k)`, statistics of the whole sample (mean, std, min, max) used to normalise, `bfill`, interpolation.

### Assumptions

The builder is deterministic and only uses the data it receives.

### Your task

Implement `truncation_test(build_features, prices, cutoff)`:

- `build_features` is a function taking a `DataFrame` (index = date, column `wti_usd_bbl`) and returning a `DataFrame` of features with the same index;
- compute `full = build_features(prices)` and `truncated = build_features(prices[prices.index <= cutoff])`;
- for each column of `full`, compare its values on the dates ≤ cutoff with `truncated` (`np.allclose(..., equal_nan=True)` on float arrays);
- return the **list of column names that differ**, in the column order of `full` (empty list if none).

The test code defines `leaky_features` and `fixed_features`. Answer in the **Explain** tab.
