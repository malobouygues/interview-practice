import pandas as pd

FUNCTION = "known_at"


def hand_made():
    rows = []
    for month, value in [("2022-12", 100.0), ("2023-01", 101.0), ("2023-02", 102.0), ("2023-12", 104.0),
                         ("2024-01", 103.0), ("2024-02", 105.0)]:
        period = pd.Period(month, freq="M")
        first = (period + 2).to_timestamp(how="end").strftime("%Y-%m-%d")
        second = (period + 3).to_timestamp(how="end").strftime("%Y-%m-%d")
        annual = "%d-08-31" % (period.year + 1)
        rows += [[month, first, value - 2], [month, second, value - 1], [month, annual, value]]
    vintages = pd.DataFrame(rows, columns=["obs_month", "vintage_date", "demand_kbd"])
    return {"vintages": vintages, "decision_dates": ["2024-03-31", "2024-04-01", "2024-05-15"]}


TESTS = [
    {"name": "Hand-made: the day a vintage is published, and the day after", "origin": "extra", "args": hand_made},
    {"name": "Demand vintages, one decision date per quarter 2019-2024", "origin": "extra",
     "args": lambda: {"vintages": pd.read_csv("data/p3_us_oil_demand_vintages_synthetic.csv"),
                      "decision_dates": [d.strftime("%Y-%m-%d") for d in pd.date_range("2019-02-15", "2024-11-15", freq="3MS") + pd.Timedelta(days=14)]}},
]
