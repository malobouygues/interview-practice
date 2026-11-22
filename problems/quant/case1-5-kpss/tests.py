import numpy as np
import pandas as pd

FUNCTION = "stationarity_verdict"


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
    {"name": "TTF level -> unit root", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"x": ttf()}},
    {"name": "TTF log returns -> stationary", "origin": "extra",
     "args": lambda: {"x": np.log(ttf()).diff()}},
    {"name": "Trend-stationary tested with 'c' -> (misleading) unit root", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks()), "regression": "c"}},
    {"name": "Same series with 'ct' -> stationary", "origin": "extra",
     "args": lambda: {"x": pd.Series(0.05 * np.arange(500) + shocks()), "regression": "ct"}},
    {"name": "Very persistent series, 2000 obs -> conflict", "origin": "extra",
     "args": lambda: {"x": persistent(2000, 0.97, 1)}},
    {"name": "Short persistent series, 40 obs -> inconclusive", "origin": "extra",
     "args": lambda: {"x": persistent(40, 0.8, 0)}},
    {"name": "Stationary series with a level shift -> fooled into 'unit root'", "origin": "extra",
     "args": lambda: {"x": persistent(600, 0.5, 1) + 2.0 * (np.arange(600) >= 300)}},
    {"name": "Same 40-obs design, another draw: inconclusive at 5 %...", "origin": "extra",
     "args": lambda: {"x": persistent(40, 0.8, 3), "regression": "c", "alpha": 0.05}},
    {"name": "...but 'stationary' at 10 %: the verdict depends on the level you chose", "origin": "extra",
     "args": lambda: {"x": persistent(40, 0.8, 3), "regression": "c", "alpha": 0.10}},
]
