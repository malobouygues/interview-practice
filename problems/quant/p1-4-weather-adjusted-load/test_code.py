import pandas as pd
import matplotlib.pyplot as plt

daily = pd.read_csv("data/p1_zone_daily_synthetic.csv")
normals = pd.read_csv("data/p1_weather_normals_synthetic.csv")
print(normals[normals["month"].isin([1, 7])].to_string())

result = weather_adjusted_load(daily, normals)
print(result["coefficients"].round(2).to_string())
print(result["winter_comparison"].round(1).to_string())

# actual vs weather-adjusted load, CENTRAL zone, 30-day averages
central = result["daily"][result["daily"]["zone"] == "CENTRAL"].set_index("local_date")
fig, ax = plt.subplots(figsize=(10, 4))
central["load_avg_mw"].rolling(30).mean().plot(ax=ax, label="actual load")
central["load_adjusted_mw"].rolling(30).mean().plot(ax=ax, label="weather-adjusted load")
ax.set_title("CENTRAL: 30-day average load, actual vs normal weather")
ax.set_ylabel("MW")
ax.legend()
