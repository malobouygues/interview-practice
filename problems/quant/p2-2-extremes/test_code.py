import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prices = pd.read_csv("data/p2_products_wide_synthetic.csv", index_col="date", parse_dates=["date"])
events = pd.read_csv("data/p2_market_events_synthetic.csv")
print(events.to_string())

# masking: the z-score of the hurricane day BEFORE the unit error is fixed
rbob = np.log(prices["rbob"].dropna()).diff().dropna()
z_before = (rbob - rbob.mean()) / rbob.std()
print("RBOB return std before the fix:", round(rbob.std(), 4), "| hurricane-day z:", round(z_before["2017-08-28"], 2))

result = investigate_extremes(prices, events)
decisions = result["decisions"]
print(decisions.to_string(float_format="%.3f"))
print(decisions["decision"].value_counts().to_dict())
print(result["flag_counts"].to_string())

# sensitivity of the doubtful point
repaired = result["prices"]
jet_crack = repaired["jet"] - repaired["brent"]
june = jet_crack.loc["2021-06"]
print("June 2021 jet crack, with / without 15 June:", round(june.mean(), 2), "/", round(june.drop(pd.Timestamp("2021-06-15")).mean(), 2))

# the distribution of daily gasoil-crack changes, by year (are 2022 moves 'outliers' or a regime?)
change = (repaired["gasoil"] - repaired["brent"]).diff()
fig, ax = plt.subplots(figsize=(9, 3.6))
years = sorted(change.index.year.unique())
ax.boxplot([change[change.index.year == y].dropna() for y in years], showfliers=True)
ax.set_xticks(range(1, len(years) + 1), years)
ax.set_title("daily change of the gasoil crack (USD/bbl), by year")

fig, ax = plt.subplots(figsize=(9, 3.2))
np.log(repaired["ulsd"].dropna()).diff().hist(bins=150, ax=ax)
ax.set_title("ULSD daily log returns after repair: fat tails, and the squeeze on the right")
