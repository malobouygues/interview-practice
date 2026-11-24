import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv")
demand = pd.read_csv("data/p4_diesel_demand_monthly_synthetic.csv")
table = stationarity_table(prices, demand)
print(table.round(3).to_string())

level = demand.copy()
level["month"] = pd.to_datetime(level["month"])
level = level.set_index("month")["demand_kbd"]

# what do the series look like? (choose n / c / ct from this, not from the p-value)
fig, ax = plt.subplots(2, 2, figsize=(11, 6))
prices_by_date = prices.set_index(pd.to_datetime(prices["date"]))
np.log(prices_by_date["brent"]).plot(ax=ax[0, 0], title="log Brent")
level.plot(ax=ax[0, 1], title="diesel demand (kb/d)")
plot_acf(level.diff().dropna(), lags=24, ax=ax[1, 0], title="ACF: first difference of demand")
plot_acf(level.diff(12).dropna(), lags=24, ax=ax[1, 1], title="ACF: seasonal difference of demand")
plt.tight_layout()

# a seasonal plot: one line per year, months on the x axis
seasonal = level.groupby([level.index.month, level.index.year]).mean().unstack()
fig, ax = plt.subplots(figsize=(8, 3.5))
seasonal.plot(ax=ax, legend=False, title="diesel demand by month, one line per year")
