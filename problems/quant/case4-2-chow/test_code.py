import numpy as np
import pandas as pd

history = pd.read_csv("data/crude_history_synthetic.csv", parse_dates=["date"], index_col="date")
log_brent, log_wti = np.log(history["brent"]), np.log(history["wti"])
r_brent, r_wti = log_brent.diff(), log_wti.diff()

post = history.index >= "2016-07-01"
pre = history.index < "2016-01-01"
runs = [
    ("returns, break 2016-01-01", r_wti, r_brent, "2016-01-01"),
    ("returns, placebo 2018 (post regime only)", r_wti[post], r_brent[post], "2018-01-01"),
    ("returns, placebo 2014 (pre regime only)", r_wti[pre], r_brent[pre], "2014-01-01"),
    ("LEVELS, placebo 2018 (post regime only)", log_wti[post], log_brent[post], "2018-01-01"),
]
for name, y, x, date in runs:
    out = chow_test(y, x, date)
    print(f"{name:42s} F={out['F']:9.2f}  p={out['pvalue']:.4f}  reject={out['reject']}")
