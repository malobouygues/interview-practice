> **Synthetic data** — monthly table from 2.3; relationships simulated, not estimated from real markets.

### The desk asks

> “I see the crack moving with stocks. Put a number on it: how much is a stock deficit worth, do refinery outages matter, and how much should I trust those numbers? Last time someone showed me a regression, the t-stats were too good to be true.”

### What you have

`data/p2_monthly_table_synthetic.csv` — the output of 2.3: `month`, `gasoil_crack` (monthly average, USD/bbl), `stocks_vs_5y_pct`, `outages_kbd`, `refinery_utilisation_pct`, imports, … (78 months, 2017-01 to 2023-06).

### What to find out

The size of each effect in its units, whether the usual standard errors can be trusted, and whether the model's shape fits the market.

### Minimum theory (PDF A08-B/C, A10-C)

- **OLS**: `crack = a + b1·stocks_vs_5y + b2·outages + b3·utilisation + e`. Each coefficient is “$/bbl of crack per unit of the regressor, the others held fixed”.
- **Heteroskedasticity**: the variance of `e` changes across observations. OLS coefficients stay unbiased, but the usual standard errors are wrong.
- **White's test**: regress the squared residuals on the regressors, their squares and cross-products; LM = n·R². **H0: constant variance.** A small p-value rejects it. (`statsmodels.stats.diagnostic.het_white(resid, X)` → LM, p, F, p.)
- **HC3 standard errors** (`fit(cov_type="HC3")`): valid under heteroskedasticity of unknown form, conservative with few observations. They change SEs, t, p and intervals — **not** the coefficients.
- **Robust SEs do not repair a wrong model**: if the relationship is curved, or a driver is missing, the coefficients themselves are misleading. Look at the residuals.
- **VIF** (`variance_inflation_factor`): how much a coefficient's variance is inflated by correlation with the other regressors (> 5–10 is a warning).

### Assumptions

Months with a missing regressor or crack are dropped. Regressors: `stocks_vs_5y_pct`, `outages_kbd`, `refinery_utilisation_pct`.

### Your task

Implement `crack_regression(monthly)` returning a dict:

- `coefficients`: frame indexed like the parameters (`const` first) with `coef`, `se`, `p`, `se_hc3`, `p_hc3`;
- `r2`, `n`; `white_lm`, `white_p` (from `het_white(resid, X)`);
- `vif`: dict regressor → VIF;
- `durbin_watson` of the residuals;
- `residuals_by_stocks`: mean, std and count of the residuals for stocks below −15 %, −15 % to −5 %, −5 % to +5 %, above +5 % (`pd.cut` with bins `[-100, -15, -5, 5, 100]` and those labels; `observed=False`).

Plot the residuals in the Test code pad, then the **Explain** tab.
