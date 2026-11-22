import pandas as pd

nan = float("nan")
prices = pd.DataFrame({
    "timestamp": ["2024-01-02 09:00:00", "2024-01-02 09:01:00", "2024-01-02 09:02:00",
                  "2024-01-02 09:03:00", "2024-01-02 09:04:00"],
    "Asset_1": [100.0, 100.1, 100.2, 100.3, 100.4],
    "Asset_2": [50.0, nan, 50.2, nan, nan],
    "Asset_3": [nan, 20.1, nan, nan, nan],
})
print(reference_price(prices, "Asset_1", "2024-01-02 09:03:30", 5))
print(reference_price(prices, "Asset_3", "2024-01-02 09:04:00", 2))
