import pandas as pd

nan = float("nan")
prices = pd.DataFrame(
    [[2000, nan, 50.2, 20.2],
     [0, 100.0, 50.0, 20.0],
     [1000, 100.1, 0.0, 20.1],
     [1000, 999.0, 999.0, 999.0]],
    columns=["timestamp", "Asset_1", "Asset_2", "Asset_3"])
print(clean_tape(prices))
