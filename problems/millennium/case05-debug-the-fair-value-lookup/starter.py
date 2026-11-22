import pandas as pd
import numpy as np

def fair_value_at(ts, asset, prices, max_staleness_minutes):
    df = prices.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    query_ts = pd.to_datetime(ts)

    # Bars strictly before the query time.
    eligible = df[df['timestamp'] < query_ts]
    if eligible.empty:
        return {"price": None}

    # Walk back to the most recent bar that actually has a price.
    chosen = None
    for _, row in eligible.iloc[::-1].iterrows():
        val = row[asset]
        if val is not None and not pd.isna(val):
            chosen = row
            break

    if chosen is None:
        return {"price": None}

    return {"price": float(chosen[asset])}
