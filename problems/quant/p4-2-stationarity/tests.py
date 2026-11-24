import numpy as np
import pandas as pd

FUNCTION = "stationarity_table"


def hand_made():
    rng = np.random.default_rng(12)
    dates = pd.bdate_range("2016-01-01", periods=600)
    brent = 50 * np.exp(np.cumsum(rng.normal(0, 0.015, 600)))
    prices = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "brent": brent, "wti": brent * 0.95})
    months = pd.date_range("2012-01-01", periods=96, freq="MS")
    season = np.array([30, 25, 10, 0, -10, -20, -25, -25, -15, 0, 10, 20], dtype=float)
    demand = 1000 + 0.8 * np.arange(96) + season[months.month - 1] + rng.normal(0, 8, 96)
    return {"prices": prices, "demand": pd.DataFrame({"month": months.strftime("%Y-%m"), "demand_kbd": demand})}


TESTS = [
    {"name": "Hand-made: a random walk and a trend-plus-season demand series", "origin": "extra", "args": hand_made},
    {"name": "Brent 2012-2019 and diesel demand 2010-2019", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p4_crude_research_daily_synthetic.csv"),
                      "demand": pd.read_csv("data/p4_diesel_demand_monthly_synthetic.csv")}},
]
