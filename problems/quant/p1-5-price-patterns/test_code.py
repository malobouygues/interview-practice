import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

hours = pd.read_csv("data/p1_power_hourly_treated_synthetic.csv")
hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
hours["local_date"] = pd.to_datetime(hours["local_date"])
hours = hours.set_index("delivery_start_utc")

patterns = price_patterns(hours)
print(patterns["hourly_profile"].round(1).T.to_string())
print("changes:", {k: round(float(v), 3) for k, v in patterns["change_stats"].items()})
print("load ACF:", {k: round(float(v), 3) for k, v in patterns["acf_load"].items()})
print("load vs solar:", {k: round(float(v), 3) for k, v in patterns["load_solar_correlation"].items()})

# 1. where in the day are prices high? (one box per local hour, extreme points hidden)
fig, ax = plt.subplots(figsize=(10, 3.5))
groups = [hours.loc[hours["local_hour"] == h, "price_eur_mwh"].dropna() for h in range(24)]
ax.boxplot(groups, showfliers=False)
ax.set_xticks(range(1, 25), range(24))
ax.set_title("day-ahead price by local hour")
ax.set_ylabel("EUR/MWh")

# 2. ordinary moves vs extreme moves
fig, ax = plt.subplots(figsize=(10, 3.2))
hours["price_eur_mwh"].diff().clip(-120, 120).hist(bins=120, ax=ax)
ax.set_title("hour-to-hour price changes (clipped at ±120 for display)")

# 3. memory of the load, one week of lags
fig, ax = plt.subplots(figsize=(10, 3.2))
plot_acf(hours["load_mw"], lags=168, ax=ax)

# 4. when was volatility high?
fig, ax = plt.subplots(figsize=(10, 3.2))
patterns["rolling_std_30d"].plot(ax=ax, title="30-day rolling std of the daily average price change")
