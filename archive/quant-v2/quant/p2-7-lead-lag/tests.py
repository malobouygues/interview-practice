import numpy as np
import pandas as pd

FUNCTION = "lead_lag_table"


def returns():
    prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
    usd_bbl = pd.DataFrame({"ulsd": prices["ulsd_usd_gal"] * 42, "gasoil": prices["gasoil_usd_t"] / 7.45,
                            "brent": prices["brent_usd_bbl"]}).dropna()
    return np.log(usd_bbl).diff()


def planted_lead():
    rng = np.random.default_rng(8)
    x = pd.Series(rng.normal(size=300))
    y = 0.8 * x.shift(2) + 0.6 * pd.Series(rng.normal(size=300))
    return {"x": x, "y": y, "max_lag": 3}


TESTS = [
    {"name": "Planted lead: y follows x two days later", "origin": "extra", "args": planted_lead},
    {"name": "ULSD -> gasoil returns", "origin": "extra",
     "args": lambda: {"x": returns()["ulsd"], "y": returns()["gasoil"], "max_lag": 3}},
    {"name": "Brent -> gasoil returns", "origin": "extra",
     "args": lambda: {"x": returns()["brent"], "y": returns()["gasoil"], "max_lag": 2}},
]
