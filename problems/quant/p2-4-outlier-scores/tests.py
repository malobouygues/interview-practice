import numpy as np
import pandas as pd

FUNCTION = "outlier_scores"


def rbob_returns():
    prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
    return np.log(prices["rbob_usd_gal"].dropna()).diff()


def toy():
    values = np.random.default_rng(5).normal(0, 0.01, 120)
    values[100] = 0.2
    return pd.Series(values, index=pd.bdate_range("2021-01-04", periods=120))


TESTS = [
    {"name": "Toy series with one planted spike", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"returns": toy()}},
    {"name": "RBOB daily log returns 2017-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"returns": rbob_returns()}},
]
