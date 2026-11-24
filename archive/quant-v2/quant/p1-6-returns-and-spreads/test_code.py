import numpy as np
import pandas as pd

prices = pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")
table = make_returns(prices["brent"])
print(table.head())

first, last = table["price"].iloc[0], table["price"].iloc[-1]
print("total move, log      :", np.log(last / first))
print("sum of log returns   :", table["log_return"].sum())
print("total move, %        :", last / first - 1)
print("sum of % changes     :", table["pct_change"].sum(), " <- not the total move")

for name, series in [("WTI", prices["wti"]), ("Brent-Dubai spread", prices["brent"] - prices["dubai"])]:
    try:
        make_returns(series)
    except ValueError as error:
        print(name, "->", error)

print(prices["wti"].dropna().diff().loc["2020-04-16":"2020-04-23"])   # what diff() shows around the event
