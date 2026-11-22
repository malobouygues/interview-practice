import pandas as pd

prices = pd.DataFrame({
    "timestamp": ["2024-01-02 09:%02d:00" % i for i in range(11)],
    "Asset_1": [100.0, 100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8, 100.9, 101.0],
})
fills = pd.DataFrame({
    "client_id": ["CLIENT_A", "CLIENT_B"],
    "timestamp": ["2024-01-02 09:00:00", "2024-01-02 09:00:00"],
    "asset": ["Asset_1", "Asset_1"],
    "side": ["BUY", "SELL"],
    "quantity": [100, 100],
    "fill_price": [100.0, 100.0],
})
print(client_markout(fills, prices, 5))
