import numpy as np
import pandas as pd

FUNCTION = "summary_stats"


def prices():
    return pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")


def hand():
    return pd.Series([1.0, 2.0, 3.0, 4.0, 100.0])


TESTS = [
    {"name": "Hand-checkable: one extreme value moves the mean, not the median", "origin": "extra",
     "args": lambda: {"x": hand()},
     "expected": lambda: {"n": 5, "mean": 22.0, "median": 3.0, "std": 1902.5 ** 0.5, "var": 1902.5,
                          "q05": 1.2, "q95": 80.8, "skew": float(hand().skew()),
                          "excess_kurtosis": float(hand().kurt())}},
    {"name": "Missing values are ignored", "origin": "extra",
     "args": lambda: {"x": pd.Series([2.0, np.nan, 4.0, 6.0, np.nan, 8.0])}},
    {"name": "Brent level (holidays are NaN)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"x": prices()["brent"]}},
    {"name": "Brent daily log returns", "origin": "extra",
     "args": lambda: {"x": np.log(prices()["brent"].dropna()).diff()}},
    {"name": "Brent-WTI spread (one extreme day)", "origin": "extra",
     "args": lambda: {"x": prices()["brent"] - prices()["wti"]}},
]
