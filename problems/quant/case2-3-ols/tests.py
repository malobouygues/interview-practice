import numpy as np
import pandas as pd

FUNCTION = "ols_fit"


def logs():
    crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return np.log(crude["brent"]), np.log(crude["wti"]), np.log(crude["coffee"])


def exact_line():
    x = pd.Series(np.arange(10, dtype=float))
    noise = pd.Series([0.1, -0.1] * 5)
    return {"y": 2.0 + 3.0 * x + noise, "x": x}


TESTS = [
    {"name": "Near-exact line y = 2 + 3x (+/- 0.1)", "origin": "extra",
     "args": exact_line},
    {"name": "WTI on Brent, log levels", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": logs()[1], "x": logs()[0]}},
    {"name": "WTI on Brent, daily log returns (first row NaN)", "origin": "extra",
     "args": lambda: {"y": logs()[1].diff(), "x": logs()[0].diff()}},
    {"name": "Coffee on Brent, log levels ('significant'...?)", "origin": "extra",
     "args": lambda: {"y": logs()[2], "x": logs()[0]}},
    {"name": "Series with a gap are aligned before fitting", "origin": "extra",
     "args": lambda: {"y": pd.Series([1.0, 2.1, np.nan, 3.9, 5.2, 5.8]),
                      "x": pd.Series([0.0, 1.0, 2.0, 3.0, np.nan, 5.0])}},
]
