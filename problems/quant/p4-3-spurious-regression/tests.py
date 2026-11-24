import numpy as np
import pandas as pd

FUNCTION = "spurious_check"


def hand_made():
    rng = np.random.default_rng(8)
    dates = pd.bdate_range("2015-01-01", periods=700)
    brent = 4.0 + np.cumsum(rng.normal(0, 0.015, 700))
    wti = brent - 0.08 + 0.3 * np.convolve(rng.normal(0, 0.01, 700), np.ones(5) / 5, mode="same")
    coffee = 4.8 + np.cumsum(rng.normal(0.0004, 0.016, 700))
    prices = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "brent": np.exp(brent), "wti": np.exp(wti),
                           "dubai": np.exp(brent), "coffee": np.exp(coffee)})
    return {"prices": prices}


TESTS = [
    {"name": "Hand-made: a cointegrated pair and an independent random walk", "origin": "extra", "args": hand_made},
    {"name": "WTI, Brent and coffee 2012-2019", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p4_crude_research_daily_synthetic.csv")}},
]
