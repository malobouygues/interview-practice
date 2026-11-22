import numpy as np
import pandas as pd

crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
log_brent, log_wti, log_coffee = np.log(crude["brent"]), np.log(crude["wti"]), np.log(crude["coffee"])

print("WTI on Brent, log levels :", ols_fit(log_wti, log_brent))
print("WTI on Brent, log returns:", ols_fit(log_wti.diff(), log_brent.diff()))
print("coffee on Brent, levels  :", ols_fit(log_coffee, log_brent))
