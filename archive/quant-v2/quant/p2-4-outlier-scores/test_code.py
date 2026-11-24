import numpy as np
import pandas as pd

prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
rbob = prices["rbob_usd_gal"].dropna()
returns = np.log(rbob).diff()

scores = outlier_scores(returns)
print("days flagged:")
print("  |z| > 3                 ", (scores["z"].abs() > 3).sum())
print("  |modified z| > 3.5      ", (scores["modified_z"].abs() > 3.5).sum())
print("  IQR rule                ", scores["iqr_outlier"].sum())
print("  |rolling modified z| > 5", (scores["rolling_modified_z"].abs() > 5).sum())
print(scores.loc[["2017-08-28", "2019-05-14", "2019-05-15"]].round(3))
print("std with / without the two error days:",
      round(returns.std(), 4), round(returns.drop(pd.to_datetime(["2019-05-14", "2019-05-15"])).std(), 4))
