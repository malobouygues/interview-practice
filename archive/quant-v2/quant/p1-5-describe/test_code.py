import numpy as np
import pandas as pd

prices = pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")

brent = prices["brent"].dropna()               # observed prices only (holidays removed)
brent_returns = np.log(brent).diff()            # return between two consecutive observed prices
spread = prices["brent"] - prices["wti"]        # USD/bbl, NaN when either leg is missing

for name, series in [("Brent level", brent), ("Brent log returns", brent_returns), ("Brent-WTI spread", spread)]:
    stats = summary_stats(series)
    print(name)
    for key, value in stats.items():
        print(f"    {key:16s} {value:12.4f}")
