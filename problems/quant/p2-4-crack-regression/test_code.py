import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

monthly = pd.read_csv("data/p2_monthly_table_synthetic.csv")
result = crack_regression(monthly)
print(result["coefficients"].round(4).to_string())
print("R2", round(result["r2"], 3), "| n", result["n"], "| White LM", round(result["white_lm"], 1),
      "p", round(result["white_p"], 4), "| DW", round(result["durbin_watson"], 2))
print("VIF", {k: round(v, 2) for k, v in result["vif"].items()})
print(result["residuals_by_stocks"].round(2).to_string())

# residuals against the stock deficit: a funnel (variance) and a curve (shape)
sample = monthly.dropna(subset=["gasoil_crack", "stocks_vs_5y_pct", "outages_kbd", "refinery_utilisation_pct"])
X = sm.add_constant(sample[["stocks_vs_5y_pct", "outages_kbd", "refinery_utilisation_pct"]])
fit = sm.OLS(sample["gasoil_crack"], X).fit()
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].scatter(sample["stocks_vs_5y_pct"], sample["gasoil_crack"], s=12)
ax[0].set_xlabel("stocks vs 5-year average (%)")
ax[0].set_ylabel("gasoil crack (USD/bbl)")
ax[1].scatter(sample["stocks_vs_5y_pct"], fit.resid, s=12)
ax[1].axhline(0, color="grey")
ax[1].set_xlabel("stocks vs 5-year average (%)")
ax[1].set_ylabel("residual (USD/bbl)")
plt.tight_layout()
