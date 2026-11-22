import numpy as np
import pandas as pd

demand = pd.read_csv("data/diesel_demand_monthly_synthetic.csv",
                     parse_dates=["month"], index_col="month")["demand_kbd"]
print(demand.head(13))

ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
ttf_monthly = ttf.resample("MS").mean()          # monthly average price (a price: mean, never sum)

for name, series in [("diesel demand", demand), ("TTF monthly average", ttf_monthly)]:
    print(name, trend_or_random_walk(series))
