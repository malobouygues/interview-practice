import pandas as pd

FUNCTION = "add_availability"


def hand_made():
    stocks = pd.DataFrame({
        "week_ending": ["2022-01-14", "2021-12-31", "2022-01-07", "2022-06-17"],
        "release_date": ["2022-01-20", "2022-01-05", "2022-01-12", "2022-06-29"],
        "release_time_et": ["10:30", "10:30", "10:30", "10:30"],
        "crude_stocks_mbbl": [413.3, 417.9, 413.3, 418.7],
        "consensus_change_mbbl": [-1.5, -3.0, -2.0, 1.0],
        "ingested_at_utc": ["2022-01-20T15:37:00Z", "2020-03-02T09:00:00Z", "2022-01-12T15:37:00Z", "2022-06-29T14:37:00Z"],
    })
    return {"stocks": stocks}


TESTS = [
    {"name": "Hand-made: a Thursday release after a Monday holiday, a backfilled record, a late summer release",
     "origin": "extra", "args": hand_made, "check_no_mutation": True},
    {"name": "Weekly reports 2019-2024", "origin": "extra",
     "args": lambda: {"stocks": pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")}},
]
