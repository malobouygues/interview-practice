FUNCTION = "quote_impact_stream"

TIGHT = {"tol": 0, "abs_tol": 5e-10}      # quotes are rounded to 9 dp


def reqs(*pairs):
    return [{"side": side, "quantity": qty} for side, qty in pairs]


def case(reference, k, decay, half_spread, score, requests):
    return lambda: {"reference": reference,
                    "impact_params": {"k": k, "decay": decay, "half_spread": half_spread},
                    "liquidity_score": score,
                    "requests_for_asset": [dict(r) for r in requests]}


TESTS = [
    dict(TIGHT, name="Worked example: three BUYs of 100", origin="source",
         args=case(200.0, 0.01, 0.5, 0.0, 0.0, reqs(("BUY", 100)) * 3),
         expected=[200.0, 200.5, 200.75]),
    dict(TIGHT, name="Single BUY: one half-spread, no impact", origin="extra",
         args=case(100.0, 0.001, 0.9, 0.05, 0.5, reqs(("BUY", 100))),
         expected=[100.05]),
    dict(TIGHT, name="Single SELL: one half-spread, no impact", origin="extra",
         args=case(100.0, 0.001, 0.9, 0.05, 0.5, reqs(("SELL", 100))),
         expected=[99.95]),
    dict(TIGHT, name="liquidity_score = 1: quotes are reference ± half_spread", origin="rebuilt",
         note="Test recommandé par le corrigé et par les notes de l'énoncé (données reconstituées).",
         args=case(100.0, 0.01, 0.5, 0.05, 1.0, reqs(("BUY", 100), ("SELL", 200), ("BUY", 300))),
         expected=[100.05, 99.95, 100.05]),
    dict(TIGHT, name="Liquidity scales the impact (score 0.5)", origin="extra",
         args=case(200.0, 0.01, 0.5, 0.0, 0.5, reqs(("BUY", 100)) * 3),
         expected=[200.0, 200.25, 200.375]),
    dict(TIGHT, name="Mixed BUY / SELL sequence", origin="rebuilt",
         note="Test recommandé par le corrigé (données reconstituées).",
         args=case(50.0, 0.002, 0.8, 0.02, 0.25,
                   reqs(("BUY", 500), ("SELL", 1000), ("SELL", 200), ("BUY", 800), ("BUY", 100)))),
    dict(TIGHT, name="decay = 1: impact accumulates without fading", origin="rebuilt",
         note="Test recommandé par le corrigé (données reconstituées).",
         args=case(100.0, 0.001, 1.0, 0.01, 0.0, reqs(("BUY", 100)) * 4),
         expected=[100.01, 100.11, 100.21, 100.31]),
    dict(TIGHT, name="Long run of BUYs: the state converges, it does not drift", origin="extra",
         args=case(200.0, 0.01, 0.5, 0.0, 0.0, reqs(("BUY", 100)) * 8)),
    dict(TIGHT, name="No requests", origin="extra",
         args=case(100.0, 0.01, 0.5, 0.05, 0.0, []), expected=[]),
]
