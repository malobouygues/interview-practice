> **Synthetic data** — simulated prices; the event log imitates well-known episodes, but every number is invented.

### The desk asks

> “The crack history has some enormous daily moves. The data team wants to winsorise every return at the 1st and 99th percentiles ‘to be safe’. I'm not convinced: some of those moves are the reason I'm asking. Go through them and tell me which ones are real.”

### What you have

- `data/p2_products_wide_synthetic.csv` — the output of 2.1 (index `date`; `brent`, `gasoil`, `ulsd`, `rbob`, `jet` in USD/bbl, plus cracks).
- `data/p2_market_events_synthetic.csv` — the desk's event log: `start`, `end`, `event`, `markets` (products affected, separated by `;`).

### What to find out

For every extreme observation: is it a data error (to correct or blank), or a market event (to keep)? And when the evidence is unclear, what is the effect of keeping it?

### Minimum theory (PDF A03-B outliers, A05-B)

- **Impossible values**: a refined product cannot trade at ≤ 0 → set missing.
- **Unit errors** show in *levels*: a price ≈ 100×, 42×, 10× (or the inverse) the average of its two neighbours is a scale problem — divide, do not delete.
- **Scores on log returns**: z-score `(r − mean) / std`; **modified z-score** `0.6745 (r − median) / MAD` (robust: one huge error cannot inflate it); **IQR** flag outside `[Q1 − 3·IQR, Q3 + 3·IQR]`.
- **Masking**: a gross error inflates the standard deviation and hides the other extremes from the z-score. Hence an **iterative** procedure: fix gross errors, *then* score.
- **Investigation**: did related markets move the same way the same day? Does the event log cover it? A market-wide or logged move is information; an isolated, unexplained one is doubtful — keep it, flag it and measure its influence.

### Assumptions

- Unit factors tested: 100, 42, 10, 0.1, 1/42, 0.01, within 3 %.
- Candidates: |modified z| > 6. Sister markets: brent ↔ gasoil, ulsd; gasoil ↔ ulsd, jet; ulsd ↔ gasoil, jet; rbob ↔ ulsd, brent; jet ↔ gasoil, ulsd. “Confirmed” = a sister moved the same way by at least half as much.
- Decision order: event covering the date and the product → `keep_event`; else confirmed → `keep_market_move`; else `keep_doubtful`.

### Your task

Implement `investigate_extremes(prices, events)` on a copy of the five price columns:

1. **Pass 1 (levels)**, series by series: prices ≤ 0 → record `set_missing` and blank them; then on the non-missing values, ratio to the mean of the previous and next value; a ratio within 3 % of a unit factor → record `correct_unit` and divide by the factor.
2. **Pass 2 (returns)**: for each series, log returns of its non-missing repaired prices; z, modified z, IQR flag; `flag_counts` per series: `z_above_4`, `modified_z_above_6`, `iqr_3`.
3. **Pass 3 (investigation)**: for each candidate, apply the decision order.

Each decision row: `date`, `series`, `value`, `check`, `decision` (+ `ret`, `z`, `modified_z`, `iqr_flag` in pass 3). Return `{"decisions": <sorted by date, series; fresh index>, "flag_counts": <indexed by series>, "prices": <repaired prices>}`. Then the **Explain** tab.
