import numpy as np
import pandas as pd

FUNCTION = "chow_test"


def logs():
    h = pd.read_csv("data/crude_history_synthetic.csv", parse_dates=["date"], index_col="date")
    return np.log(h["brent"]), np.log(h["wti"])


def returns_window(start=None, end=None):
    b, w = logs()
    return w.diff().loc[start:end], b.diff().loc[start:end]


TESTS = [
    {"name": "Log returns, break 2016-01-01 -> reject", "origin": "extra", "check_no_mutation": True,
     "args": lambda: dict(zip(("y", "x"), returns_window()), break_date="2016-01-01")},
    {"name": "Placebo 2018-01-01 within the post regime -> no change", "origin": "extra",
     "args": lambda: dict(zip(("y", "x"), returns_window("2016-07-01")), break_date="2018-01-01")},
    {"name": "Placebo 2014-01-01 within the pre regime -> no change", "origin": "extra",
     "args": lambda: dict(zip(("y", "x"), returns_window(None, "2015-12-31")), break_date="2014-01-01")},
    {"name": "Pitfall: same placebo on LOG LEVELS -> spurious rejection", "origin": "extra",
     "note": "I(1) levels, persistent residuals: the F distribution does not apply.",
     "args": lambda: {"y": logs()[1].loc["2016-07-01":], "x": logs()[0].loc["2016-07-01":],
                      "break_date": "2018-01-01"}},
    {"name": "Hand-made: slope 1 then slope 2, no noise elsewhere", "origin": "extra",
     "args": lambda: {"y": pd.Series([0.0, 1.1, 1.9, 3.0, 8.1, 9.9, 12.0, 14.1],
                                     index=pd.date_range("2020-01-01", periods=8, freq="D")),
                      "x": pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                                     index=pd.date_range("2020-01-01", periods=8, freq="D")),
                      "break_date": "2020-01-05"}},
]
