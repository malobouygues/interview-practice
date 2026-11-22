FUNCTION = "quote_stream_with_impact"

SAMPLE = {'half_spread': 0.1, 'k': 2e-5, 'decay': 0.9}
TIGHT = {"tol": 0, "abs_tol": 5e-10}      # quotes are rounded to 9 dp


def reqs(*pairs):
    return [{"side": side, "quantity": qty} for side, qty in pairs]


def case(reference, requests, score, params):
    return lambda: {"reference": reference, "requests_for_asset": [dict(r) for r in requests],
                    "liquidity_score": score, "impact_params": dict(params)}


TESTS = [
    dict(TIGHT, name="Sample: three BUYs of 2500 on an illiquid asset", origin="source",
         args=case(20.0, reqs(("BUY", 2500)) * 3, 0.0, SAMPLE),
         expected=[20.1, 20.145000045, 20.185500086]),
    dict(TIGHT, name="Three SELLs push the quotes down", origin="extra",
         args=case(20.0, reqs(("SELL", 2500)) * 3, 0.0, SAMPLE),
         expected=[19.9, 19.854999955, 19.814499914]),
    dict(TIGHT, name="Single request carries no impact", origin="extra",
         args=case(100.0, reqs(("SELL", 10000)), 0.3, SAMPLE),
         expected=[99.9]),
    dict(TIGHT, name="Mixed BUY / SELL sequence", origin="extra",
         args=case(100.0, reqs(("BUY", 1000), ("SELL", 500), ("BUY", 2000), ("SELL", 4000),
                               ("SELL", 100)), 0.5,
                   {'half_spread': 0.05, 'k': 1e-5, 'decay': 0.8})),
    dict(TIGHT, name="No 'decay' key: impact does not fade", origin="extra",
         args=case(50.0, reqs(("BUY", 1000)) * 4, 0.2, {'half_spread': 0.02, 'k': 1e-5})),
    dict(TIGHT, name="Perfectly liquid asset barely moves (the 1e-6 term)", origin="extra",
         args=case(100.0, reqs(("BUY", 10000), ("BUY", 10000), ("SELL", 10000)), 1.0,
                   {'half_spread': 0.05, 'k': 1e-5, 'decay': 0.9})),
    dict(TIGHT, name="Order matters: big SELL first, then BUYs", origin="extra",
         args=case(20.0, reqs(("SELL", 5000), ("BUY", 2500), ("BUY", 2500)), 0.1, SAMPLE)),
    dict(TIGHT, name="No requests", origin="extra",
         args=case(20.0, [], 0.0, SAMPLE), expected=[]),
]
