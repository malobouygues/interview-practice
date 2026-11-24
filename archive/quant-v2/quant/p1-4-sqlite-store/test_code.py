import pandas as pd

prices = pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")
monthly = monthly_spreads_sql(prices)
print(monthly.to_string(index=False))

# cross-check with pandas: same numbers?
complete = prices.dropna()
spread = complete["brent"] - complete["wti"]
print(spread.groupby(complete.index.strftime("%Y-%m")).mean().head())
