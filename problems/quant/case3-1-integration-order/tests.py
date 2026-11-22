import numpy as np
import pandas as pd

FUNCTION = "integration_order"


def logs():
    crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return np.log(crude["brent"]), np.log(crude["wti"])


TESTS = [
    {"name": "log Brent -> I(1)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"x": logs()[0]}},
    {"name": "log WTI -> I(1)", "origin": "extra",
     "args": lambda: {"x": logs()[1]}},
    {"name": "log spread (Brent - WTI) -> I(0)", "origin": "extra",
     "args": lambda: {"x": logs()[0] - logs()[1]}},
    {"name": "Brent log returns -> I(0)", "origin": "extra",
     "args": lambda: {"x": logs()[0].diff()}},
    {"name": "Twice-accumulated noise -> I(2)", "origin": "extra",
     "args": lambda: {"x": pd.Series(np.random.default_rng(4).normal(size=600).cumsum().cumsum())}},
    {"name": "log TTF (Case 1) -> I(1)", "origin": "extra",
     "args": lambda: {"x": np.log(pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"],
                                              index_col="date")["ttf"])}},
    {"name": "max_order=0 on log Brent -> None", "origin": "extra",
     "args": lambda: {"x": logs()[0], "max_order": 0}},
]
