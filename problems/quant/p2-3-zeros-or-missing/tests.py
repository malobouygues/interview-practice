import pandas as pd

FUNCTION = "total_imports"


def imports():
    return pd.read_csv("data/p2_diesel_imports_monthly_synthetic.csv")


def hand():
    return pd.DataFrame({
        "month": ["2020-01"] * 4 + ["2020-02"] * 4 + ["2020-03"] * 2,
        "importer": ["A", "A", "B", "B", "A", "A", "B", "B", "A", "A"],
        "origin": ["X", "Y", "X", "Y", "X", "Y", "X", "Y", "X", "Y"],
        "volume_kbd": [10.0, 0.0, 5.0, 7.0, 0.0, 0.0, 6.0, 8.0, 12.0, 3.0]})


def hand_expected():
    index = pd.to_datetime(["2020-01-01", "2020-02-01", "2020-03-01"])
    index.name = "month"
    nan = float("nan")
    table = pd.DataFrame({"A": [10.0, nan, 15.0], "B": [12.0, 14.0, nan], "total": [22.0, nan, nan]}, index=index)
    table.columns.name = "importer"
    return table


TESTS = [
    {"name": "Hand-made: a genuine zero, a non-report, a missing country", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"imports": hand()}, "expected": hand_expected},
    {"name": "European diesel imports 2017-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"imports": imports()}},
]
