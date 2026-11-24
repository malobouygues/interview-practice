import pandas as pd
import matplotlib.pyplot as plt

temps = pd.read_csv("data/p1_zone_temperature_obs_synthetic.csv")
load = pd.read_csv("data/p1_zone_load_hourly_synthetic.csv")
zones = pd.read_csv("data/p1_zones_reference_synthetic.csv")
print(zones.to_string())
print("readings by minute of the hour:", pd.to_datetime(temps["observed_at_utc"]).dt.minute.value_counts().to_dict())

daily = daily_zone_table(temps, load, zones)
print(daily[daily["local_date"].isin(pd.to_datetime(["2023-03-26", "2023-10-29"]))].to_string(float_format="%.1f"))
print("blank days:", daily[daily["temp_mean_c"].isna() | daily["load_avg_mw"].isna()][["zone", "local_date"]].to_string())

# does load follow temperature in a straight line? (one chart per zone)
fig, ax = plt.subplots(1, 3, figsize=(12, 3.6), sharey=False)
for i, zone in enumerate(["NORTH", "CENTRAL", "SOUTH"]):
    part = daily[daily["zone"] == zone]
    ax[i].scatter(part["temp_mean_c"], part["load_avg_mw"], s=4)
    ax[i].set_title(zone)
    ax[i].set_xlabel("daily mean temperature (°C)")
ax[0].set_ylabel("average load (MW)")
plt.tight_layout()
for zone in ["NORTH", "CENTRAL", "SOUTH"]:
    part = daily[daily["zone"] == zone].dropna()
    print(zone, "corr with temperature", round(part["load_avg_mw"].corr(part["temp_mean_c"]), 3),
          "| with HDD", round(part["load_avg_mw"].corr(part["hdd"]), 3),
          "| with CDD", round(part["load_avg_mw"].corr(part["cdd"]), 3))
