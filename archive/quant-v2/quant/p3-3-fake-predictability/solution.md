### A. Reasoning — why the same data give a signal and no signal

Nothing in the data changes between the three runs — only the date at which the stock number is assumed to be known. The market's reaction to the report happens at the release. Any alignment that "knows" the number before the release moves that reaction into the future window and turns it into apparent predictive power. This is the most common way a publication delay manufactures a lead-lag.

### B. Theory (PDF, A04-E, A05-D)

- Outcome vs features: future prices are allowed in the **outcome** (next-5-day return) and forbidden in the **signal**.
- Look-ahead through misalignment: joining on the observation date puts the value before its publication.
- Efficient reaction: if prices absorb the report at the release, a correctly aligned signal has little left to predict.
- Ingestion date ≠ availability for backfilled data.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| alignment | n | corr(stock change, next 5-day WTI return) |
|---|---|---|
| `week_ending` (look-ahead) | 1,033 | **−0.19** |
| `available_at` (correct) | 1,030 | **+0.02** |
| `ingested_at` (backfill) | 252 | ≈ −0.05, meaningless |

On the release day itself, the stock change and that day's WTI return correlate at **−0.53**: the information is priced when it is published. The −0.19 "signal" is that same reaction, seen through a window that starts before the release.

### E. Decision

Reject the signal. Any study of fundamentals vs prices must align on availability; a predictive claim must survive the correct alignment (here it does not).

### F. Pitfalls and limits

- Trusting a correlation whose timing you have not audited.
- Building the outcome with `shift(-5)` and then, by mistake, a feature with a negative shift too.
- Concluding "no effect of stocks on prices": the effect is large — it is simply contemporaneous, not predictive.
- Daily settlement data cannot show intraday timing (the 10:30 reaction); a finer analysis would need intraday prices.

### G. Interview defence

> **Q: "Inventory builds predict WTI falls over the next week. Would you trade it?"**
>
> **A:** Not before checking the alignment. The report covers the week to Friday but is released the next Wednesday at 10:30. If you date the number on Friday, the next week's return includes Wednesday's reaction to the release, so it looks predictive — in my data the correlation is −0.19. Dated at its actual release, the correlation drops to 0.02. The market does react strongly on the release day, about −0.5 correlation with that day's move, but that's information being priced at publication, not a forecast you could have traded.
