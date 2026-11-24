import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv")
print(spurious_check(prices).round(4).to_string())

logs = np.log(prices.set_index(pd.to_datetime(prices["date"]))[["brent", "wti", "coffee"]])
coffee_fit = sm.OLS(logs["wti"], sm.add_constant(logs["coffee"])).fit()
brent_fit = sm.OLS(logs["wti"], sm.add_constant(logs["brent"])).fit()

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
logs[["wti", "coffee"]].plot(ax=ax[0], title="log WTI and log coffee: two trends")
coffee_fit.resid.plot(ax=ax[1], label="residual, WTI on coffee")
brent_fit.resid.plot(ax=ax[1], label="residual, WTI on Brent")
ax[1].axhline(0, color="grey")
ax[1].legend()
plt.tight_layout()

fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(logs["coffee"].diff(), logs["wti"].diff(), s=3)
ax.set_xlabel("daily change, log coffee")
ax.set_ylabel("daily change, log WTI")
