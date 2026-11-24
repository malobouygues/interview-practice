import numpy as np
import pandas as pd

FUNCTION = "explain_spikes"


def hand_made():
    # six January days: a cold still spike, an outage spike, ordinary days
    index = pd.date_range("2024-01-08 23:00", periods=24 * 6, freq="h", tz="UTC")
    local = index.tz_convert("Europe/Paris")
    day = (np.arange(len(index)) // 24)
    load = np.full(len(index), 38000.0)
    wind = np.full(len(index), 9000.0)
    capacity = np.full(len(index), 47000.0)
    price = np.full(len(index), 90.0)
    load[day == 1] = 45000.0
    wind[day == 1] = 900.0
    price[(day == 1) & (local.hour == 18)] = 650.0           # cold and still
    capacity[day == 3] = 39000.0
    price[(day == 3) & (local.hour == 19)] = 420.0           # outage in mild weather
    price[(day == 5) & (local.hour == 8)] = 310.0            # nothing obvious
    hours = pd.DataFrame({"local_date": local.tz_localize(None).normalize(), "local_hour": local.hour,
                          "price_eur_mwh": price, "load_mw": load, "wind_mw": wind, "solar_mw": 0.0,
                          "available_capacity_mw": capacity, "gas_eur_mwh": 30.0}, index=index)
    dates = pd.date_range("2024-01-09", periods=6, freq="D").strftime("%Y-%m-%d")
    hdd = {"NORTH": [10, 21, 9, 4, 8, 7], "CENTRAL": [9, 19, 8, 3, 7, 6], "SOUTH": [6, 14, 5, 2, 4, 5]}
    rows = [{"zone": z, "local_date": d, "hdd": hdd[z][i]} for z in hdd for i, d in enumerate(dates)]
    return {"hours": hours, "daily": pd.DataFrame(rows)}


def files():
    hours = pd.read_csv("data/p1_power_hourly_treated_synthetic.csv")
    hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
    hours["local_date"] = pd.to_datetime(hours["local_date"])
    return {"hours": hours.set_index("delivery_start_utc"), "daily": pd.read_csv("data/p1_zone_daily_synthetic.csv")}


TESTS = [
    {"name": "Hand-made: one cold and still spike, one outage spike, one unexplained", "origin": "extra",
     "args": hand_made},
    {"name": "2023-2024: spike days and their drivers", "origin": "extra", "args": files},
]
