import pandas as pd

products = pd.read_csv("data/p2_products_daily_synthetic.csv", parse_dates=["date"], index_col="date")
products = products[~products.index.duplicated(keep="first")]      # two dates were delivered twice

cracks = crack_spreads(products)
print(cracks.describe().round(2))

print("average crack by calendar month (USD/bbl):")
print(cracks[["diesel_crack", "gasoline_crack"]].groupby(cracks.index.month).mean().round(1))

print(cracks.loc["2019-05-10":"2019-05-17", "gasoline_crack"])        # something odd here
