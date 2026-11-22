import numpy as np
import pandas as pd

history = pd.read_csv("data/crude_history_synthetic.csv", parse_dates=["date"], index_col="date")
print(history.iloc[[0, -1]])

out = regime_comparison(history, "2016-01-01")
for period in ("pre", "post"):
    print(period, {k: round(v, 4) for k, v in out[period].items()})
print("full-sample Engle-Granger p-value:", round(out["full_eg_pvalue"], 3))

spread = np.log(history["brent"]) - np.log(history["wti"])
print(spread.resample("YE").mean().round(3))     # yearly average WTI discount
