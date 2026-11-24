import numpy as np
import pandas as pd

stocks = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
stocks["week_ending"] = pd.to_datetime(stocks["week_ending"])
stocks["release_date"] = pd.to_datetime(stocks["release_date"])
stocks["available_at"] = stocks["release_date"] + pd.to_timedelta(stocks["release_time_et"] + ":00")
stocks["ingested_at"] = pd.to_datetime(stocks["ingested_at"])
prices = pd.read_csv("data/p3_wti_daily_synthetic.csv")

for key in ["week_ending", "available_at", "ingested_at"]:
    print(f"{key:12s}", predictive_correlation(prices, stocks, key))

# where does the information really go? the return ON the release day
wti = prices.assign(date=pd.to_datetime(prices["date"])).set_index("date")["wti_usd_bbl"]
daily_return = np.log(wti).diff()
change = stocks.set_index("release_date")["crude_stocks_mbbl"].diff()
release_day = pd.concat([change, daily_return.reindex(change.index)], axis=1).dropna()
print("corr(stock change, WTI return on the release day):", round(release_day.corr().iloc[0, 1], 3))
