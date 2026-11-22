import numpy as np
import pandas as pd

FUNCTION = "summary_stats"


def ttf():
    return pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]


TESTS = [
    {"name": "TTF price level", "origin": "extra", "check_no_mutation": True,
     "note": "Right-skewed level: mean above median.",
     "args": lambda: {"x": ttf()}},
    {"name": "TTF daily log returns (first value is NaN)", "origin": "extra",
     "note": "Returns: mean near zero, fat tails (excess kurtosis well above 0).",
     "args": lambda: {"x": np.log(ttf()).diff()}},
    {"name": "Hand-checkable: one extreme value", "origin": "extra",
     "note": "Mean 22 vs median 3: one outlier moves the mean, not the median.",
     "args": lambda: {"x": pd.Series([1.0, 2.0, 3.0, 4.0, 100.0])},
     "expected": {"n": 5, "mean": 22.0, "median": 3.0, "var": 1902.5, "std": 1902.5 ** 0.5,
                  "skew": float(pd.Series([1.0, 2.0, 3.0, 4.0, 100.0]).skew()),
                  "excess_kurtosis": float(pd.Series([1.0, 2.0, 3.0, 4.0, 100.0]).kurt())}},
    {"name": "Missing values are ignored", "origin": "extra",
     "args": lambda: {"x": pd.Series([2.0, np.nan, 4.0, 6.0, np.nan, 8.0])},
     "expected": lambda: {"n": 4, "mean": 5.0, "median": 5.0, "var": 20.0 / 3, "std": (20.0 / 3) ** 0.5,
                          "skew": 0.0, "excess_kurtosis": -1.2}},
    {"name": "Large normal sample: skew and excess kurtosis close to 0", "origin": "extra",
     "args": lambda: {"x": pd.Series(np.random.default_rng(42).normal(50.0, 5.0, 5000))}},
]
