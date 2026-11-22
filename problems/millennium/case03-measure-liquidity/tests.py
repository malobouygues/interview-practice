import pandas as pd

FUNCTION = "liquidity_scores"

STABLE = [100.0, 100.01, 100.0, 100.02, 100.01, 100.02]
MEDIUM = [50.0, 50.2, 49.9, 50.3, 50.0, 50.4]
JUMPY = [20.0, 21.0, 19.5, 21.5, 19.0, 22.0]


def prices(**columns):
    n = len(next(iter(columns.values())))
    data = {"timestamp": ["2024-01-02 09:%02d:00" % i for i in range(n)]}
    data.update(columns)
    return pd.DataFrame(data)


def requests(assets):
    n = len(assets)
    return pd.DataFrame({
        "request_id": list(range(1, n + 1)),
        "timestamp": ["2024-01-02 09:%02d:30" % (i % 6) for i in range(n)],
        "asset": assets,
        "side": ["BUY" if i % 2 == 0 else "SELL" for i in range(n)],
        "quantity": [100 * (1 + i % 4) for i in range(n)],
    })


TESTS = [
    {"name": "Stable and popular vs jumpy and rare", "origin": "extra",
     "note": "Le Sample I/O du book est coupé ; ce cas reprend sa forme (Asset_1 → 1.0).",
     "args": lambda: {"prices": prices(Asset_1=STABLE, Asset_2=MEDIUM, Asset_3=JUMPY),
                      "requests": requests(["Asset_1"] * 6 + ["Asset_2"] * 3 + ["Asset_3"])}},
    {"name": "Same request flow for every asset (zero range → 0.5)", "origin": "extra",
     "args": lambda: {"prices": prices(Asset_1=STABLE, Asset_2=MEDIUM, Asset_3=JUMPY),
                      "requests": requests(["Asset_1", "Asset_2", "Asset_3"] * 2)}},
    {"name": "An asset that is never requested", "origin": "extra",
     "args": lambda: {"prices": prices(Asset_1=STABLE, Asset_2=MEDIUM, Asset_3=JUMPY),
                      "requests": requests(["Asset_1", "Asset_1", "Asset_2", "Asset_1"])}},
    {"name": "Same volatility for every asset (zero range → 0.5)", "origin": "extra",
     "args": lambda: {"prices": prices(Asset_1=MEDIUM, Asset_2=MEDIUM, Asset_3=MEDIUM),
                      "requests": requests(["Asset_3"] * 5 + ["Asset_2"] * 2 + ["Asset_1"])}},
    {"name": "Quiet price but little flow", "origin": "extra",
     "args": lambda: {"prices": prices(Asset_1=STABLE, Asset_2=MEDIUM, Asset_3=JUMPY),
                      "requests": requests(["Asset_3"] * 7 + ["Asset_2"] * 2 + ["Asset_1"])}},
    {"name": "Four assets (every non-timestamp column counts)", "origin": "extra",
     "args": lambda: {"prices": prices(Asset_1=STABLE, Asset_2=MEDIUM, Asset_3=JUMPY,
                                       Asset_4=[10.0, 10.1, 10.0, 10.2, 10.1, 10.3]),
                      "requests": requests(["Asset_1"] * 4 + ["Asset_4"] * 3 + ["Asset_2"] * 2
                                           + ["Asset_3"])}},
    {"name": "Both signals flat: every score is the midpoint", "origin": "extra",
     "args": lambda: {"prices": prices(Asset_1=MEDIUM, Asset_2=MEDIUM, Asset_3=MEDIUM),
                      "requests": requests(["Asset_1", "Asset_2", "Asset_3"])},
     "expected": {"Asset_1": 0.55, "Asset_2": 0.55, "Asset_3": 0.55}},
]
