### A. Reasoning — why check the mechanics before the signal

A lead-lag correlation is easy to compute and easy to misread: the sign convention of `shift` is a classic source of inverted conclusions, and settlement prices of different exchanges are not taken at the same moment. Before calling something a lead, ask which clock each price was measured on.

### B. Theory

- Cross-correlation at lag k: corr(x_{t−k}, y_t). Here a simple loop with `shift(k)` — explicit about the sign.
- Settlement-time artefact: if market A closes before market B, news between the two closes is in B today and in A tomorrow → B appears to "lead" A by one day.
- Publication delays create the same illusion for fundamental data (Project 3).
- Levels: shared trends make every lag look strongly correlated.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| lag k | −3 | −2 | −1 | 0 | **+1** | +2 | +3 |
|---|---|---|---|---|---|---|---|
| ULSD → gasoil (returns) | 0.06 | 0.00 | −0.04 | 0.75 | **0.36** | −0.03 | 0.05 |
| Brent → gasoil (returns) | 0.04 | 0.02 | −0.07 | 0.72 | **0.28** | −0.04 | 0.04 |
| ULSD → gasoil (levels) | 0.94 | 0.96 | 0.97 | 0.98 | 0.98 | 0.97 | 0.96 |

- Yesterday's ULSD and Brent moves correlate with today's gasoil move (0.36 and 0.28), while the reverse is ≈ 0. Gasoil settles two hours earlier: it "catches up" the next day with news it had not yet priced at its close.
- Not exploitable at settlement prices: by the time ULSD settles, gasoil is already trading on the same news.
- Levels: 0.94–0.98 at every lag — no information about timing.

### E. Decision

Do not use lagged US moves as a "leading indicator" of gasoil without intraday prices synchronised in time. For research on settlement data, either align the clocks or treat a one-day lag between exchanges as a known artefact.

### F. Pitfalls and limits

- Inverting the sign of `shift` (concluding that gasoil leads).
- Searching for the best lag over many lags and series on the whole sample, then reporting it as a discovery.
- Correlating levels.
- Different holiday calendars: aligning on dates where both settled (done here) is necessary.

### G. Interview defence

> **Q: "Yesterday's NYMEX diesel move predicts today's ICE gasoil move. Can we trade it?"**
>
> **A:** I'd first check the clocks. ICE Gasoil settles at 5:30 pm London, two hours before NYMEX and Brent, so news arriving in between shows up in today's ULSD settlement but only in tomorrow's gasoil settlement. That alone produces a one-day "lead" of about 0.36 in my data, with nothing in the reverse direction. It's a measurement artefact: when ULSD settles, gasoil is already trading the news, so you can't trade it at those prices. I'd only believe a lead-lag after synchronising the timestamps.
