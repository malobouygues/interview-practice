import numpy as np
import pandas as pd

FUNCTION = "treat_gaps"


def clean():
    hours = pd.read_csv("data/p1_power_hourly_clean_synthetic.csv")
    hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
    hours["local_date"] = pd.to_datetime(hours["local_date"])
    return hours.set_index("delivery_start_utc")


def three_june_days():
    index = pd.date_range("2024-06-10 22:00", periods=72, freq="h", tz="UTC")
    local = index.tz_convert("Europe/Paris")
    utc_hour = index.hour.values
    solar = np.where((utc_hour >= 5) & (utc_hour <= 18), 4000.0, np.nan)      # blank at night
    solar[(index >= "2024-06-12 09:00") & (index <= "2024-06-12 11:00")] = np.nan  # failure at midday
    wind = np.full(72, 6000.0)
    wind[30:32] = np.nan
    capacity = np.full(72, np.nan)
    capacity[0] = 43000.0                      # first hour of 11 June (local)
    capacity[48] = 42500.0                     # first hour of 13 June; 12 June was not sent
    price = np.full(72, 40.0)
    price[40] = np.nan
    hours = pd.DataFrame({"local_date": local.tz_localize(None).normalize(), "local_hour": local.hour,
                          "price_eur_mwh": price, "load_mw": 30000.0, "wind_mw": wind, "solar_mw": solar,
                          "available_capacity_mw": capacity, "gas_eur_mwh": 33.0}, index=index)
    hours.index.name = "delivery_start_utc"
    return {"hours": hours}


TESTS = [
    {"name": "Hand-made: three June days, a midday solar failure, a missed capacity report", "origin": "extra",
     "args": three_june_days, "check_no_mutation": True},
    {"name": "The clean hourly file, 2023-2024", "origin": "extra",
     "args": lambda: {"hours": clean()}, "check_no_mutation": True},
]
