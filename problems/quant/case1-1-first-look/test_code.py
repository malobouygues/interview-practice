import numpy as np
import pandas as pd

prices = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")
ttf = prices["ttf"]
print(prices.info())            # what is a row? which dtype? any missing value?
print(ttf.head(), ttf.tail(), sep="\n")

log_returns = np.log(ttf).diff()  # first value is NaN (no previous price)

print("price level :", summary_stats(ttf))
print("log returns :", summary_stats(log_returns))
