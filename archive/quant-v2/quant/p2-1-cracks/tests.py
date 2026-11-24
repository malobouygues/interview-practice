import pandas as pd

FUNCTION = "crack_spreads"


def products():
    raw = pd.read_csv("data/p2_products_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return raw[~raw.index.duplicated(keep="first")]


def hand():
    index = pd.to_datetime(["2018-01-02"])
    return pd.DataFrame({"brent_usd_bbl": [66.0], "ulsd_usd_gal": [2.0], "rbob_usd_gal": [1.8],
                         "gasoil_usd_t": [596.0], "jet_usd_t": [630.4]}, index=index)


def hand_expected():
    index = pd.to_datetime(["2018-01-02"])
    return pd.DataFrame({"diesel_crack": [18.0], "gasoline_crack": [9.6], "gasoil_crack": [14.0],
                         "jet_crack": [14.0], "crack_321": [(2 * 75.6 + 84.0 - 3 * 66.0) / 3]}, index=index)


TESTS = [
    {"name": "Hand-checkable: one day", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"products": hand()}, "expected": hand_expected},
    {"name": "Products 2017-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"products": products()}},
]
