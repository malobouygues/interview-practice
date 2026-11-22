FUNCTION = "quote_request"

NOISE = ("Prix déjà sur la grille : le bruit flottant ne doit pas ajouter un tick "
         "(point du corrigé : round(raw / tick_size, 9) avant ceil / floor).")


def case(reference, half_spread, side, quantity, k, tick):
    return lambda: {"reference": reference, "half_spread": half_spread, "side": side,
                    "quantity": quantity, "size_params": {"k": k}, "tick_size": tick}


TESTS = [
    {"name": "Sample: client BUY → ask, rounded up", "origin": "source",
     "args": case(100.0, 0.05, 'BUY', 100, 1e-5, 0.01), "expected": 100.06},
    {"name": "Sample: client SELL → bid, rounded down", "origin": "source",
     "args": case(100.0, 0.05, 'SELL', 100, 1e-5, 0.01), "expected": 99.94},
    {"name": "Bigger size worsens the ask (tick 0.05)", "origin": "extra",
     "args": case(50.0, 0.02, 'BUY', 5000, 1e-5, 0.05), "expected": 50.1},
    {"name": "Bigger size worsens the bid (tick 0.05)", "origin": "extra",
     "args": case(50.0, 0.02, 'SELL', 5000, 1e-5, 0.05), "expected": 49.9},
    {"name": "Coarse tick of 0.5, SELL", "origin": "extra",
     "args": case(20.0, 0.1, 'SELL', 1000, 2e-4, 0.5), "expected": 19.5},
    {"name": "No size penalty, tick of 1", "origin": "extra",
     "args": case(99.4, 0.3, 'BUY', 10, 0.0, 1.0), "expected": 100.0},
    {"name": "Ask already on the grid stays there", "origin": "extra", "note": NOISE,
     "args": case(100.0, 0.04, 'BUY', 1000, 1e-5, 0.01), "expected": 100.05},
    {"name": "Bid already on the grid stays there", "origin": "extra", "note": NOISE,
     "args": case(100.0, 0.04, 'SELL', 1000, 1e-5, 0.01), "expected": 99.95},
]
