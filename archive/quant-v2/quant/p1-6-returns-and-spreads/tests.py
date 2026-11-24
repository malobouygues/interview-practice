import numpy as np
import pandas as pd

FUNCTION = "make_returns"


def prices():
    return pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")


def hand():
    index = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"])
    return pd.Series([100.0, 110.0, np.nan, 99.0], index=index)


def hand_expected():
    index = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-05"])
    nan = float("nan")
    return pd.DataFrame({"price": [100.0, 110.0, 99.0],
                         "diff": [nan, 10.0, -11.0],
                         "pct_change": [nan, 0.10, -0.10],
                         "log_return": [nan, np.log(1.1), np.log(0.9)]}, index=index)


TESTS = [
    {"name": "Hand-checkable: 100 -> 110 -> (holiday) -> 99", "origin": "extra", "check_no_mutation": True,
     "note": "+10 % then -10 % is not back to 100; the holiday is skipped, not a zero return.",
     "args": lambda: {"prices": hand()}, "expected": hand_expected},
    {"name": "Brent (holidays dropped, log returns add up)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": prices()["brent"]}},
    {"name": "WTI went negative -> ValueError", "origin": "extra",
     "args": lambda: {"prices": prices()["wti"]}, "raises": "ValueError"},
    {"name": "Brent-Dubai spread crosses zero -> ValueError", "origin": "extra",
     "args": lambda: {"prices": prices()["brent"] - prices()["dubai"]}, "raises": "ValueError"},
]
