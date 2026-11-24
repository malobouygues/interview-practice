import numpy as np
import pandas as pd

FUNCTION = "compare_specifications"


def returns(start="2016-07-01", end=None):
    prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return np.log(prices.loc[start:end]).diff().dropna()


TESTS = [
    {"name": "Exports-allowed regime (from 2016-07)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"returns": returns()}},
    {"name": "Export-ban regime (2012-2015)", "origin": "extra",
     "args": lambda: {"returns": returns("2012-01-01", "2015-12-31")}},
]
