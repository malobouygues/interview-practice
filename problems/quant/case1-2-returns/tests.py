import numpy as np
import pandas as pd

FUNCTION = "make_returns"


def ttf():
    return pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]


def hand():
    idx = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"])
    return pd.Series([100.0, 110.0, 99.0], index=idx, name="ttf")


def hand_expected():
    s = hand()
    nan = float("nan")
    return pd.DataFrame({"price": [100.0, 110.0, 99.0],
                         "diff": [nan, 10.0, -11.0],
                         "pct_change": [nan, 0.10, -0.10],
                         "log_return": [nan, np.log(1.1), np.log(0.9)]}, index=s.index)


TESTS = [
    {"name": "Hand-checkable: 100 -> 110 -> 99", "origin": "extra", "check_no_mutation": True,
     "note": "+10 % then -10 % is not back to 100: % changes do not add up.",
     "args": lambda: {"prices": hand()}, "expected": hand_expected},
    {"name": "TTF daily prices (index kept, first row NaN)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": ttf()}},
    {"name": "A spread can be negative -> ValueError", "origin": "extra",
     "note": "Use diff() for spreads: log and % change are undefined or explode.",
     "args": lambda: {"prices": pd.Series([1.2, 0.4, -0.3, 0.8])}, "raises": "ValueError"},
    {"name": "A zero print -> ValueError", "origin": "extra",
     "args": lambda: {"prices": pd.Series([20.0, 0.0, 21.0])}, "raises": "ValueError"},
    {"name": "Missing value inside the series is allowed (not <= 0)", "origin": "extra",
     "args": lambda: {"prices": pd.Series([20.0, np.nan, 22.0, 21.0])}},
]
