import numpy as np
import pandas as pd

FUNCTION = "correlation_report"


def prices():
    return pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")


def monotone():
    x = np.sqrt(np.arange(1.0, 51.0))
    return pd.DataFrame({"x": x, "y": x ** 3})


TESTS = [
    {"name": "Brent / Dubai", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": prices(), "a": "brent", "b": "dubai"}},
    {"name": "Brent / WTI: one event drags Pearson on changes", "origin": "extra",
     "args": lambda: {"prices": prices(), "a": "brent", "b": "wti"}},
    {"name": "Brent / WTI without the two expiry days", "origin": "extra",
     "args": lambda: {"prices": prices().drop(pd.to_datetime(["2020-04-20", "2020-04-21"])), "a": "brent", "b": "wti"}},
    {"name": "Monotone but non-linear: Spearman = 1 in levels, Pearson < 1", "origin": "extra",
     "args": lambda: {"prices": monotone(), "a": "x", "b": "y"}},
]
