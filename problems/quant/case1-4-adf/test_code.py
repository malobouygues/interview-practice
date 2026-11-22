import numpy as np
import pandas as pd

ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
rng = np.random.default_rng(0)
e = rng.normal(size=500)


def persistent(n, phi, seed):
    """Stationary but persistent: each day keeps a fraction phi of yesterday's deviation."""
    shocks = np.random.default_rng(seed).normal(size=n)
    u = np.zeros(n)
    for t in range(n):
        u[t] = (phi * u[t - 1] if t else 0.0) + shocks[t]
    return pd.Series(u)


cases = [
    ("TTF price level", ttf, "c"),
    ("TTF log returns", np.log(ttf).diff(), "c"),
    ("trend-stationary, 'c' only", pd.Series(0.05 * np.arange(500) + e), "c"),
    ("trend-stationary, 'ct'", pd.Series(0.05 * np.arange(500) + e), "ct"),
    ("stationary but only 40 obs", persistent(40, 0.8, 0), "c"),
    ("stationary + level shift", persistent(600, 0.5, 1) + 2.0 * (np.arange(600) >= 300), "c"),
]
for name, series, reg in cases:
    out = adf_report(series, reg)
    print(f"{name:30s} stat={out['stat']:8.2f}  crit5%={out['crit_5pct']:6.2f}  "
          f"p={out['pvalue']:.3f}  reject={out['reject_unit_root']}")
