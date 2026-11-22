### A. Reasoning — why transform at all

Statistics and tests need a quantity whose behaviour is comparable across time. A price level is not (step 1); its *changes* usually are. But "change" has three definitions with different units and properties, and choosing the wrong one silently breaks either the arithmetic (adding % changes) or the maths (log of a negative spread).

### B. Theory

- `diff()`: P_t − P_{t−1}, in €/MWh. Additive over time (the sum telescopes to P_T − P_0) but its scale grows with the price level.
- `pct_change()`: P_t / P_{t−1} − 1. Readable ("+3 %"), but compounding is multiplicative.
- log return: log P_t − log P_{t−1} = log(1 + r_t). Additive over time **and** scale-free; ≈ the % change for small moves (log(1.02) = 0.0198).
- Domain: log and % change need P > 0 (and a base far from 0).

### C. Implementation

{{code}}

`prices.dropna() <= 0` ignores missing values: a gap is not a negative price, it stays `NaN` in every column.

### D. Interpretation (this dataset)

- Total move over 2017–2019: 18.00 → 32.76 €/MWh, i.e. **+82.0 %**, or **0.599** in log points.
- The sum of the 781 daily log returns is exactly **0.599**.
- The sum of daily % changes is ≈ 0.77 — not +82 %; compounding them, Π(1 + r) − 1, gives back 0.82.
- On the hand example, +10 % then −10 % ends at 99, not 100; in logs, +0.0953 − 0.1054 = −0.0101 = log(0.99) exactly.

### E. Decision

| Series | Transformation for analysis |
|---|---|
| outright price (TTF, Brent) | log returns |
| spread, crack, calendar spread, anything ≤ 0 | `diff()` |
| growth figure for a slide | % change (computed from the levels, not summed) |

### F. Limitations and pitfalls

- A transformation **removes information**: returns forget the level, so any long-run relationship between levels is invisible in returns (that is what Case 3 is about).
- Taking logs of a spread "because returns are standard" — it crashes, or worse, silently produces `NaN`/`inf` when a value is ≤ 0.
- Annualising or aggregating % changes by summing them.
- Computing returns across a gap without noticing (a 3-day return labelled as a daily one).

### G. Interview defence

> **Q: "Why log returns rather than simple returns?"**
>
> **A:** For statistics and aggregation: log returns add up over time — the sum of daily log returns is exactly the log of the total price ratio — and they don't depend on the price level, so a 1 €/MWh move at 15 and at 40 aren't treated as the same thing. For small moves they're almost identical to % changes, which I'd still use to communicate. The one case where I'd use neither is a spread that can go negative: there I work in absolute differences.
