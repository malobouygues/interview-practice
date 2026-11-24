import numpy as np
import pandas as pd

FUNCTION = "classify_extremes"


def product_returns():
    prices = pd.read_csv("data/p2_products_treated_synthetic.csv", parse_dates=["date"], index_col="date")
    usd_bbl = pd.DataFrame({"rbob": prices["rbob_usd_gal"] * 42, "ulsd": prices["ulsd_usd_gal"] * 42,
                            "gasoil": prices["gasoil_usd_t"] / 7.45}).dropna()
    return np.log(usd_bbl).diff().dropna()


def toy():
    rng = np.random.default_rng(3)
    index = pd.bdate_range("2022-01-03", periods=100)
    returns = pd.DataFrame({"a": rng.normal(0, 0.01, 100), "b": rng.normal(0, 0.01, 100),
                            "c": rng.normal(0, 0.01, 100)}, index=index)
    returns.loc[index[70], "a"] = 0.9            # error: alone, then back
    returns.loc[index[71], "a"] = -0.9
    returns.loc[index[85], ["a", "b"]] = 0.12    # event: confirmed by b
    returns.loc[index[92], "a"] = 0.10           # alone, does not reverse
    return returns


TESTS = [
    {"name": "Toy: an error and its bounce, a confirmed event, an unexplained move", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"returns": toy(), "series": "a"}},
    {"name": "RBOB 2017-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"returns": product_returns(), "series": "rbob"}},
    {"name": "ULSD 2017-2019", "origin": "extra",
     "args": lambda: {"returns": product_returns(), "series": "ulsd"}},
]
