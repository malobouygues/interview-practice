import pandas as pd

raw = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
print(raw.dtypes)

stocks = add_availability(raw)
print(stocks.head(4).to_string())
print("publication lag (days):", stocks["publication_lag_days"].value_counts().to_dict())
print("backfilled rows:", stocks["backfilled"].sum(), "of", len(stocks))
print(stocks[stocks["publication_lag_days"] == 6].head(3).to_string())
