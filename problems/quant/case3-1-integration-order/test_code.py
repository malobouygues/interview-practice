import numpy as np
import pandas as pd

crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
log_brent, log_wti = np.log(crude["brent"]), np.log(crude["wti"])
spread = log_brent - log_wti            # WTI discount to Brent, in log points

for name, s in [("log Brent", log_brent), ("log WTI", log_wti), ("log spread", spread)]:
    print(f"{name:11s}", integration_order(s))
print("average WTI discount:", round(spread.mean(), 4), "log points")
