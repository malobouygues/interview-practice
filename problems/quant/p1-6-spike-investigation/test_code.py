import pandas as pd
import matplotlib.pyplot as plt

hours = pd.read_csv("data/p1_power_hourly_treated_synthetic.csv")
hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
hours["local_date"] = pd.to_datetime(hours["local_date"])
hours = hours.set_index("delivery_start_utc")
daily = pd.read_csv("data/p1_zone_daily_synthetic.csv")

result = explain_spikes(hours, daily)
spikes = result["spike_days"]
print(spikes[["max_price", "min_margin_mw", "wind_mean_mw", "hdd", "capacity_ratio", "gas_eur_mwh", "driver"]].round(2).to_string())
print(spikes["driver"].value_counts().to_dict())
print("Spearman with the daily max price:", result["rank_correlations"].round(3).to_dict())

# timeline of the daily maximum price, spike days annotated by driver
days = hours.groupby("local_date")["price_eur_mwh"].max()
fig, ax = plt.subplots(figsize=(11, 3.8))
ax.plot(days.index, days.values, color="grey", linewidth=0.8)
ax.set_yscale("log")
for driver, colour in [("cold and still", "tab:blue"), ("low available capacity", "tab:red"), ("unexplained", "black")]:
    part = spikes[spikes["driver"] == driver]
    ax.scatter(part.index, part["max_price"], color=colour, label=driver, zorder=3)
ax.set_title("daily maximum price (log scale) and spike days")
ax.legend()

# does the margin explain the spikes better than the cold?
hours["margin_mw"] = hours["available_capacity_mw"] - (hours["load_mw"] - hours["wind_mw"] - hours["solar_mw"])
by_day = hours.groupby("local_date").agg(max_price=("price_eur_mwh", "max"), min_margin=("margin_mw", "min"))
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(by_day["min_margin"], by_day["max_price"], s=5)
ax.set_yscale("log")
ax.set_xlabel("smallest hourly margin of the day (MW)")
ax.set_ylabel("daily max price (EUR/MWh)")
