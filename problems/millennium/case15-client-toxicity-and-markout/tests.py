import pandas as pd

FUNCTION = "client_markout"


def tape():
    return pd.DataFrame({
        "timestamp": ["2024-01-02 09:%02d:00" % i for i in range(11)],
        "Asset_1": [100.0, 100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8, 100.9, 101.0],
        "Asset_2": [50.0, 49.95, 49.9, 49.85, 49.8, 49.75, 49.7, 49.65, 49.6, 49.55, 49.5],
        "Asset_3": [20.0, 20.0, 20.0, 20.2, 20.2, 20.2, 20.2, 19.8, 19.8, 19.8, 19.8],
    })


def fills(*rows):
    return pd.DataFrame(
        [(c, "2024-01-02 " + t, a, s, q, p) for c, t, a, s, q, p in rows],
        columns=["client_id", "timestamp", "asset", "side", "quantity", "fill_price"])


BOOK = (
    ("CLIENT_A", "09:00:00", "Asset_1", "BUY", 100, 100.0),
    ("CLIENT_A", "09:00:00", "Asset_2", "BUY", 200, 50.0),
    ("CLIENT_B", "09:02:00", "Asset_2", "SELL", 100, 50.0),
    ("CLIENT_B", "09:00:00", "Asset_3", "SELL", 10, 20.0),
    ("CLIENT_C", "09:03:00", "Asset_3", "BUY", 1000, 20.2),
)


def case(rows, horizon):
    return lambda: {"fills": fills(*rows), "prices": tape(), "horizon_minutes": horizon}


TESTS = [
    {"name": "Sample: Asset_1 rising, one buyer and one seller", "origin": "rebuilt",
     "note": "Sample du book ; fills et prices n'y sont pas détaillés. Données reconstituées "
             "d'après le corrigé (Asset_1 passe de 100 à 100.5 en 5 minutes, quantité 100).",
     "args": case((("CLIENT_A", "09:00:00", "Asset_1", "BUY", 100, 100.0),
                   ("CLIENT_B", "09:00:00", "Asset_1", "SELL", 100, 100.0)), 5),
     "expected": {"CLIENT_A": {"avg_markout": -50.0, "toxic": True},
                  "CLIENT_B": {"avg_markout": 50.0, "toxic": False}}},
    {"name": "Horizon runs past the end of the tape: last price", "origin": "extra",
     "args": case((("CLIENT_A", "09:08:00", "Asset_1", "BUY", 100, 100.8),), 5),
     "expected": {"CLIENT_A": {"avg_markout": -20.0, "toxic": True}}},
    {"name": "As-of lookup between two bars", "origin": "extra",
     "args": case((("CLIENT_C", "09:02:30", "Asset_1", "SELL", 50, 100.25),), 2),
     "expected": {"CLIENT_C": {"avg_markout": 7.5, "toxic": False}}},
    {"name": "Several fills per client, several assets", "origin": "extra",
     "note": "CLIENT_A : -50 et +50 → moyenne 0.0, donc pas toxique (0 n'est pas négatif).",
     "args": case(BOOK, 5),
     "expected": {"CLIENT_A": {"avg_markout": 0.0, "toxic": False},
                  "CLIENT_B": {"avg_markout": -16.5, "toxic": True},
                  "CLIENT_C": {"avg_markout": 400.0, "toxic": False}}},
    {"name": "Same fills, arriving in another order", "origin": "extra",
     "args": case((BOOK[4], BOOK[2], BOOK[0], BOOK[3], BOOK[1]), 5),
     "expected": {"CLIENT_A": {"avg_markout": 0.0, "toxic": False},
                  "CLIENT_B": {"avg_markout": -16.5, "toxic": True},
                  "CLIENT_C": {"avg_markout": 400.0, "toxic": False}}},
    {"name": "Horizon of zero: marked at the fill time", "origin": "extra",
     "args": case((("CLIENT_A", "09:02:00", "Asset_1", "BUY", 100, 100.3),
                   ("CLIENT_B", "09:02:00", "Asset_1", "SELL", 100, 100.1)), 0)},
    {"name": "Fractional horizon", "origin": "extra",
     "args": case(BOOK, 2.5)},
    {"name": "Long horizon: everything marked at the last price", "origin": "extra",
     "args": case(BOOK, 60)},
]
