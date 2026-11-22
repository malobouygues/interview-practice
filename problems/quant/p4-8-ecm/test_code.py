import numpy as np
import pandas as pd

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices.loc["2016-07-01":]
log_brent, log_wti, log_coffee = np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])

print("WTI ~ Brent   :", fit_ecm(log_wti, log_brent))
print("coffee ~ Brent:", fit_ecm(log_coffee, log_brent), " <- not cointegrated: meaningless")

# what a deviation looks like: a WTI-specific shock in August 2017 and its correction
spread = log_brent - log_wti
print(spread.loc["2017-08-24":"2017-09-15"].round(3))
