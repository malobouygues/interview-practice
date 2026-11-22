> **Synthetic data** — the series of this case are simulated with fixed seeds (see `data/README.md`). Not market observations.

### Context

New case, new desk: crude oil. Your dataset (`data/crude_daily_synthetic.csv`) contains, for each business day from July 2016 to December 2019:

- `brent` — the international seaborne benchmark, $/bbl;
- `wti` — the US benchmark, delivered inland at Cushing (Oklahoma), $/bbl;
- `coffee` — an arabica coffee price, US¢/lb, added by your manager "as a control".

Your manager asks: *"Brent and WTI obviously move together. Before you compute anything, tell me **why** they should, what that should look like in the data, and what could break it. And why do you think I gave you coffee?"*

### What to write

**6–10 sentences** covering:

1. the economic mechanism that links the two crude prices;
2. what statistical signature you therefore expect — in daily returns and in price levels;
3. what could weaken or interrupt the link;
4. the role of the coffee series.

There is no number to compute yet. **Submit** your answer, then compare it with the reference answer and tick the key points you covered (self-review, not graded automatically).
