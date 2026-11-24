import pandas as pd

path = "data/p1_power_hourly_vendor_synthetic.csv"
raw = pd.read_csv(path)

# 1. look before you clean
print(raw.head(3).to_string())
raw.info()
print(raw.describe().round(1).to_string())

# 2. how many rows look duplicated, depending on the key you choose?
print("exact copies:", raw.duplicated().sum())
print("same local time + offset:", raw.duplicated(subset=["delivery_start_local", "utc_offset"]).sum())
print("same local time only:", raw.duplicated(subset=["delivery_start_local"]).sum())
print(raw[raw["delivery_start_local"].str.startswith("2023-10-29 0")].iloc[:6, :4].to_string())

hours = load_market_hours(path)
print(len(hours), "delivery hours")
print("hours per local day:", hours.groupby("local_date").size().value_counts().to_dict())
print(hours.loc["2023-11-21 17:00":"2023-11-21 17:00"].to_string())
