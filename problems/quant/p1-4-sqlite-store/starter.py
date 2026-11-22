import sqlite3

import pandas as pd


def monthly_spreads_sql(prices: pd.DataFrame) -> pd.DataFrame:
    """Columns: month, brent_wti, brent_dubai, n_days (one row per month)."""
    raise NotImplementedError("create the table, load twice, query")
