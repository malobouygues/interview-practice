### Reference answer

> **Verdict: the dataset is usable after a small number of documented corrections — with one genuine extreme event that every analysis must treat explicitly.**
>
> It contains daily settlements of Brent (ICE), WTI (NYMEX) and Dubai in USD/bbl from January 2019 to December 2021, one row per business day. Each benchmark follows its own holiday calendar, so missing values on UK or US holidays are structural and stay missing. The raw vendor export was loaded with explicit types and day-first dates; I removed 5 rows that had been loaded twice and resolved 2 dates the vendor re-sent with corrected values by keeping the latest load. Values marked as holidays or not delivered are kept as missing, not filled. One Brent print (15 March 2021, 549.70) was ten times its recent level while WTI and Dubai were normal: a decimal error, set to missing and logged. I deliberately kept WTI's −35.90 print on 20 April 2020: it is a front-month expiry squeeze, not an error, but it breaks log returns and dominates any moment-based statistic. The clean data are stored in a small SQLite table keyed by date, so reloading is harmless.
>
> On a typical day Brent trades about 3.7 USD/bbl above WTI (90 % of days between 2.2 and 6.5) and about 1.2 above Dubai. April 2020 is a separate episode: the WTI discount averaged about 10 USD/bbl that month. Daily moves are strongly linked: about 0.87 for Brent and WTI on ranks — the plain Pearson figure is 0.32 only because of the expiry days — and about 0.88 for Brent and Dubai. The 0.99 correlations of price levels mean little: all three prices fell and recovered together.
>
> Limits: there is no second source to confirm the corrections, the quality thresholds are judgement calls, and these statistics describe 2019–2021 only — prices are not stationary. Next, I would test whether the spreads are stable and mean-reverting, and whether the relationship changes across regimes (Project 4).

### What makes this a strong answer

- **Provenance and counts**: raw → clean → table, with the number of rows each step touched.
- **Errors vs events** separated, with the evidence used (other benchmarks on the same day).
- **Robust statistics** for spreads, and the estimator choice for correlation explained.
- **Honest limits** and a concrete next step.

### Common weaknesses

- "I cleaned the data" without saying what changed — impossible to audit.
- Dropping the negative WTI print, or reporting a 0.32 correlation without explanation.
- Quoting level correlations as evidence of a relationship.
