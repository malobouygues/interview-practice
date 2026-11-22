import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices.loc["2016-07-01":]
log_brent, log_wti = np.log(prices["brent"]), np.log(prices["wti"])

# controlled examples (as in the source document)
e = np.random.default_rng(0).normal(size=500)
random_walk = pd.Series(e).cumsum()
trend_stationary = pd.Series(0.05 * np.arange(500) + e)


def persistent(n, phi, seed):
    """Stationary but persistent: each day keeps a share phi of yesterday's deviation."""
    shocks = np.random.default_rng(seed).normal(size=n)
    values = np.zeros(n)
    for t in range(n):
        previous = values[t - 1] if t > 0 else 0.0
        values[t] = phi * previous + shocks[t]
    return pd.Series(values)


cases = [("log Brent", log_brent, "c"), ("log WTI", log_wti, "c"),
         ("Brent returns", log_brent.diff(), "n"), ("WTI returns", log_wti.diff(), "n"),
         ("log spread Brent - WTI", log_brent - log_wti, "c"),
         ("random walk", random_walk, "c"),
         ("trend-stationary, 'c'", trend_stationary, "c"), ("trend-stationary, 'ct'", trend_stationary, "ct"),
         ("stationary, only 40 obs", persistent(40, 0.8, 0), "c"),
         ("stationary + level shift", persistent(600, 0.5, 1) + 2.0 * (np.arange(600) >= 300), "c")]
for name, series, regression in cases:
    out = adf_report(series, regression)
    print(f"{name:26s} [{regression:2s}] stat={out['stat']:8.2f}  crit5%={out['crit_5pct']:6.2f}  "
          f"p={out['pvalue']:.3f}  lags={out['lags']:2d}  reject={out['reject_unit_root']}")

print("lag choice on the log spread (fixed lags, no AIC):")
spread = (log_brent - log_wti).dropna()
for lags in [0, 5, 20]:
    stat, pvalue = adfuller(spread, maxlag=lags, regression="c", autolag=None)[:2]
    print(f"  {lags:2d} lags: stat={stat:6.2f}  p={pvalue:.4f}")
