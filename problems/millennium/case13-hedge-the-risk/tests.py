import pandas as pd

FUNCTION = "hedge_inventory"

CALM = {
    "Asset_1": [100.0, 100.5, 100.2, 101.0, 100.7, 101.5, 101.2, 102.0, 101.6, 102.3],
    "Asset_2": [50.0, 50.1, 50.3, 50.2, 50.6, 50.5, 50.9, 50.8, 51.2, 51.0],
    "Asset_3": [20.0, 20.3, 20.1, 20.6, 20.4, 20.9, 20.6, 21.2, 20.9, 21.4],
}
CHOPPY = {
    "Asset_1": [100.0, 104.0, 99.0, 107.0, 101.0, 110.0, 103.0, 112.0, 105.0, 115.0],
    "Asset_2": [50.0, 49.0, 52.0, 50.0, 54.0, 51.0, 55.0, 52.0, 57.0, 54.0],
    "Asset_3": [20.0, 21.5, 19.4, 22.6, 20.1, 23.8, 21.0, 24.9, 21.9, 26.0],
}


def prices(history):
    n = len(history["Asset_1"])
    data = {"timestamp": ["2024-01-02 09:%02d:00" % i for i in range(n)]}
    data.update(history)
    return pd.DataFrame(data)


def case(history, inventory):
    return lambda: {"prices": prices(history), "inventory": dict(inventory)}


TESTS = [
    {"name": "Sample: nothing to hedge", "origin": "source",
     "note": "Le book ne précise pas prices : avec un inventaire nul le résultat n'en dépend pas.",
     "args": case(CALM, {'Asset_1': 0, 'Asset_2': 0, 'Asset_3': 0}),
     "expected": {"hedge": {"Asset_1": 0.0, "Asset_2": 0.0}, "residual_variance": 0.0}},
    {"name": "Long the illiquid asset", "origin": "extra",
     "args": case(CALM, {'Asset_1': 0, 'Asset_2': 0, 'Asset_3': 1000})},
    {"name": "Short the illiquid asset", "origin": "extra",
     "args": case(CALM, {'Asset_1': 0, 'Asset_2': 0, 'Asset_3': -500})},
    {"name": "Mixed book: existing liquid positions are hedged too", "origin": "extra",
     "args": case(CALM, {'Asset_1': 200, 'Asset_2': -300, 'Asset_3': 800})},
    {"name": "Only liquid inventory: the hedge flattens it", "origin": "extra",
     "note": "À 4 dp, le ridge 1e-12 se voit : -499.9998 et non -500.0.",
     "args": case(CALM, {'Asset_1': 500, 'Asset_2': 250, 'Asset_3': 0})},
    {"name": "Choppier price history", "origin": "extra",
     "args": case(CHOPPY, {'Asset_1': 0, 'Asset_2': 0, 'Asset_3': 1000})},
    {"name": "Choppier history, mixed book", "origin": "extra",
     "args": case(CHOPPY, {'Asset_1': -150, 'Asset_2': 400, 'Asset_3': -600})},
]
