import numpy as np
import pandas as pd

FUNCTION = "adf_report"


def ttf():
    return pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]


def shocks():
    return np.random.default_rng(0).normal(size=500)


def persistent(n, phi, seed):
    e = np.random.default_rng(seed).normal(size=n)
    u = np.zeros(n)
    for t in range(n):
        u[t] = (phi * u[t - 1] if t else 0.0) + e[t]
    return pd.Series(u)


TESTS = [
    {"name": "TTF level, 'c': cannot reject the unit root", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"x": ttf(), "regression": "c"}},
    {"name": "TTF log returns, 'c': unit root rejected", "origin": "extra",
     "args": lambda: {"x": np.log(ttf()).diff(), "regression": "c"}},
    {"name": "White noise, 'n' (centred on zero)", "origin": "extra",
     "args": lambda: {"x": pd.Series(shocks()), "regression": "n"}},
    {"name": "Trend-stationary with 'c' only: looks like a unit root (misspecified)", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks()), "regression": "c"}},
    {"name": "Same series with 'ct': unit root rejected", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks()), "regression": "ct"}},
    {"name": "Stationary, persistent, only 40 obs: low power", "origin": "extra",
     "args": lambda: {"x": persistent(40, 0.8, 0), "regression": "c"}},
    {"name": "Stationary with a level shift: the break fools the test", "origin": "extra",
     "args": lambda: {"x": persistent(600, 0.5, 1) + 2.0 * (np.arange(600) >= 300), "regression": "c"}},
]
