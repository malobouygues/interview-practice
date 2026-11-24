import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv")
print(prices.describe().round(1).to_string())
result = levels_and_returns(prices)
for key in ["level_corr", "return_corr", "brent_distribution"]:
    print(key, {k: round(float(v), 5) for k, v in result[key].items()})
print("yearly volatility:", result["yearly_vol"].round(3).to_dict())
print("Brent - WTI by year:", result["spread_by_year"].round(2).to_dict())

table = prices.copy()
table["date"] = pd.to_datetime(table["date"])
table = table.set_index("date")
fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
table[["brent", "wti"]].plot(ax=ax[0], title="levels (USD/bbl)")
(table["coffee"]).plot(ax=ax[0], secondary_y=True, color="tab:brown", alpha=0.6)
np.log(table["brent"]).diff().plot(ax=ax[1], linewidth=0.5, title="Brent daily log returns")
result["rolling_vol_60d"].plot(ax=ax[2], title="Brent 60-day volatility, annualised")
plt.tight_layout()

fig, ax = plt.subplots(figsize=(8, 3.2))
np.log(table["brent"]).diff().hist(bins=100, ax=ax)
ax.set_title("histogram of Brent daily log returns")
