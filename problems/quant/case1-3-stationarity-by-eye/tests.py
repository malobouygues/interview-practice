import numpy as np
import pandas as pd

FUNCTION = "subsample_stats"


def shocks():
    return np.random.default_rng(0).normal(size=500)


def ttf():
    return pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]


TESTS = [
    {"name": "Hand-checkable: 8 values, 2 blocks", "origin": "extra",
     "args": lambda: {"x": pd.Series([1.0, 2.0, 3.0, 4.0, 11.0, 12.0, 13.0, 14.0]), "parts": 2},
     "expected": {"means": [2.5, 12.5], "stds": [1.2909944487358056, 1.2909944487358056],
                  "mean_shift": 10.0 / 1.2909944487358056, "std_ratio": 1.0}},
    {"name": "White noise: block means close, stds similar", "origin": "extra",
     "args": lambda: {"x": pd.Series(shocks())}},
    {"name": "Random walk: block means wander", "origin": "extra",
     "args": lambda: {"x": pd.Series(shocks()).cumsum()}},
    {"name": "Trend-stationary: means climb, dispersion stable", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks())}},
    {"name": "TTF price level", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"x": ttf()}},
    {"name": "TTF log returns (NaN dropped), 5 blocks of unequal size", "origin": "extra",
     "args": lambda: {"x": np.log(ttf()).diff(), "parts": 5}},
]
