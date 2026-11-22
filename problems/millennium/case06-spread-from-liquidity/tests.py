FUNCTION = "half_spread"

PARAMS = {'base': 0.01, 'k_vol': 2.0, 'k_liq': 0.05, 'min_half_spread': 0.02}
REBUILT = ("Appel du Sample I/O du book ; les valeurs de params y sont coupées, "
           "elles sont reconstituées ici.")


def case(score, vol, params=None):
    return lambda: {"liquidity_score": score, "volatility": vol,
                    "params": dict(params or PARAMS)}


TESTS = [
    {"name": "half_spread(1.0, 0.001, ...) — liquid and calm: the floor applies",
     "origin": "rebuilt", "note": REBUILT,
     "args": case(1.0, 0.001), "expected": 0.02},
    {"name": "half_spread(0.0, 0.08, ...) — illiquid and volatile",
     "origin": "rebuilt", "note": REBUILT,
     "args": case(0.0, 0.08), "expected": 0.22},
    {"name": "Mid liquidity", "origin": "extra",
     "args": case(0.5, 0.01), "expected": 0.055},
    {"name": "Wider when volatility rises", "origin": "extra",
     "args": case(0.8, 0.05), "expected": 0.12},
    {"name": "Raw spread exactly on the floor", "origin": "extra",
     "args": case(1.0, 0.005), "expected": 0.02},
    {"name": "Floor dominates when everything is zero", "origin": "extra",
     "args": case(1.0, 0.0, {'base': 0.0, 'k_vol': 1.0, 'k_liq': 1.0, 'min_half_spread': 0.005}),
     "expected": 0.005},
    {"name": "Integer params still give a float", "origin": "extra",
     "args": case(0.5, 0.0, {'base': 1, 'k_vol': 3, 'k_liq': 2, 'min_half_spread': 0}),
     "expected": 2.0},
]
