### A. Reasoning — two questions hidden in one correlation

“Brent and WTI move together” can mean “their levels trended the same way over eight years” or “on a given day, when Brent moves, WTI moves too”. The first is true of almost any two prices in a commodity cycle — coffee included. The second is a statement about co-movement. Separate them before testing anything.

### B. Theory (PDF A05)

- **Levels** of prices are persistent and trending: their correlation is dominated by the low-frequency path (A05-D).
- **Log returns** are approximately additive over time and comparable across price levels.
- **Robust statistics**: median, Spearman; **tail statistics**: skewness, excess kurtosis.
- **Volatility clustering**: calm and agitated periods group together; a rolling standard deviation shows the regimes; a single full-sample std averages them away.

### C. Implementation

`prices.set_index("date")`, `corr()` on levels; `np.log(...).diff().dropna()` for returns; `corr(method="spearman")`; `rolling(60).std() * np.sqrt(252)`; `groupby(index.year)` for yearly volatility and spread.

### D. Interpretation (this dataset)

- Levels: Brent–WTI **0.996**, WTI–coffee **0.821**.
- Returns: Brent–WTI **0.824** (Pearson), **0.804** (Spearman); WTI–coffee **0.006**.
- Brent returns: mean −0.023 %, median −0.014 %, std **1.77 %**/day, skew −0.09, excess kurtosis **0.98**.
- Volatility: 60-day annualised from **14.9 %** (1 Nov 2012) to **47.7 %** (22 Sep 2014); by year 18.3 % (2012), 37.5 % (2015), 26.6 % (2019).
- Spread Brent − WTI: **19.7** (2012), 21.4 (2013), 16.2 (2014), 6.1 (2015), then **1.5–4.1** $/bbl (2016–2019).

### E. Decision

Discard level correlations as evidence (coffee proves the point). Brent and WTI do co-move day by day, but the spread collapsed around 2015–2016: there may be an equilibrium, and it may have changed. The next steps test what kind of series these are (4.2), what a levels regression can fake (4.3) and whether the equilibrium is real and stable (4.4).

### F. Pitfalls and limits

- Simple returns vs log returns: close for small moves, different for large ones; log returns are needed for additivity.
- A full-sample volatility (1.77 %) mixes 1.2 % days and 2.6 % days: risk estimated on it is wrong in both regimes.
- Pearson close to Spearman here; with a single extreme day (a negative WTI print, for example) they can diverge sharply.

### G. Interview defence

*“0.996 correlation — isn't that proof that WTI follows Brent?”* — It's proof that both went down in 2014 and up after 2016. Coffee has 0.82 with WTI on the same measure and nothing to do with oil; on daily returns coffee falls to 0.006 while Brent–WTI stays at 0.82. The returns are the evidence of co-movement; whether the levels are tied by an equilibrium is a separate test.
