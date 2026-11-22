import pandas as pd

FUNCTION = "reference_price"
NaN = float("nan")


def tape():
    return pd.DataFrame({
        "timestamp": ["2024-01-02 09:%02d:00" % i for i in range(11)],
        "Asset_1": [100.0, 100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8, 100.9, 101.0],
        "Asset_2": [50.0, NaN, 50.2, NaN, NaN, 50.5, 50.6, 0.0, -1.0, 50.9, 51.0],
        "Asset_3": [NaN, 20.1, NaN, NaN, NaN, NaN, NaN, NaN, 20.8, NaN, NaN],
    })


def case(asset, ts, staleness):
    return lambda: {"prices": tape(), "asset": asset, "ts": ts, "max_staleness_minutes": staleness}


TESTS = [
    {"name": "Request exactly on a bar", "origin": "extra",
     "args": case("Asset_1", "2024-01-02 09:03:00", 5), "expected": {"price": 100.3}},
    {"name": "Request between two bars", "origin": "extra",
     "args": case("Asset_1", "2024-01-02 09:03:30", 5), "expected": {"price": 100.3}},
    {"name": "NaN bars are skipped", "origin": "extra",
     "args": case("Asset_2", "2024-01-02 09:04:00", 5), "expected": {"price": 50.2}},
    {"name": "Illiquid asset: last print too old", "origin": "extra",
     "args": case("Asset_3", "2024-01-02 09:07:00", 5), "expected": {"price": None}},
    {"name": "Exactly max_staleness_minutes old is still fine", "origin": "extra",
     "args": case("Asset_3", "2024-01-02 09:06:00", 5), "expected": {"price": 20.1}},
    {"name": "No valid price at or before ts", "origin": "extra",
     "args": case("Asset_3", "2024-01-02 09:00:30", 5), "expected": {"price": None}},
    {"name": "Request before the tape starts", "origin": "extra",
     "args": case("Asset_1", "2024-01-02 08:59:00", 5), "expected": {"price": None}},
    {"name": "Non-positive prints are not valid prices", "origin": "extra",
     "args": case("Asset_2", "2024-01-02 09:08:30", 5), "expected": {"price": 50.6}},
    {"name": "Request after the end of the tape, still fresh", "origin": "extra",
     "args": case("Asset_1", "2024-01-02 09:12:00", 5), "expected": {"price": 101.0}},
    {"name": "Request long after the end of the tape", "origin": "extra",
     "args": case("Asset_3", "2024-01-02 09:30:00", 5), "expected": {"price": None}},
    {"name": "ts given as a pd.Timestamp", "origin": "extra",
     "args": case("Asset_3", pd.Timestamp("2024-01-02 09:08:00"), 1), "expected": {"price": 20.8}},
    {"name": "Fractional staleness limit, on the boundary", "origin": "extra",
     "args": case("Asset_1", "2024-01-02 09:03:30", 0.5), "expected": {"price": 100.3}},
    {"name": "Fractional staleness limit, one second too old", "origin": "extra",
     "args": case("Asset_1", "2024-01-02 09:03:31", 0.5), "expected": {"price": None}},
]
