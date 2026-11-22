FUNCTION = "price_quote"

PARAMS = {"soft_frac": 0.6, "base_limit": 1000, "skew_coeff": 0.001}
ADVISED = "Test recommandé par le corrigé (données reconstituées)."


def case(inventory, side, quantity, reference=100.0, half_spread=0.05, asset="Asset_X"):
    return lambda: {"params": dict(PARAMS),
                    "request": {"side": side, "asset": asset, "quantity": quantity,
                                "reference": reference, "half_spread": half_spread},
                    "inventory": dict(inventory), "liquidity_score": 0.7}


TESTS = [
    {"name": "Flat book, BUY (the easy case)", "origin": "extra",
     "args": case({}, "BUY", 100), "expected": {"quote": 100.05, "action": "accept"}},
    {"name": "Flat book, SELL", "origin": "extra",
     "args": case({}, "SELL", 100), "expected": {"quote": 99.95, "action": "accept"}},
    {"name": "Long inventory pulls ask and bid down", "origin": "rebuilt", "note": ADVISED,
     "args": case({"Asset_X": 200}, "SELL", 100),
     "expected": {"quote": 99.75, "action": "accept"}},
    {"name": "Short inventory pulls the quote up", "origin": "extra",
     "args": case({"Asset_X": -200}, "BUY", 100),
     "expected": {"quote": 100.25, "action": "accept"}},
    {"name": "Under the soft limit now, above it after the trade: widen", "origin": "rebuilt",
     "note": ADVISED,
     "args": case({"Asset_X": 550}, "BUY", 100),
     "expected": {"quote": 99.55, "action": "widen"}},
    {"name": "Projected position lands exactly on the cap: reject", "origin": "rebuilt",
     "note": ADVISED,
     "args": case({"Asset_X": 900}, "BUY", 100),
     "expected": {"quote": None, "action": "reject"}},
    {"name": "Trade jumps over the cap from below the soft limit", "origin": "extra",
     "args": case({"Asset_X": 500}, "BUY", 600),
     "expected": {"quote": None, "action": "reject"}},
    {"name": "Loaded book, but the trade reduces it: accept", "origin": "extra",
     "args": case({"Asset_X": 700}, "SELL", 200),
     "expected": {"quote": 99.25, "action": "accept"}},
    {"name": "Projected position exactly on the soft limit: accept", "origin": "extra",
     "args": case({"Asset_X": 500}, "BUY", 100),
     "expected": {"quote": 99.55, "action": "accept"}},
    {"name": "Short side: lands exactly on the cap", "origin": "extra",
     "args": case({"Asset_X": -950}, "SELL", 50),
     "expected": {"quote": None, "action": "reject"}},
    {"name": "Short side: widen with the skew pulling up", "origin": "extra",
     "args": case({"Asset_X": -600}, "SELL", 100),
     "expected": {"quote": 100.5, "action": "widen"}},
    {"name": "Asset with no inventory entry is flat", "origin": "extra",
     "args": case({"Asset_Y": 5000}, "BUY", 100),
     "expected": {"quote": 100.05, "action": "accept"}},
    {"name": "Rounding to 4 dp", "origin": "extra",
     "args": case({"Asset_X": 123}, "BUY", 10, reference=100.12345, half_spread=0.01234),
     "expected": {"quote": 100.0128, "action": "accept"}},
]
