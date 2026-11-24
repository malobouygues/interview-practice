import pandas as pd

MARKET_TZ = "Europe/Paris"


def load_market_hours(path):
    """One row per delivery hour, indexed by its UTC start, latest version of each record."""
    raw = pd.read_csv(path)
    raise NotImplementedError("parse to UTC, drop copies, keep the latest version, add local labels")
