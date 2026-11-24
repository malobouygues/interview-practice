import pandas as pd
import matplotlib.pyplot as plt

hours = pd.read_csv("data/p1_power_hourly_clean_synthetic.csv")
hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
hours["local_date"] = pd.to_datetime(hours["local_date"])
hours = hours.set_index("delivery_start_utc")

# where are the blanks? (position and regularity tell you the cause)
print("blanks per column:", hours.isna().sum().to_dict())
solar_blank_by_hour = hours["solar_mw"].isna().groupby(hours.index.hour).mean().round(2)
print("share of solar blanks by UTC hour:", solar_blank_by_hour.to_dict())

treated = treat_gaps(hours)
print("solar failures:", treated["solar_missing"].sum(), "| wind failures:", treated["wind_missing"].sum())
print("capacity still blank:", treated["available_capacity_mw"].isna().sum(),
      "| stale hours:", treated["capacity_is_stale"].sum(), "| max age:", treated["capacity_age_h"].max())

# the September 2024 publication outage: how far is the last value carried?
window = treated.loc["2024-08-31":"2024-09-08"]
fig, ax = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
window["available_capacity_mw"].plot(ax=ax[0], title="capacity after ffill(limit=48)")
window["capacity_age_h"].plot(ax=ax[1], title="age of the capacity value (hours)")
ax[1].axhline(24, color="red", linestyle="--")
plt.tight_layout()
