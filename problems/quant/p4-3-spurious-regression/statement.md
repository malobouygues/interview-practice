> **Synthetic data** — coffee is simulated independently of crude: any relationship between them is an artefact.

### The desk asks

> “An intern sent me this: ‘log WTI on log coffee: t-stat 69, R² 0.69, and the residuals pass a unit-root test at 6 %.’ He wants to put it in the morning note. Before he embarrasses himself — what's going on? And how would I know the Brent–WTI regression isn't the same kind of thing?”

### What you have

`data/p4_crude_research_daily_synthetic.csv` — daily `brent`, `wti`, `coffee`, 2012–2019.

### What to find out

What the same regression says in levels and in daily changes, what the residuals say, and what test of the residuals is legitimate.

### Minimum theory (PDF A06-E, A08-C, A10-C)

- **Spurious regression** (Granger–Newbold): regressing one I(1) series on another unrelated I(1) series gives high R² and large t-statistics with probability close to one; the standard t distribution is invalid because the errors are non-stationary.
- **Durbin-Watson** `≈ 2(1 − ρ̂₁)`: near 0 means residuals behave like a random walk. Rule of thumb: R² > DW → suspect a spurious regression. A warning sign, not proof.
- **Differences**: regress daily changes on daily changes — both stationary, standard inference applies.
- **Cointegration** (Engle-Granger): the residuals of the levels regression are stationary. They must be tested with **Engle-Granger critical values** (`statsmodels.tsa.stattools.coint`), not with ordinary ADF p-values: OLS chose the coefficient that makes the residuals look as stationary as possible.
- Test cointegration only when a mechanism plausibly links the series.

### Assumptions

Everything in natural logs. Residual ADF with a constant and AIC lag selection.

### Your task

Implement `spurious_check(prices)` returning a frame with four rows, in order: (`wti ~ coffee`, `log levels`), (`wti ~ coffee`, `log changes`), (`wti ~ brent`, `log levels`), (`wti ~ brent`, `log changes`), and the columns `pair`, `form`, `coef`, `t`, `r2`, `durbin_watson`, `residual_adf_p_naive`, `engle_granger_p` (the last two only for levels, `NaN` for changes).

Plot the levels and the residuals in the Test code pad, then the **Explain** tab.
