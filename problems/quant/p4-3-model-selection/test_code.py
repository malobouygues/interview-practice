import numpy as np
import pandas as pd

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices.loc["2016-07-01":]
returns = np.log(prices).diff().dropna()

table = compare_specifications(returns)
print(table.round(4).to_string())
print("correlation of Brent and Dubai returns:", round(returns["brent"].corr(returns["dubai"]), 3))
