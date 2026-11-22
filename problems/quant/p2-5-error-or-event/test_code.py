import numpy as np
import pandas as pd

prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
usd_bbl = pd.DataFrame({"rbob": prices["rbob_usd_gal"] * 42,
                        "ulsd": prices["ulsd_usd_gal"] * 42,
                        "gasoil": prices["gasoil_usd_t"] / 7.45})
usd_bbl = usd_bbl.dropna()                       # days where the three products settled
returns = np.log(usd_bbl).diff().dropna()

decisions = classify_extremes(returns, "rbob")
print(decisions.round({"return": 3, "score": 1}).to_string())
print(returns.loc["2017-08-24":"2017-09-05"].round(3))
