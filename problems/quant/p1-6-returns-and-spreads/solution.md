### A. Reasoning — why the transformation depends on the series

Prices are analysed in changes, but each definition of change has its own unit and domain. Log returns are the best tool for an outright price (additive, scale-free) and impossible for a series that can be zero or negative. On this dataset the choice is not theoretical: WTI's expiry print and the Brent–Dubai spread both break logs.

### B. Theory

- `diff()`: P_t − P_{t−1} in USD/bbl, defined for any value; telescopes to P_T − P_0.
- `pct_change()`: P_t/P_{t−1} − 1; compounding is multiplicative.
- log return: log(1 + r_t); additive and scale-free; ≈ r_t for small moves.
- Domain: logs and % changes need P > 0 and a base far from 0.
- Gaps: a return is defined between two observations. With `NaN`s left in place, `diff()` gives `NaN` on the gap **and** on the next day, and the move across the gap is lost.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

- Brent goes from 55.00 to 78.58 USD/bbl: **+42.9 %**, or **0.357** log points. The 758 daily log returns sum to exactly 0.357; the daily % changes sum to 0.444.
- Had the holiday `NaN`s been left in, the log returns would sum to 0.256: the move across every gap (holidays and the removed fat-finger day) would have vanished.
- WTI and the Brent–Dubai spread are refused. Around the expiry, WTI's daily differences are −47.52 and +46.10 USD/bbl: still defined, but dominated by the event.

### E. Decision

| series | transformation |
|---|---|
| outright positive price (Brent, Dubai) | log returns, on observed prices |
| WTI over a period containing the negative print, any spread | `diff()` in USD/bbl |
| a growth figure for a slide | % change from the levels (not summed) |

### F. Pitfalls and limits

- Taking logs of a spread "because returns are standard": `NaN`/`inf` silently enter the data.
- Summing % changes to annualise or aggregate.
- Leaving gaps in before differencing.
- A transformation discards information: returns forget the level, so a long-run link between levels is invisible in returns (Project 4).

### G. Interview defence

> **Q: "Why log returns, and when wouldn't you use them?"**
>
> **A:** For an outright price I use log returns because they add up over time — the daily log returns of Brent sum exactly to the log of the total move — and they don't depend on the price level. I compute them between consecutive observed prices, otherwise every holiday deletes a return. I can't use them for WTI over 2020, because it printed negative at an expiry, nor for spreads, which can cross zero: there I work in absolute differences in dollars per barrel and treat the extreme day explicitly.
