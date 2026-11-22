import numpy as np
import pandas as pd

FUNCTION = "correlation_report"


def crude():
    return pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")


TESTS = [
    {"name": "Brent / WTI: high in levels and in returns", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": crude(), "a": "brent", "b": "wti"}},
    {"name": "Brent / coffee: high in levels, ~0 in returns (spurious)", "origin": "extra",
     "args": lambda: {"prices": crude(), "a": "brent", "b": "coffee"}},
    {"name": "WTI / coffee", "origin": "extra",
     "args": lambda: {"prices": crude(), "a": "wti", "b": "coffee"}},
    {"name": "First year only (Jul 2016 – Jun 2017)", "origin": "extra",
     "args": lambda: {"prices": crude().loc[:"2017-06-30"], "a": "brent", "b": "wti"}},
    {"name": "Monotone but non-linear: Spearman = 1, Pearson < 1", "origin": "extra",
     "args": lambda: {"prices": pd.DataFrame({"x": np.exp(np.sqrt(np.arange(1, 51))),
                                              "y": np.exp(np.sqrt(np.arange(1, 51)) ** 3 / 50)}),
                      "a": "x", "b": "y"}},
]
