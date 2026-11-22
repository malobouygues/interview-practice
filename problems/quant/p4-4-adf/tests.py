import numpy as np
import pandas as pd

FUNCTION = "adf_report"


def logs():
    prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    prices = prices.loc["2016-07-01":]
    return np.log(prices["brent"]), np.log(prices["wti"])


def shocks():
    return np.random.default_rng(0).normal(size=500)


def persistent(n, phi, seed):
    e = np.random.default_rng(seed).normal(size=n)
    values = np.zeros(n)
    for t in range(n):
        values[t] = (phi * values[t - 1] if t > 0 else 0.0) + e[t]
    return pd.Series(values)


TESTS = [
    {"name": "log Brent, 'c': cannot reject the unit root", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"x": logs()[0], "regression": "c"}},
    {"name": "Brent daily log returns, 'n': unit root rejected", "origin": "extra",
     "args": lambda: {"x": logs()[0].diff(), "regression": "n"}},
    {"name": "log spread Brent - WTI, 'c': stationary", "origin": "extra",
     "args": lambda: {"x": logs()[0] - logs()[1], "regression": "c"}},
    {"name": "Trend-stationary with 'c' only: looks like a unit root", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks()), "regression": "c"}},
    {"name": "Same series with 'ct': unit root rejected", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks()), "regression": "ct"}},
    {"name": "Stationary, persistent, only 40 obs: low power", "origin": "extra",
     "args": lambda: {"x": persistent(40, 0.8, 0), "regression": "c"}},
    {"name": "Stationary with a level shift: the break fools the test", "origin": "extra",
     "args": lambda: {"x": persistent(600, 0.5, 1) + 2.0 * (np.arange(600) >= 300), "regression": "c"}},
]
