import numpy as np
import pandas as pd

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
prices = prices.loc["2016-07-01":]                       # exports-allowed regime (tested in 4.9)
log_brent, log_wti, log_coffee = np.log(prices["brent"]), np.log(prices["wti"]), np.log(prices["coffee"])

runs = [("WTI on Brent, returns", log_wti.diff(), log_brent.diff()),
        ("WTI on Brent, LEVELS", log_wti, log_brent),
        ("coffee on Brent, returns", log_coffee.diff(), log_brent.diff()),
        ("coffee on Brent, LEVELS", log_coffee, log_brent)]
for name, y, x in runs:
    result = ols_fit(y, x)
    print(f"{name:26s} beta={result['beta']:.3f}  se={result['beta_se']:.4f}  t={result['beta_tstat']:7.1f}  "
          f"CI=[{result['beta_ci_low']:.3f}, {result['beta_ci_high']:.3f}]  R2={result['r2']:.3f}")
