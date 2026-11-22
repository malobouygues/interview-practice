import numpy as np
import pandas as pd

# the output of step 1.2 (re-done here in a few lines so this pad runs on its own)
raw = pd.read_csv("data/p1_crude_prices_vendor_synthetic.csv", na_values=["HOL", "-"])
raw.columns = ["date", "brent", "wti", "dubai", "loaded_at"]
raw["date"] = pd.to_datetime(raw["date"], format="%d/%m/%Y")
raw["loaded_at"] = pd.to_datetime(raw["loaded_at"])
prices = raw.drop_duplicates().sort_values(["date", "loaded_at"])
prices = prices.drop_duplicates(subset="date", keep="last").set_index("date")[["brent", "wti", "dubai"]]

flags = quality_checks(prices)
print(flags)

for date in flags["date"]:
    window = prices.loc[date - pd.Timedelta(days=4): date + pd.Timedelta(days=4)]
    print(window, "\n")

# apply the decisions: errors -> NaN, documented events stay
clean = prices.copy()
for _, flag in flags.iterrows():
    if flag["action"] == "set to NaN":
        clean.loc[flag["date"], flag["series"]] = np.nan
provided = pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")
print("same as the provided clean file:", clean.equals(provided))
