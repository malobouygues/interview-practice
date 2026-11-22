import pandas as pd

FUNCTION = "fair_value_at"
NaN = float("nan")

ROWS = [
    ["2024-01-02 09:00:00", 100.0, 50.0, 20.0],
    ["2024-01-02 09:01:00", 100.1, NaN, 20.1],
    ["2024-01-02 09:02:00", 100.2, NaN, NaN],
    ["2024-01-02 09:03:00", 100.3, 50.3, NaN],
    ["2024-01-02 09:04:00", 100.4, 50.4, NaN],
    ["2024-01-02 09:10:00", 101.0, 51.0, NaN],
]


def tape(order=(0, 1, 2, 3, 4, 5)):
    return pd.DataFrame([ROWS[i] for i in order],
                        columns=["timestamp", "Asset_1", "Asset_2", "Asset_3"])


def shuffled():
    return tape(order=(4, 0, 5, 2, 3, 1))


def case(ts, asset, staleness, frame=tape):
    return lambda: {"ts": ts, "asset": asset, "prices": frame(),
                    "max_staleness_minutes": staleness}


TESTS = [
    {"name": "Query between two bars (the easy case)", "origin": "extra",
     "args": case("2024-01-02 09:03:30", "Asset_1", 5), "expected": {"price": 100.3}},
    {"name": "Query lands exactly on a bar", "origin": "extra",
     "args": case("2024-01-02 09:03:00", "Asset_1", 5), "expected": {"price": 100.3}},
    {"name": "Query exactly on the first bar", "origin": "extra",
     "args": case("2024-01-02 09:00:00", "Asset_1", 5), "expected": {"price": 100.0}},
    {"name": "Stale quote returns null", "origin": "extra",
     "args": case("2024-01-02 09:09:00", "Asset_1", 3), "expected": {"price": None}},
    {"name": "Exactly max_staleness_minutes old is acceptable", "origin": "extra",
     "args": case("2024-01-02 09:09:00", "Asset_1", 5), "expected": {"price": 100.4}},
    {"name": "Unsorted input", "origin": "extra",
     "args": case("2024-01-02 09:03:30", "Asset_1", 5, shuffled), "expected": {"price": 100.3}},
    {"name": "Null bars are skipped", "origin": "extra",
     "args": case("2024-01-02 09:02:30", "Asset_2", 5), "expected": {"price": 50.0}},
    {"name": "Exact bar is null: walk back", "origin": "extra",
     "args": case("2024-01-02 09:02:00", "Asset_3", 5), "expected": {"price": 20.1}},
    {"name": "Walk back over nulls, then too stale", "origin": "extra",
     "args": case("2024-01-02 09:04:00", "Asset_3", 2), "expected": {"price": None}},
    {"name": "Before the first print", "origin": "extra",
     "args": case("2024-01-02 08:59:00", "Asset_1", 5), "expected": {"price": None}},
    {"name": "Unsorted input, exact match, nulls around", "origin": "extra",
     "args": case("2024-01-02 09:10:00", "Asset_2", 5, shuffled), "expected": {"price": 51.0}},
    {"name": "Unsorted input and stale", "origin": "extra",
     "args": case("2024-01-02 09:09:30", "Asset_2", 5, shuffled), "expected": {"price": None}},
]
