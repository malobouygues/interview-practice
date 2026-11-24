import numpy as np
import pandas as pd

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices.loc["2016-07-01":]
log_brent, log_wti, log_coffee = np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])

for name, y, x in [("wti ~ brent", log_wti, log_brent),
                   ("coffee ~ brent", log_coffee, log_brent),
                   ("brent ~ coffee", log_brent, log_coffee)]:
    out = engle_granger(y, x)
    print(f"{name:15s} beta={out['beta']:.3f}  stat={out['adf_stat']:.2f}  naive p={out['naive_pvalue']:.4f}  "
          f"EG p={out['eg_pvalue']:.4f}  EG 5% crit={out['eg_crit_5pct']:.2f}  cointegrated={out['cointegrated']}")
