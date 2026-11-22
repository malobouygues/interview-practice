import numpy as np
import pandas as pd

FUNCTION = "levels_vs_differences"


def logs():
    crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return np.log(crude["brent"]), np.log(crude["wti"]), np.log(crude["coffee"])


TESTS = [
    {"name": "WTI ~ Brent -> co-moving", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": logs()[1], "x": logs()[0]}},
    {"name": "Coffee ~ Brent -> spurious", "origin": "extra",
     "args": lambda: {"y": logs()[2], "x": logs()[0]}},
    {"name": "Two independent random walks -> spurious", "origin": "extra",
     "args": lambda: {"y": pd.Series(np.random.default_rng(21).normal(size=900).cumsum()),
                      "x": pd.Series(np.random.default_rng(20).normal(size=900).cumsum())}},
    {"name": "Two independent white noises -> unrelated", "origin": "extra",
     "args": lambda: {"y": pd.Series(np.random.default_rng(6).normal(size=900)),
                      "x": pd.Series(np.random.default_rng(5).normal(size=900))}},
]
