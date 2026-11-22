import numpy as np
import pandas as pd

FUNCTION = "fit_ecm"


def logs():
    prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    prices = prices.loc["2016-07-01":]
    return np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])


def known_ecm():
    """Simulated pair with alpha = -0.3, gamma = 0.5, beta = 1: the estimates should be close."""
    rng = np.random.default_rng(11)
    n = 2000
    x = np.cumsum(rng.normal(0, 1, n))
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = y[t - 1] + 0.5 * (x[t] - x[t - 1]) - 0.3 * (y[t - 1] - x[t - 1]) + rng.normal(0, 0.5)
    return {"y": pd.Series(y), "x": pd.Series(x)}


TESTS = [
    {"name": "WTI ~ Brent: alpha < 0, half-life of a few days", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": logs()[1], "x": logs()[0]}},
    {"name": "Simulated ECM with known alpha = -0.3, gamma = 0.5", "origin": "extra", "args": known_ecm},
    {"name": "Coffee ~ Brent (not cointegrated): alpha ~ 0, meaningless", "origin": "extra",
     "args": lambda: {"y": logs()[2], "x": logs()[0]}},
]
