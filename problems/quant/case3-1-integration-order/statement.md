> **Synthetic data** — simulated with fixed seeds (see `data/README.md`). Not market observations.

### Context

Case 2 showed that Brent and WTI genuinely co-move day to day. The open question is about **levels**: do the two prices share a long-run equilibrium they keep returning to? That is **cointegration** — and it is only defined for series with the same *order of integration*. So the first step of any cointegration analysis is to establish that order for each series.

### Objective

Automate the "test, difference, re-test" loop of Case 1 to find the order of integration, and apply it to both prices and to the spread between them.

### Minimum theory

- A series is **I(d)** if it must be differenced **d** times to become stationary.
  - **I(0)**: stationary in levels (returns, a mean-reverting spread).
  - **I(1)**: stationary after one difference (most prices).
  - **I(2)**: two differences — rare; often a misread structural break.
- **Cointegration**: two I(1) series are cointegrated if some combination `y − β·x` is I(0). They drift, but together.
- Differencing too little leaves a unit root; differencing too much (over-differencing) adds noise and artificial dependence (Case 1, step 6).

### Assumptions

At each stage the verdict uses ADF + KPSS with a constant (`regression='c'`), as in step 1.5. The loop stops at the first `"stationary"` verdict.

### Your task

Implement `integration_order(x, max_order=2)`:

- Drop missing values. For `d = 0, 1, …, max_order`: compute the ADF + KPSS verdict (`'c'`, `autolag="AIC"`, `nlags="auto"`, 5 % level, KPSS warning silenced) exactly as in step 1.5. If the verdict is `"stationary"`, stop: the order is `d`. Otherwise difference once more (`x.diff().dropna()`).
- Return `{"order": d, "verdicts": [...]}` where `verdicts` lists the verdict obtained at each stage, in order. If no stage is `"stationary"`, `order` is `None`.

You may copy your function from step 1.5 into this file.

Then answer the question in the **Explain** tab.
