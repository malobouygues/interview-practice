import numpy as np
import pandas as pd

prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
usd_bbl = pd.DataFrame({"ulsd": prices["ulsd_usd_gal"] * 42,
                        "gasoil": prices["gasoil_usd_t"] / 7.45,
                        "brent": prices["brent_usd_bbl"]}).dropna()
returns = np.log(usd_bbl).diff()

print("ULSD -> gasoil (returns)")
print(lead_lag_table(returns["ulsd"], returns["gasoil"], 3).round(3))
print("Brent -> gasoil (returns)")
print(lead_lag_table(returns["brent"], returns["gasoil"], 3).round(3))
print("ULSD -> gasoil (price LEVELS)")
print(lead_lag_table(usd_bbl["ulsd"], usd_bbl["gasoil"], 3).round(3))
