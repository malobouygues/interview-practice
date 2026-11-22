import pandas as pd

FUNCTION = "track_book"


def fills(*rows):
    return pd.DataFrame(list(rows), columns=["asset", "side", "quantity", "fill_price"])


def marks(asset_1=(99.8, 99.9, 100.0), asset_2=(50.2, 50.1, 50.0), asset_3=(19.0, 19.5, 20.0)):
    return pd.DataFrame({
        "timestamp": ["2024-01-02 09:00:00", "2024-01-02 09:01:00", "2024-01-02 09:02:00"],
        "Asset_1": list(asset_1), "Asset_2": list(asset_2), "Asset_3": list(asset_3),
    })


TESTS = [
    {"name": "Sample: BUY 100 @100.05 then SELL 100 @99.95, marks at 100", "origin": "source",
     "note": "cash et pnl sont coupés dans le book ; valeurs données par le corrigé (10.0 / 10.0).",
     "args": lambda: {"filled_requests": fills(("Asset_1", "BUY", 100, 100.05),
                                               ("Asset_1", "SELL", 100, 99.95)),
                      "prices": marks()},
     "expected": {"inventory": {"Asset_1": 0, "Asset_2": 0, "Asset_3": 0},
                  "cash": 10.0, "pnl": 10.0}},
    {"name": "No fills: the book is flat", "origin": "rebuilt",
     "note": "Cas prévu par l'énoncé (filled_requests may be empty) ; données reconstituées.",
     "args": lambda: {"filled_requests": fills(), "prices": marks()},
     "expected": {"inventory": {"Asset_1": 0, "Asset_2": 0, "Asset_3": 0},
                  "cash": 0.0, "pnl": 0.0}},
    {"name": "Client BUY leaves the maker short", "origin": "extra",
     "args": lambda: {"filled_requests": fills(("Asset_1", "BUY", 100, 100.05)),
                      "prices": marks()},
     "expected": {"inventory": {"Asset_1": -100, "Asset_2": 0, "Asset_3": 0},
                  "cash": 10005.0, "pnl": 5.0}},
    {"name": "Client SELL leaves the maker long", "origin": "extra",
     "args": lambda: {"filled_requests": fills(("Asset_3", "SELL", 500, 19.9)),
                      "prices": marks()},
     "expected": {"inventory": {"Asset_1": 0, "Asset_2": 0, "Asset_3": 500},
                  "cash": -9950.0, "pnl": 50.0}},
    {"name": "Several assets, several fills", "origin": "extra",
     "args": lambda: {"filled_requests": fills(("Asset_1", "BUY", 200, 100.10),
                                               ("Asset_2", "SELL", 300, 49.90),
                                               ("Asset_3", "BUY", 1000, 20.50),
                                               ("Asset_1", "SELL", 50, 99.90),
                                               ("Asset_2", "SELL", 100, 49.80)),
                      "prices": marks()},
     "expected": {"inventory": {"Asset_1": -150, "Asset_2": 400, "Asset_3": -1000},
                  "cash": 15575.0, "pnl": 575.0}},
    {"name": "Inventory is marked at the last row of prices", "origin": "extra",
     "args": lambda: {"filled_requests": fills(("Asset_2", "SELL", 100, 50.0)),
                      "prices": marks(asset_2=(48.0, 49.0, 51.0))},
     "expected": {"inventory": {"Asset_1": 0, "Asset_2": 100, "Asset_3": 0},
                  "cash": -5000.0, "pnl": 100.0}},
    {"name": "Rounding to 6 dp", "origin": "extra",
     "args": lambda: {"filled_requests": fills(("Asset_1", "BUY", 3, 100.1234567),
                                               ("Asset_1", "SELL", 7, 99.9876543)),
                      "prices": marks()}},
]
