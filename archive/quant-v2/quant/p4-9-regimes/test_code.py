import numpy as np
import pandas as pd

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices[["brent", "wti"]]

result = regime_comparison(prices, "2016-01-01")
for period in ("pre", "post"):
    print(period, {key: round(value, 4) for key, value in result[period].items()})
print("full-sample Engle-Granger p-value:", round(result["full_eg_pvalue"], 3))

spread = np.log(prices["brent"]) - np.log(prices["wti"])
print(spread.resample("YE").mean().round(3))                     # yearly average WTI discount

for start, end, placebo in [(None, "2015-12-31", "2014-01-01"), ("2016-07-01", None, "2018-01-01")]:
    placebo_result = regime_comparison(prices.loc[start:end], placebo)
    print("placebo", placebo, {p: round(placebo_result[p]["mean_spread"], 3) for p in ("pre", "post")})
