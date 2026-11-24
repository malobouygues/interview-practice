import pandas as pd

FUNCTION = "monthly_table"


def hand_made():
    rows = []
    volumes = {"2023-01": {"UK": 300, "France": 400, "Germany": 200, "Netherlands": 500},
               "2023-02": {"UK": 310, "France": 0, "Germany": 190, "Netherlands": 480},
               "2023-03": {"UK": 320, "France": 410, "Germany": 210}}
    for month, by_importer in volumes.items():
        for importer, total in by_importer.items():
            russia = 0.0 if month >= "2023-02" else total / 2
            other = 0.0 if total == 0 else total - russia
            rows.append([month, importer, "Russia", russia])
            rows.append([month, importer, "India", other])
    imports = pd.DataFrame(rows, columns=["month", "importer", "origin", "volume_kbd"])
    outages = pd.DataFrame({"refinery": ["R1", "R2"], "region": ["x", "y"], "start": ["2023-01-20", "2023-02-27"],
                            "end": ["2023-02-05", "2023-03-02"], "offline_kbd": [100, 300], "cause": ["fire", "strike"]})
    fundamentals = pd.DataFrame({"month": ["2023-01", "2023-02", "2023-03"], "refinery_utilisation_pct": [85.0, 86.0, 87.0],
                                 "distillate_stocks_mb": [400.0, 380.0, 390.0], "stocks_5y_avg_mb": [420.0, 415.0, 410.0]})
    days = pd.bdate_range("2023-01-02", "2023-03-31")
    daily = pd.DataFrame({"gasoil_crack": [20.0 + i * 0.1 for i in range(len(days))]}, index=days)
    daily.index.name = "date"
    daily.iloc[3] = float("nan")
    return {"imports": imports, "outages": outages, "fundamentals": fundamentals, "daily": daily}


def files():
    return {"imports": pd.read_csv("data/p2_diesel_imports_monthly_synthetic.csv"),
            "outages": pd.read_csv("data/p2_refinery_outages_synthetic.csv"),
            "fundamentals": pd.read_csv("data/p2_distillate_fundamentals_monthly_synthetic.csv"),
            "daily": pd.read_csv("data/p2_products_repaired_synthetic.csv", index_col="date", parse_dates=["date"])}


TESTS = [
    {"name": "Hand-made: a non-reporting country, an embargo zero, a ragged edge, outages across months",
     "origin": "extra", "args": hand_made},
    {"name": "Europe 2017-2023", "origin": "extra", "args": files},
]
