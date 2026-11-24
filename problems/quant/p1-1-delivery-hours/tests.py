import pandas as pd

FUNCTION = "load_market_hours"

COLUMNS = ["delivery_start_local", "utc_offset", "price_eur_mwh", "load_mw", "wind_mw", "solar_mw",
           "available_capacity_mw", "gas_eur_mwh", "loaded_at_utc"]


def write(rows, name):
    pd.DataFrame(rows, columns=COLUMNS).to_csv(name, index=False)
    return {"path": name}


def autumn_day():
    # the end of summer time: 02:00 happens twice; one record sent twice; one record corrected
    rows = [
        ["2023-10-29 01:00", "+02:00", 34.7, 22519, 3596, None, 45280, 44.04, "2023-10-30T05:00:00Z"],
        ["2023-10-29 02:00", "+02:00", 35.8, 21878, 2256, None, None, 44.04, "2023-10-30T05:00:00Z"],
        ["2023-10-29 02:00", "+01:00", 33.0, 21827, 2607, None, None, 44.04, "2023-10-30T05:00:00Z"],
        ["2023-10-29 02:00", "+01:00", 33.0, 21827, 2607, None, None, 44.04, "2023-10-30T05:00:00Z"],
        ["2023-10-29 03:00", "+01:00", 309.7, 21737, 3135, None, None, 44.04, "2023-10-30T05:00:00Z"],
        ["2023-10-29 03:00", "+01:00", 30.97, 21737, 3135, None, None, 44.04, "2023-10-31T08:00:00Z"],
    ]
    return write(rows, "autumn_day.csv")


def spring_day():
    # 02:00 local does not exist on the last Sunday of March: 01:00 (+01:00) is followed by 03:00 (+02:00)
    rows = [
        ["2024-03-31 00:00", "+01:00", 51.2, 25000, 8000, None, 47000, 26.1, "2024-04-01T04:00:00Z"],
        ["2024-03-31 01:00", "+01:00", 49.9, 24100, 8100, None, None, 26.1, "2024-04-01T04:00:00Z"],
        ["2024-03-31 03:00", "+02:00", 48.0, 23600, 8300, None, None, 26.1, "2024-04-01T04:00:00Z"],
        ["2024-03-31 04:00", "+02:00", 47.1, 23400, 8200, None, None, 26.1, "2024-04-01T04:00:00Z"],
    ]
    return write(rows, "spring_day.csv")


TESTS = [
    {"name": "Hand-made autumn DST day: two different 02:00 hours, one copy, one correction", "origin": "extra",
     "args": autumn_day},
    {"name": "Hand-made spring DST day: no 02:00 hour, nothing to invent", "origin": "extra",
     "args": spring_day},
    {"name": "The vendor file, 2023-2024", "origin": "extra",
     "args": lambda: {"path": "data/p1_power_hourly_vendor_synthetic.csv"}},
]
