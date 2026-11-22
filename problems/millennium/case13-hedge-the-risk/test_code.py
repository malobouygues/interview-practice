import pandas as pd

prices = pd.DataFrame({
    "timestamp": ["2024-01-02 09:%02d:00" % i for i in range(10)],
    "Asset_1": [100.0, 100.5, 100.2, 101.0, 100.7, 101.5, 101.2, 102.0, 101.6, 102.3],
    "Asset_2": [50.0, 50.1, 50.3, 50.2, 50.6, 50.5, 50.9, 50.8, 51.2, 51.0],
    "Asset_3": [20.0, 20.3, 20.1, 20.6, 20.4, 20.9, 20.6, 21.2, 20.9, 21.4],
})
print(hedge_inventory(prices, {'Asset_1': 0, 'Asset_2': 0, 'Asset_3': 0}))
print(hedge_inventory(prices, {'Asset_1': 0, 'Asset_2': 0, 'Asset_3': 1000}))
