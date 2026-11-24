import numpy as np
import pandas as pd

FUNCTION = "relationship_by_period"


def hand_made():
    rng = np.random.default_rng(30)
    dates = pd.bdate_range("2018-01-01", periods=800)
    brent = np.log(70) + np.cumsum(rng.normal(0, 0.016, 800))
    wti = np.zeros(800)
    wti[0] = brent[0] - 0.12
    for t in range(1, 800):
        discount, gamma, alpha = (0.12, 0.6, -0.05) if t < 400 else (0.04, 0.9, -0.12)
        wti[t] = wti[t - 1] + gamma * (brent[t] - brent[t - 1]) + alpha * (wti[t - 1] - brent[t - 1] + discount) + rng.normal(0, 0.007)
    prices = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "brent": np.exp(brent), "wti": np.exp(wti)})
    return {"prices": prices, "break_date": dates[400].strftime("%Y-%m-%d")}


TESTS = [
    {"name": "Hand-made: a known break in the discount, the pass-through and the speed of adjustment",
     "origin": "extra", "args": hand_made},
    {"name": "Brent and WTI 2012-2019, break at the end of the export ban", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p4_crude_research_daily_synthetic.csv"), "break_date": "2016-01-01"}},
]
