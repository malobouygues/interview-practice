import pandas as pd

prices = pd.DataFrame({
    "timestamp": ["09:00", "09:01", "09:02", "09:03"],
    "Asset_1": [100.0, 100.01, 100.0, 100.02],
    "Asset_2": [50.0, 50.2, 49.9, 50.3],
    "Asset_3": [20.0, 21.0, 19.5, 21.5],
})
requests = pd.DataFrame({
    "request_id": [1, 2, 3, 4, 5, 6],
    "timestamp": ["09:00", "09:00", "09:01", "09:02", "09:02", "09:03"],
    "asset": ["Asset_1", "Asset_1", "Asset_2", "Asset_1", "Asset_3", "Asset_2"],
    "side": ["BUY", "SELL", "BUY", "BUY", "SELL", "SELL"],
    "quantity": [100, 200, 100, 300, 50, 100],
})
print(liquidity_scores(prices, requests))
