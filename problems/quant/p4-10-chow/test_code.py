import numpy as np
import pandas as pd

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
log_brent, log_wti = np.log(prices["brent"]), np.log(prices["wti"])
brent_returns, wti_returns = log_brent.diff(), log_wti.diff()

post = prices.index >= "2016-07-01"
pre = prices.index < "2016-01-01"
runs = [
    ("returns, break 2016-01-01", wti_returns, brent_returns, "2016-01-01"),
    ("returns, placebo 2018 (post regime)", wti_returns[post], brent_returns[post], "2018-01-01"),
    ("returns, placebo 2014 (pre regime)", wti_returns[pre], brent_returns[pre], "2014-01-01"),
    ("LEVELS, placebo 2018 (post regime)", log_wti[post], log_brent[post], "2018-01-01"),
]
for name, y, x, date in runs:
    out = chow_test(y, x, date)
    print(f"{name:38s} F={out['F']:9.2f}  p={out['pvalue']:.4f}  reject={out['reject']}")
