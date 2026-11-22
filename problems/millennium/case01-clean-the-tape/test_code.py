import pandas as pd

nan = float("nan")
prices = pd.DataFrame(
    [["09:02", 100.2, 50.2, 20.2],
     ["09:00", 100.0, 50.0, 20.0],
     ["09:01", 100.1, nan, 20.1],
     ["09:00", 100.0, 50.0, 20.0]],
    columns=["timestamp", "Asset_1", "Asset_2", "Asset_3"])
print(clean_prices(prices))
