import pandas as pd


def load_crude_prices(path: str) -> pd.DataFrame:
    """Typed, chronological, one row per date; index = date, columns = brent, wti, dubai."""
    raise NotImplementedError("load the vendor file")
