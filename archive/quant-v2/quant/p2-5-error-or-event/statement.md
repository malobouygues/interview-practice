> **Synthetic data** — simulated with fixed seeds; the refinery outage is imitated, values are invented.

### Context

Step 2.4 flagged three RBOB days. A flag is not a verdict: in energy markets the most extreme days are often the most important ones (outages, hurricanes, squeezes). The desk's rule of thumb (PDF, *Arbre K*): a data error is **isolated** — it is **not confirmed by related markets** and it **reverts** the next day; a market event is **confirmed** by related markets and/or **persists**.

### Objective

Turn that rule into explicit code, classify every extreme day, and attach an action to each.

### Minimum theory

- **Robust score** of each product's return: rolling modified z (median and MAD of the 60 previous days), as in 2.4.
- **Confirmation**: on the same day, another product has |score| > 3.
- **Reversal**: the next day's return undoes at least 80 % of today's (`tomorrow / today < −0.8`).
- **Decision**: error (reverses, not confirmed) → set the price to NaN; event (confirmed) → keep and annotate; otherwise → investigate. The day right after an error is the bounce back from the bad price, not a new event.

### Assumptions

ULSD and gasoil are the related markets of RBOB (they share crude and refinery news); one day of hindsight is acceptable for a cleaning decision.

### Your task

Implement `classify_extremes(returns, series)`. `returns` is a `DataFrame` of daily log returns (columns `rbob`, `ulsd`, `gasoil`, dates where all three exist), `series` the column to examine.

1. Score every column with the rolling modified z of 2.4.
2. Candidates: days where `|score[series]| > 5`, in date order.
3. For each candidate: `confirmed` = any **other** column has |score| > 3 that day; `reverses` = next day's return / today's < −0.8 (`False` on the last day).
4. Label and action:
   - if the previous candidate was the **previous trading day** and was a `"data error"` → `"reversal of an error"`, `"disappears once the bad price is removed"`;
   - elif `reverses` and not `confirmed` → `"data error"`, `"set the price to NaN"`;
   - elif `confirmed` → `"market event"`, `"keep and annotate"`;
   - else → `"investigate"`, `"check a second source"`.

Return a `DataFrame` with columns `date`, `return`, `score`, `confirmed`, `reverses`, `classification`, `action` (index reset). Answer in the **Explain** tab.
