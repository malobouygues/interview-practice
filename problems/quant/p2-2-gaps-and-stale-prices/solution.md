### A. Reasoning — why the cause of a gap decides its treatment

The same `NaN` calls for opposite treatments depending on its origin (A03-A). A series that did not exist yet, a value not yet published, a holiday on one exchange and a frozen feed are four different facts. Treating them with one `fillna` either invents prices, uses the future, or keeps fake data.

### B. Theory

- **Forward fill** assumes the last known price is still the best estimate: acceptable for a short holiday, wrong for long gaps (stale prices create fake zero returns and an artificial spread between a fresh and a stale price). Always with a limit, always flagged.
- **Backward fill / interpolation** put a future value in the past: look-ahead.
- **Stale detection**: identical consecutive values counted with a run id, `(~same_as_previous).cumsum()`.
- **One row per date** is a property of the index; `drop_duplicates()` compares values only.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

- 784 raw rows, **2 duplicated dates**. `drop_duplicates()` would have removed **13** rows: besides the 2 real duplicates, it deletes distinct holidays whose rows are entirely empty (they compare equal).
- Imputed values: 23 (Brent), 26 (ULSD), 26 (RBOB), 25 (gasoil), 13 (jet) — almost all holidays on one side of the Atlantic.
- Gasoil, 8–15 October 2018: six identical prices (629.01). The first is kept; the five copies become missing; the limited forward fill carries 629.01 for two more days (flagged) and three days stay missing.
- Jet stays missing before 1 March 2018 (305 days) and on the last three days.

### E. Decision

Use the treated prices (`data/p2_products_treated_synthetic.csv`) for returns and rolling features, keep the `filled` flags, and check that key results do not change when imputed days are excluded.

### F. Pitfalls and limits

- `fillna(method="bfill")`, `interpolate()` or a full-sample mean on prices.
- Unlimited forward fill: weeks of fake zero returns, volatility understated.
- Filling the ragged edge: the "latest" price is invented.
- Treating a frozen feed as a calm market.
- The thresholds (2 days, 4 identical values) are judgement calls: state them.

### G. Interview defence

> **Q: "How do you handle missing prices?"**
>
> **A:** By cause first. Before a series starts or after the last publication I leave it missing — filling would invent prices. For a holiday on one exchange I carry the last settlement for at most two days and flag it, because the last price is what a trader would actually have; I never interpolate or backward-fill, since that uses tomorrow's price. And I look for stale feeds: six identical gasoil settlements in a row aren't a quiet market, they're a frozen feed, so I keep the first and treat the copies as missing.
