import pandas as pd

demand = pd.read_csv("data/p4_diesel_demand_monthly_synthetic.csv", parse_dates=["month"], index_col="month")["demand_kbd"]
prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
brent_monthly = prices["brent"].resample("MS").mean()      # a price: monthly MEAN, never a sum

for name, series in [("diesel demand (kb/d)", demand), ("Brent monthly average (USD/bbl)", brent_monthly)]:
    result = trend_or_random_walk(series)
    print(name)
    for key, value in result.items():
        print(f"    {key:20s} {value}")
