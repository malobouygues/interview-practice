import numpy as np
import pandas as pd

FUNCTION = "treat_gaps"


def raw():
    return pd.read_csv("data/p2_products_daily_synthetic.csv", parse_dates=["date"], index_col="date")


def hand():
    index = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08",
                            "2020-01-09", "2020-01-10", "2020-01-13", "2020-01-13", "2020-01-14"])
    nan = np.nan
    return pd.DataFrame({"a": [nan, 10.0, nan, nan, nan, 11.0, 11.0, 11.0, 11.0, 11.0, 12.0],
                         "b": [5.0, 5.1, 5.2, 5.2, nan, 5.3, 5.4, 5.5, 5.6, 5.6, 5.7]}, index=index)


def hand_expected():
    index = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08",
                            "2020-01-09", "2020-01-10", "2020-01-13", "2020-01-14"])
    nan = np.nan
    prices = pd.DataFrame({"a": [nan, 10.0, 10.0, 10.0, nan, 11.0, 11.0, 11.0, nan, 12.0],
                           "b": [5.0, 5.1, 5.2, 5.2, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7]}, index=index)
    filled = pd.DataFrame({"a": [False, False, True, True, False, False, True, True, False, False],
                           "b": [False, False, False, False, True, False, False, False, False, False]}, index=index)
    return {"prices": prices, "filled": filled}


TESTS = [
    {"name": "Hand-made: a leading NaN, a 3-day gap, a stale run of 4, a duplicated date", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"products": hand()}, "expected": hand_expected},
    {"name": "Products 2017-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"products": raw()}},
]
