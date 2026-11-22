import numpy as np
import pandas as pd

FUNCTION = "engle_granger"


def logs():
    prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    prices = prices.loc["2016-07-01":]
    return np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])


TESTS = [
    {"name": "WTI ~ Brent -> cointegrated", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": logs()[1], "x": logs()[0]}},
    {"name": "Coffee ~ Brent: naive p < 0.05 but EG p = 0.50 -> NOT cointegrated", "origin": "extra",
     "args": lambda: {"y": logs()[2], "x": logs()[0]}},
    {"name": "Brent ~ coffee: the ordering changes the statistic", "origin": "extra",
     "args": lambda: {"y": logs()[0], "x": logs()[2]}},
    {"name": "Brent ~ WTI (other normalisation) -> cointegrated", "origin": "extra",
     "args": lambda: {"y": logs()[0], "x": logs()[1]}},
]
