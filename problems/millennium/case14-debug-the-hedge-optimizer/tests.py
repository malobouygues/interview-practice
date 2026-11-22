FUNCTION = "hedge_optimizer"

CALM = [
    [100.0, 50.0, 20.0], [100.5, 50.1, 20.3], [100.2, 50.3, 20.1], [101.0, 50.2, 20.6],
    [100.7, 50.6, 20.4], [101.5, 50.5, 20.9], [101.2, 50.9, 20.6], [102.0, 50.8, 21.2],
    [101.6, 51.2, 20.9], [102.3, 51.0, 21.4],
]
CHOPPY = [
    [100.0, 50.0, 20.0], [104.0, 49.0, 21.5], [99.0, 52.0, 19.4], [107.0, 50.0, 22.6],
    [101.0, 54.0, 20.1], [110.0, 51.0, 23.8], [103.0, 55.0, 21.0], [112.0, 52.0, 24.9],
    [105.0, 57.0, 21.9], [115.0, 54.0, 26.0],
]
WILD = [
    [100.0, 50.0, 20.0], [110.0, 46.0, 25.0], [95.0, 53.0, 17.0], [112.0, 47.0, 27.0],
    [98.0, 55.0, 18.0], [118.0, 49.0, 29.0], [101.0, 58.0, 19.0], [121.0, 50.0, 31.0],
]


def serialised(history):
    return {"columns": ["timestamp", "Asset_1", "Asset_2", "Asset_3"],
            "data": [["2024-01-02 09:%02d:00" % i] + list(row) for i, row in enumerate(history)]}


def case(history, inventory):
    return lambda: {"prices": serialised(history), "inventory": dict(inventory)}


TESTS = [
    {"name": "Empty Asset_3 position: nothing to hedge", "origin": "source",
     "note": "Règle 7 du spec ; le résultat ne dépend pas de prices.",
     "args": case(CALM, {"Asset_1": 0, "Asset_2": 0, "Asset_3": 0}),
     "expected": {"hedge": {"Asset_1": 0.0, "Asset_2": 0.0}, "residual_variance": 0.0}},
    {"name": "Long book", "origin": "extra",
     "args": case(CALM, {"Asset_1": 0, "Asset_2": 0, "Asset_3": 1000})},
    {"name": "Short book", "origin": "extra",
     "args": case(CALM, {"Asset_1": 0, "Asset_2": 0, "Asset_3": -750})},
    {"name": "Mixed book: only Asset_3 drives the sizing", "origin": "extra",
     "args": case(CALM, {"Asset_1": 300, "Asset_2": -200, "Asset_3": 500})},
    {"name": "Different price history, long", "origin": "extra",
     "args": case(CHOPPY, {"Asset_1": 0, "Asset_2": 0, "Asset_3": 100})},
    {"name": "Different price history, short", "origin": "extra",
     "args": case(CHOPPY, {"Asset_1": 50, "Asset_2": 50, "Asset_3": -40})},
    {"name": "Volatile history: the residual variance is visible at 4 dp", "origin": "extra",
     "args": case(WILD, {"Asset_1": 0, "Asset_2": 0, "Asset_3": 10})},
]
