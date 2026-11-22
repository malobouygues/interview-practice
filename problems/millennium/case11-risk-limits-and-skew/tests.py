FUNCTION = "decide_request"

PARAMS = {'base_limit': 50000, 'soft_frac': 0.6, 'skew_coeff': 0.0001}


def case(inventory, side, quantity, score, asset="Asset_1", reference=100.0, half_spread=0.05):
    return lambda: {"inventory": dict(inventory),
                    "request": {"asset": asset, "side": side, "quantity": quantity,
                                "reference": reference, "half_spread": half_spread},
                    "liquidity_score": score, "params": dict(PARAMS)}


TESTS = [
    {"name": "Sample: flat book, client BUY 100", "origin": "rebuilt",
     "note": "Sample du book ; reference et half_spread y sont coupés : 100.0 et 0.05, "
             "seules valeurs cohérentes avec la quote attendue 100.05.",
     "args": case({'Asset_1': 0}, "BUY", 100, 1.0),
     "expected": {"action": "accept", "quote": 100.05}},
    {"name": "Flat book, client SELL 100", "origin": "extra",
     "args": case({'Asset_1': 0}, "SELL", 100, 1.0),
     "expected": {"action": "accept", "quote": 99.95}},
    {"name": "Projected position beyond the soft limit: widen", "origin": "extra",
     "args": case({'Asset_1': -29950}, "BUY", 100, 1.0),
     "expected": {"action": "widen", "quote": 103.095}},
    {"name": "Projected position beyond the hard limit: reject", "origin": "extra",
     "args": case({'Asset_1': 4950}, "SELL", 100, 0.1),
     "expected": {"action": "reject", "quote": None}},
    {"name": "Exactly on the hard limit is still quoted (strict >)", "origin": "extra",
     "args": case({'Asset_1': 4900}, "SELL", 100, 0.1),
     "expected": {"action": "widen", "quote": 99.41}},
    {"name": "Exactly on the soft limit is accepted (strict >)", "origin": "extra",
     "args": case({'Asset_1': 2900}, "SELL", 100, 0.1),
     "expected": {"action": "accept", "quote": 99.66}},
    {"name": "Asset missing from inventory counts as 0", "origin": "extra",
     "args": case({'Asset_2': 40000}, "BUY", 100, 0.1, asset="Asset_3", reference=20.0,
                  half_spread=0.1),
     "expected": {"action": "accept", "quote": 20.1}},
    {"name": "Long inventory pulls the ask down", "origin": "extra",
     "args": case({'Asset_1': 10000}, "BUY", 500, 1.0),
     "expected": {"action": "accept", "quote": 99.05}},
    {"name": "Same trade on an illiquid asset is rejected", "origin": "extra",
     "args": case({'Asset_1': 10000}, "BUY", 500, 0.1),
     "expected": {"action": "reject", "quote": None}},
    {"name": "Trade that brings the book back under the soft limit", "origin": "extra",
     "args": case({'Asset_1': 31000}, "BUY", 2000, 1.0),
     "expected": {"action": "accept", "quote": 96.95}},
    {"name": "Short inventory pulls the bid up, widened", "origin": "extra",
     "args": case({'Asset_1': -40000}, "BUY", 1000, 1.0),
     "expected": {"action": "widen", "quote": 104.1}},
    {"name": "Rounding to 6 dp", "origin": "extra",
     "args": case({'Asset_1': 123}, "SELL", 10, 1.0, reference=100.1234567,
                  half_spread=0.0123456)},
]
