import numpy as np
import pandas as pd

FUNCTION = "weather_adjusted_load"


def hand_made():
    rng = np.random.default_rng(3)
    dates = pd.date_range("2023-01-01", "2024-02-29", freq="7D")
    rows = []
    for zone, b_hdd, b_cdd in [("A", 200.0, 50.0), ("B", 40.0, 300.0)]:
        for i, day in enumerate(dates):
            temperature = 12 - 10 * np.cos(2 * np.pi * day.dayofyear / 365) + rng.normal(0, 2)
            hdd = max(16 - temperature, 0)
            cdd = max(temperature - 21, 0)
            weekend = 1.0 if day.dayofweek >= 5 else 0.0
            load = 5000 + b_hdd * hdd + b_cdd * cdd - 600 * weekend + rng.normal(0, 40)
            rows.append({"zone": zone, "local_date": day.strftime("%Y-%m-%d"), "hdd": hdd, "cdd": cdd,
                         "load_avg_mw": load if i != 5 else np.nan})
    daily = pd.DataFrame(rows)
    normals = pd.DataFrame([{"zone": z, "month": m, "normal_hdd": max(16 - (12 - 10 * np.cos(2 * np.pi * (30 * m - 15) / 365)), 0),
                             "normal_cdd": max((12 - 10 * np.cos(2 * np.pi * (30 * m - 15) / 365)) - 21, 0) + 0.3}
                            for z in ["A", "B"] for m in range(1, 13)])
    return {"daily": daily, "normals": normals}


TESTS = [
    {"name": "Hand-made: two zones, known sensitivities, one missing day", "origin": "extra", "args": hand_made},
    {"name": "Three zones, 2023-2024, with the 30-year normals", "origin": "extra",
     "args": lambda: {"daily": pd.read_csv("data/p1_zone_daily_synthetic.csv"),
                      "normals": pd.read_csv("data/p1_weather_normals_synthetic.csv")}},
]
