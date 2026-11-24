import numpy as np
import pandas as pd

FUNCTION = "ols_fit"


def logs():
    prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    prices = prices.loc["2016-07-01":]
    return np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])


def near_line():
    x = pd.Series(np.arange(10, dtype=float))
    return {"y": 2.0 + 3.0 * x + pd.Series([0.1, -0.1] * 5), "x": x}


TESTS = [
    {"name": "Near-exact line y = 2 + 3x", "origin": "extra", "args": near_line},
    {"name": "WTI on Brent, daily log returns", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": logs()[1].diff(), "x": logs()[0].diff()}},
    {"name": "WTI on Brent, log levels (inference invalid)", "origin": "extra",
     "args": lambda: {"y": logs()[1], "x": logs()[0]}},
    {"name": "Coffee on Brent, returns", "origin": "extra",
     "args": lambda: {"y": logs()[2].diff(), "x": logs()[0].diff()}},
    {"name": "Series with gaps are aligned before fitting", "origin": "extra",
     "args": lambda: {"y": pd.Series([1.0, 2.1, np.nan, 3.9, 5.2, 5.8]),
                      "x": pd.Series([0.0, 1.0, 2.0, 3.0, np.nan, 5.0])}},
]
