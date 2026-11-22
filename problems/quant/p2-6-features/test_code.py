import pandas as pd

prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
cracks = pd.DataFrame({"diesel_crack": prices["ulsd_usd_gal"] * 42 - prices["brent_usd_bbl"],
                       "gasoil_crack": prices["gasoil_usd_t"] / 7.45 - prices["brent_usd_bbl"]})

features = build_features(cracks)
print(features.loc["2018-03-01":"2018-03-08"].round(3))

# screening: does each feature relate to the target, and is the relation stable?
first, second = features.loc[:"2018-12-31"], features.loc["2019-01-01":]
for name in ["change_lag1", "mean_change_20", "vol_change_20", "gap_to_mean_60", "corr_gasoil_60", "heating_season"]:
    print(f"{name:16s} corr 2017-18: {first[name].corr(first['crack_change']):6.3f}   "
          f"2019: {second[name].corr(second['crack_change']):6.3f}")

# a quick look-ahead check: rebuild on data cut at a past date
cut = "2018-06-29"
truncated = build_features(cracks.loc[:cut])
print("same features up to the cut:", truncated.equals(features.loc[:cut]))
