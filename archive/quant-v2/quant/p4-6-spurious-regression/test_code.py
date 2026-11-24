import numpy as np
import pandas as pd
import statsmodels.api as sm

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices.loc["2016-07-01":]
log_brent, log_wti, log_coffee = np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])

print("WTI    ~ Brent:", levels_vs_differences(log_wti, log_brent))
print("coffee ~ Brent:", levels_vs_differences(log_coffee, log_brent))

# Monte Carlo: 200 pairs of INDEPENDENT random walks, 500 steps each
significant = 0
for seed in range(200):
    rng = np.random.default_rng(10_000 + seed)
    x = rng.normal(size=500).cumsum()
    y = rng.normal(size=500).cumsum()
    t = sm.OLS(y, sm.add_constant(x)).fit().tvalues[1]
    if abs(t) > 1.96:
        significant += 1
print(f"independent random walks with |t| > 1.96 in levels: {significant / 200:.0%} (a valid 5 % test: 5 %)")
