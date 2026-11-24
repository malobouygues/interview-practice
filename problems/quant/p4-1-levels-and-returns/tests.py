import numpy as np
import pandas as pd

FUNCTION = "levels_and_returns"


def hand_made():
    rng = np.random.default_rng(2)
    dates = pd.bdate_range("2015-01-01", periods=400)
    vol = np.where(np.arange(400) < 200, 0.01, 0.03)
    brent = 60 * np.exp(np.cumsum(rng.normal(0.001, 1, 400) * vol))
    wti = brent * np.exp(rng.normal(-0.05, 0.005, 400))
    coffee = 120 * np.exp(np.cumsum(rng.normal(0.001, 0.015, 400)))
    prices = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "brent": brent, "wti": wti, "dubai": brent - 1, "coffee": coffee})
    return {"prices": prices}


TESTS = [
    {"name": "Hand-made: a volatility regime change and two unrelated trends", "origin": "extra", "args": hand_made},
    {"name": "Brent, WTI, coffee 2012-2019", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p4_crude_research_daily_synthetic.csv")}},
]
