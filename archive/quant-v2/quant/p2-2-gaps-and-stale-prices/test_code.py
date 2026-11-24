import pandas as pd

raw = pd.read_csv("data/p2_products_daily_synthetic.csv", parse_dates=["date"], index_col="date")
print("rows:", len(raw), "| duplicated dates:", raw.index.duplicated().sum(),
      "| rows removed by drop_duplicates():", len(raw) - len(raw.drop_duplicates()))

result = treat_gaps(raw)
prices, filled = result["prices"], result["filled"]
print("imputed values per column:", filled.sum().to_dict())
print("still missing per column :", prices.isna().sum().to_dict())
print(prices.loc["2018-10-04":"2018-10-17", ["gasoil_usd_t"]].assign(filled=filled.loc["2018-10-04":"2018-10-17", "gasoil_usd_t"]))
print(prices["jet_usd_t"].first_valid_index(), prices["jet_usd_t"].last_valid_index())
