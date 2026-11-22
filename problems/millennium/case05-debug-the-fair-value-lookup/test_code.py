import pandas as pd

nan = float("nan")
prices = pd.DataFrame({
    "timestamp": ["2024-01-02 09:02:00", "2024-01-02 09:00:00", "2024-01-02 09:03:00",
                  "2024-01-02 09:01:00"],
    "Asset_1": [100.2, 100.0, 100.3, 100.1],
    "Asset_2": [nan, 50.0, 50.3, nan],
})
print(fair_value_at("2024-01-02 09:03:00", "Asset_1", prices, 5))   # exact match
print(fair_value_at("2024-01-02 09:02:30", "Asset_2", prices, 5))   # skip nulls
print(fair_value_at("2024-01-02 09:30:00", "Asset_1", prices, 5))   # stale
