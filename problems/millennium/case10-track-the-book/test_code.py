import pandas as pd

fills = pd.DataFrame({
    "asset": ["Asset_1", "Asset_1"],
    "side": ["BUY", "SELL"],
    "quantity": [100, 100],
    "fill_price": [100.05, 99.95],
})
prices = pd.DataFrame({
    "timestamp": ["09:00", "09:01"],
    "Asset_1": [99.9, 100.0], "Asset_2": [50.1, 50.0], "Asset_3": [19.5, 20.0],
})
print(track_book(fills, prices))
