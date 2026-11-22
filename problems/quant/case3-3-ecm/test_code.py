import numpy as np
import pandas as pd

crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
log_brent, log_wti, log_coffee = np.log(crude["brent"]), np.log(crude["wti"]), np.log(crude["coffee"])

print("WTI ~ Brent   :", fit_ecm(log_wti, log_brent))
print("coffee ~ Brent:", fit_ecm(log_coffee, log_brent), " <- not cointegrated: meaningless")

# what a deviation looks like: the August 2017 WTI-specific shock and its correction
spread = log_brent - log_wti
print(spread.loc["2017-08-24":"2017-09-15"].round(3))
