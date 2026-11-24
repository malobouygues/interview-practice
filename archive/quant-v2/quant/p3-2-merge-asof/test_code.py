import pandas as pd

raw = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
stocks = raw.copy()
stocks["week_ending"] = pd.to_datetime(stocks["week_ending"])
stocks["available_at"] = pd.to_datetime(stocks["release_date"]) + pd.to_timedelta(stocks["release_time_et"] + ":00")
prices = pd.read_csv("data/p3_wti_daily_synthetic.csv")

aligned = align_stocks(prices, stocks)
print(aligned.head(9).to_string())
print("age of the matched report (days):", aligned["age_days"].describe().round(1).to_dict())

# the wrong key, for comparison
naive_prices = prices.assign(date=pd.to_datetime(prices["date"]))
naive_prices["decision_time"] = naive_prices["date"] + pd.Timedelta(hours=14, minutes=30)
naive = pd.merge_asof(naive_prices.sort_values("decision_time"),
                      stocks[["week_ending", "crude_stocks_mbbl"]].sort_values("week_ending"),
                      left_on="decision_time", right_on="week_ending", direction="backward")
unpublished = (naive["crude_stocks_mbbl"] != aligned["crude_stocks_mbbl"]) & naive["crude_stocks_mbbl"].notna()
print("days where the week_ending join uses a report not yet published:", unpublished.sum(), "of", len(naive))
