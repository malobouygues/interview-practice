import pandas as pd

raw = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
print(raw.head(4).to_string())

stocks = add_availability(raw)
print(stocks[["week_ending", "available_at", "ingested_at", "publication_lag_days", "backfilled", "surprise_mbbl"]].head(4).to_string())
print("publication lags (days):", stocks["publication_lag_days"].value_counts().to_dict())
print("backfilled records:", stocks["backfilled"].sum(), "of", len(stocks))
print("UTC hour of the 10:30 New York release:", stocks["available_at"].dt.hour.value_counts().to_dict())
print(stocks[stocks["publication_lag_days"] > 6][["week_ending", "release_date", "available_at"]].to_string())
print("surprise: mean", round(stocks["surprise_mbbl"].mean(), 2), "| std", round(stocks["surprise_mbbl"].std(), 2))
