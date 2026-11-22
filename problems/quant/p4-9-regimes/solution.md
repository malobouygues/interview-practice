### A. Reasoning — why test the sample choice

Every result of 4.2–4.8 assumed one stable relationship. The desk's history contains a regulatory change that alters the arbitrage itself. With a known, economically motivated date, compare the two sides — and see what a full-sample test would have said if you had not known.

### B. Theory

- A break in the equilibrium shifts the full-sample residual; Engle-Granger's second step is an ADF test, fooled by a level shift exactly like ADF in 4.4.
- A break in the short-run dynamics changes the pass-through of returns; the Chow test (4.10) tests it formally.
- Placebo dates are a sanity check of the method.

### C. Implementation

{{code}}

`describe_period` is the one helper of the project: the same six statistics are computed for two periods.

### D. Interpretation (this dataset)

| | pre (2012–2015) | post (2016–2019) |
|---|---|---|
| n | 1,044 | 1,043 |
| mean log spread (WTI discount) | 0.169 (≈ 16 %) | 0.059 (≈ 6 %) |
| std of the spread | 0.030 | 0.020 |
| return β (pass-through) | 0.59 | 0.89 |
| return correlation | 0.79 | 0.88 |
| Engle-Granger p-value | < 0.001 | < 0.001 |
| **full-sample Engle-Granger p-value** | **0.28** | |

- After the ban ended, the discount fell from ≈ 16 % to ≈ 6 %, became less volatile, and WTI followed Brent much more closely day to day.
- Each regime is strongly cointegrated; the full sample is not. **Run on the full sample alone, the test would have said "no long-run relationship".**
- Placebos: around 2014, mean spread 0.163 vs 0.175 and pass-through 0.61 vs 0.57; around 2018, 0.059 vs 0.059 and 0.88 vs 0.89 — nothing like the jump at the real break.

### E. Decision

Treat 2012–2015 and 2016–2019 as two regimes; keep the post-2016 estimates (4.7–4.8) for anything current; test the change formally (4.10).

### F. Pitfalls and limits

- Concluding cointegration (or its absence) on a sample with an obvious break.
- Choosing the break date by scanning the data (unknown-date break tests exist but are outside this curriculum).
- Real breaks are often gradual; a sharp date is a simplification.
- Sub-period comparisons are descriptive.

### G. Interview defence

> **Q: "Your Brent–WTI relationship isn't cointegrated on 2012–2019. Doesn't that kill your model?"**
>
> **A:** No — it shows the sample mixes two regimes. Until end-2015 US exports were banned: WTI traded at about a 16 % discount and followed Brent loosely, with a daily pass-through of 0.6. From 2016 the discount is about 6 % and the pass-through 0.9. Each regime is strongly cointegrated, but a single regression over both forces one equilibrium, its residual jumps in 2016, and Engle-Granger reads the jump as a unit root. So I estimate the relationship on the current regime, using a date chosen from the policy change, not from the chart.
