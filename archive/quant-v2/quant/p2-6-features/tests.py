import numpy as np
import pandas as pd

FUNCTION = "build_features"


def cracks():
    prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
    return pd.DataFrame({"diesel_crack": prices["ulsd_usd_gal"] * 42 - prices["brent_usd_bbl"],
                         "gasoil_crack": prices["gasoil_usd_t"] / 7.45 - prices["brent_usd_bbl"]})


def reference_on_full_data_until(cut):
    """Features computed on ALL the data, kept up to the cut (built here without look-ahead)."""
    c = cracks()
    change = c["diesel_crack"].diff()
    gasoil_change = c["gasoil_crack"].diff()
    f = pd.DataFrame(index=c.index)
    f["crack_change"] = change
    f["change_lag1"] = change.shift(1)
    f["mean_change_20"] = change.rolling(20).mean().shift(1)
    f["vol_change_20"] = change.rolling(20).std().shift(1)
    f["gap_to_mean_60"] = (c["diesel_crack"] - c["diesel_crack"].rolling(60).mean()).shift(1)
    f["corr_gasoil_60"] = change.rolling(60).corr(gasoil_change).shift(1)
    f["month"] = c.index.month
    f["heating_season"] = c.index.month.isin([11, 12, 1, 2, 3]).astype(int)
    return f.loc[:cut]


TESTS = [
    {"name": "Diesel crack features 2017-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"cracks": cracks()}},
    {"name": "Truncation: data cut at 2018-06-29 gives the same features up to that date", "origin": "extra",
     "note": "A feature that uses the future changes when the future is removed.",
     "args": lambda: {"cracks": cracks().loc[:"2018-06-29"]},
     "expected": lambda: reference_on_full_data_until("2018-06-29")},
]
