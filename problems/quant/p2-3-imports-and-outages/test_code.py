import pandas as pd
import matplotlib.pyplot as plt

imports = pd.read_csv("data/p2_diesel_imports_monthly_synthetic.csv")
outages = pd.read_csv("data/p2_refinery_outages_synthetic.csv")
fundamentals = pd.read_csv("data/p2_distillate_fundamentals_monthly_synthetic.csv")
daily = pd.read_csv("data/p2_products_repaired_synthetic.csv", index_col="date", parse_dates=["date"])

# what the aggregator's zeros would say if taken literally
naive_total = imports.groupby("month")["volume_kbd"].sum()
print(naive_total.loc["2018-06":"2018-10"].round(0).to_dict())

table = monthly_table(imports, outages, fundamentals, daily)
print(table.round(1).loc["2018-06":"2018-10"].to_string())
print(table.round(1).tail(6).to_string())

fig, ax = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
table["gasoil_crack"].plot(ax=ax[0], title="gasoil crack, monthly average (USD/bbl)")
table["stocks_vs_5y_pct"].plot(ax=ax[1], title="distillate stocks vs 5-year average (%)")
ax[1].axhline(0, color="grey", linewidth=0.8)
table["imports_kbd"].plot(ax=ax[2], label="Europe total")
table["imports_from_russia_kbd"].plot(ax=ax[2], label="from Russia")
ax[2].legend()
ax[2].set_title("diesel imports (kb/d)")
plt.tight_layout()
