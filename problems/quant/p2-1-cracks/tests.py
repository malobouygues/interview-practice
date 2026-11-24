import pandas as pd

FUNCTION = "build_daily_table"


def hand_made():
    rows = [
        ["2020-12-30", "brent", "USD/bbl", 50.0], ["2020-12-30", "gasoil", "USD/t", 447.0],
        ["2020-12-30", "ulsd", "USc/gal", 150.0], ["2020-12-30", "rbob", "USD/gal", 1.40],
        ["2020-12-30", "jet", "USD/t", 433.4], ["2020-12-30", "jet", "USD/t", 433.4],
        ["2020-12-31", "brent", "USD/bbl", 51.0], ["2020-12-31", "gasoil", "USD/t", 447.0],
        ["2020-12-31", "ulsd", "USc/gal", 152.0], ["2020-12-31", "rbob", "USD/gal", 1.41],
        ["2021-01-04", "brent", "USD/bbl", 52.0], ["2021-01-04", "gasoil", "USD/t", 447.0],
        ["2021-01-04", "ulsd", "USD/gal", 1.55], ["2021-01-04", "rbob", "USD/gal", 1.42],
        ["2021-01-04", "jet", "USD/t", 441.3],
        ["2021-01-05", "gasoil", "USD/t", 447.0], ["2021-01-05", "ulsd", "USD/gal", 1.56],
        ["2021-01-05", "rbob", "USD/gal", 1.43], ["2021-01-05", "jet", "USD/t", 445.0],
        ["2021-01-06", "brent", "USD/bbl", 53.0], ["2021-01-06", "gasoil", "USD/t", 455.0],
        ["2021-01-06", "ulsd", "USD/gal", 1.57], ["2021-01-06", "rbob", "USD/gal", 1.44],
        ["2021-01-06", "jet", "USD/t", 449.0],
    ]
    return {"raw": pd.DataFrame(rows, columns=["date", "product", "unit", "price"])}


def conflicting():
    frame = hand_made()["raw"]
    extra = pd.DataFrame([["2021-01-06", "brent", "USD/bbl", 53.4]], columns=frame.columns)
    return {"raw": pd.concat([frame, extra], ignore_index=True)}


TESTS = [
    {"name": "Hand-made: cents then dollars, tonnes, a copied row, a frozen gasoil run, a Brent holiday",
     "origin": "extra", "args": hand_made},
    {"name": "Two different Brent prices for the same date must stop the build", "origin": "extra",
     "args": conflicting, "raises": "AssertionError"},
    {"name": "The vendor file, 2017-2023", "origin": "extra",
     "args": lambda: {"raw": pd.read_csv("data/p2_products_daily_long_synthetic.csv")}},
]
