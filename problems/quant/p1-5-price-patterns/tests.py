import numpy as np
import pandas as pd

FUNCTION = "price_patterns"


def hand_made():
    rng = np.random.default_rng(5)
    index = pd.date_range("2024-01-31 23:00", periods=24 * 40, freq="h", tz="UTC")
    local = index.tz_convert("Europe/Paris")
    hour = local.hour.values
    load = 30000 + 4000 * np.sin(2 * np.pi * (hour - 6) / 24) + rng.normal(0, 500, len(index))
    solar = np.where((hour >= 8) & (hour <= 16), 3000 * np.sin(np.pi * (hour - 8) / 8), 0.0) + rng.normal(0, 50, len(index)).clip(0)
    price = 40 + 0.004 * (load - 30000) - 0.002 * solar + rng.standard_t(3, len(index)) * 5
    price[100] = np.nan
    hours = pd.DataFrame({"local_date": local.tz_localize(None).normalize(), "local_hour": hour,
                          "price_eur_mwh": price, "load_mw": load, "solar_mw": solar}, index=index)
    return {"hours": hours}


def treated():
    hours = pd.read_csv("data/p1_power_hourly_treated_synthetic.csv")
    hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
    hours["local_date"] = pd.to_datetime(hours["local_date"])
    return {"hours": hours.set_index("delivery_start_utc")}


TESTS = [
    {"name": "Hand-made: 40 winter days with a daily cycle and fat-tailed noise", "origin": "extra",
     "args": hand_made},
    {"name": "The treated hourly file, 2023-2024", "origin": "extra", "args": treated},
]
