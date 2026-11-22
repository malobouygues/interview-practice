> **Synthetic data** — simulated with a fixed seed so that the concepts are visible. Not market observations.

### Context

Steps 1–2 suggested that the TTF level wanders while its returns do not. Before formal tests, a researcher checks this the simple way: cut the sample into consecutive blocks and look whether the mean and the dispersion stay put. This is the intuition every stationarity test formalises.

### Objective

Write a block-statistics function and use it to see the difference between a **stationary** series, a **random walk** (stochastic trend) and a **trend-stationary** series (deterministic trend).

### Minimum theory

- **Weak (covariance) stationarity**: constant mean, constant finite variance, and a covariance between `y_t` and `y_{t-k}` that depends only on the gap `k`, not on the date. It is the version used in practice.
- **Random walk**: `y_t = y_{t-1} + ε_t`. Each shock is **permanent**; `Var(y_t) = t·σ²` grows with time; the series has no level to return to. With a constant added each period it becomes a *random walk with drift*. It is the simplest **unit-root** process and a good first description of a price level.
- **Trend-stationary**: `y_t = a + b·t + ε_t`. It trends, but shocks are **transitory**: the series always comes back to the line.
- "It trends" is a description, not a diagnosis: both processes above trend.

### Assumptions

The check compares blocks of equal length in time order. It only looks at the first two moments and has no formal error rate: it is an eye test that tells you *what to test next*.

### Your task

Implement `subsample_stats(x, parts=4)`:

- Drop missing values, then split the values into `parts` **consecutive** blocks of (almost) equal length with `np.array_split`.
- Return a `dict`:
  - `means`: list of the block means (floats, in time order),
  - `stds`: list of the block standard deviations (`ddof=1`),
  - `mean_shift`: `(max(means) - min(means)) / mean(stds)` — how far apart the block means are, in units of the typical within-block standard deviation,
  - `std_ratio`: `max(stds) / min(stds)`.

The test code simulates the three reference processes exactly as in the source document (`np.random.default_rng(0)`, 500 normal shocks) — keep it, it is the comparison you need for the explanation.

Then answer the question in the **Explain** tab.
