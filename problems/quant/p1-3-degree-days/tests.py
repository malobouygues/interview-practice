import pandas as pd

FUNCTION = "daily_zone_table"


def hand_made():
    # two zones around the October clock change; irregular readings; one sensor code; a short day
    stamps = pd.date_range("2023-10-27 22:50", "2023-10-29 22:50", freq="h", tz="UTC")
    rows = []
    for i, stamp in enumerate(stamps):
        rows.append([stamp.strftime("%Y-%m-%dT%H:%M:%SZ"), "A", 10.0 + (i % 5)])
        if i % 7 == 0:
            rows.append([(stamp - pd.Timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ"), "A", 30.0])
        if i < 20:
            rows.append([stamp.strftime("%Y-%m-%dT%H:%M:%SZ"), "B", 25.0 if i != 3 else 99.9])
    temps = pd.DataFrame(rows, columns=["observed_at_utc", "zone", "temperature_c"])
    hours = pd.date_range("2023-10-27 22:00", "2023-10-29 22:00", freq="h", tz="UTC")
    load_rows = []
    for i, hour in enumerate(hours):
        load_rows.append([hour.strftime("%Y-%m-%dT%H:%M:%SZ"), "A", 1000.0 + i])
        if i % 3 != 0:
            load_rows.append([hour.strftime("%Y-%m-%dT%H:%M:%SZ"), "B", 500.0])
    load = pd.DataFrame(load_rows, columns=["delivery_start_utc", "zone", "load_mw"])
    zones = pd.DataFrame({"zone": ["A", "B"], "description": ["a", "b"], "station": ["x", "y"],
                          "hdd_base_c": [15.5, 17.0], "cdd_base_c": [22.0, 21.0]})
    return {"temps": temps, "load": load, "zones": zones}


def files():
    return {"temps": pd.read_csv("data/p1_zone_temperature_obs_synthetic.csv"),
            "load": pd.read_csv("data/p1_zone_load_hourly_synthetic.csv"),
            "zones": pd.read_csv("data/p1_zones_reference_synthetic.csv")}


TESTS = [
    {"name": "Hand-made: a 25-hour day, extra :20 readings, a 99.9 sensor code, two coverage failures",
     "origin": "extra", "args": hand_made},
    {"name": "Three zones, 2023-2024", "origin": "extra", "args": files},
]
