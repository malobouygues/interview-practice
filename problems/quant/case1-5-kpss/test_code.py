import numpy as np
import pandas as pd

ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
e = np.random.default_rng(0).normal(size=500)


def persistent(n, phi, seed):
    shocks = np.random.default_rng(seed).normal(size=n)
    u = np.zeros(n)
    for t in range(n):
        u[t] = (phi * u[t - 1] if t else 0.0) + shocks[t]
    return pd.Series(u)


cases = [
    ("TTF price level", ttf, "c"),
    ("TTF log returns", np.log(ttf).diff(), "c"),
    ("trend-stationary, 'c'", pd.Series(0.05 * np.arange(500) + e), "c"),
    ("trend-stationary, 'ct'", pd.Series(0.05 * np.arange(500) + e), "ct"),
    ("persistent, 2000 obs", persistent(2000, 0.97, 1), "c"),
    ("persistent, 40 obs", persistent(40, 0.8, 0), "c"),
]
for name, series, reg in cases:
    out = stationarity_verdict(series, reg)
    print(f"{name:24s} ADF p={out['adf_pvalue']:.3f}  KPSS p={out['kpss_pvalue']:.3f}  -> {out['verdict']}")
