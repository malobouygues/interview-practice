import numpy as np
import pandas as pd

FUNCTION = "investigate_extremes"


def hand_made():
    rng = np.random.default_rng(9)
    dates = pd.bdate_range("2021-03-01", periods=60)
    base = 60 * np.exp(np.cumsum(rng.normal(0, 0.01, 60)))
    prices = pd.DataFrame({"brent": base, "gasoil": base + 15, "ulsd": base + 18, "rbob": base + 12, "jet": base + 16},
                          index=dates)
    prices.index.name = "date"
    for column in prices.columns:
        prices[column] = prices[column] * np.exp(rng.normal(0, 0.004, 60))
    prices.iloc[10, prices.columns.get_loc("rbob")] *= 100        # sent in cents
    prices.iloc[20, prices.columns.get_loc("gasoil")] = 0.0       # impossible
    prices.iloc[30:, prices.columns.get_loc("ulsd")] *= 1.25      # a squeeze, logged
    prices.iloc[40:, :] *= 0.88                                   # a crude-wide drop, not logged
    prices.iloc[50:, prices.columns.get_loc("jet")] *= 1.10       # isolated, unexplained
    prices.iloc[5, prices.columns.get_loc("brent")] = np.nan      # a holiday
    events = pd.DataFrame({"start": ["2021-04-09"], "end": ["2021-04-16"], "event": ["harbour squeeze"],
                           "markets": ["ulsd"]})
    return {"prices": prices, "events": events}


TESTS = [
    {"name": "Hand-made: a cents error, a zero, a logged squeeze, a crude-wide drop, an isolated jump",
     "origin": "extra", "args": hand_made, "check_no_mutation": True},
    {"name": "The daily product table, 2017-2023, with the desk's event log", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p2_products_wide_synthetic.csv", index_col="date", parse_dates=["date"]),
                      "events": pd.read_csv("data/p2_market_events_synthetic.csv")}},
]
