import numpy as np
import pandas as pd

ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
table = make_returns(ttf)
print(table.head())

first, last = ttf.iloc[0], ttf.iloc[-1]
print("total move, log      :", np.log(last / first))
print("sum of log returns   :", table["log_return"].sum())
print("total move, %        :", last / first - 1)
print("sum of % changes     :", table["pct_change"].sum(), "  <- not the total move")
print("compounded % changes :", (1 + table["pct_change"].dropna()).prod() - 1)

spread = pd.Series([1.2, 0.4, -0.3, 0.8])   # e.g. a TTF - NBP spread in EUR/MWh
try:
    make_returns(spread)
except ValueError as exc:
    print("spread ->", exc)
