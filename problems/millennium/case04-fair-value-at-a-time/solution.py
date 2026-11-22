import pandas as pd

def reference_price(prices: pd.DataFrame, asset: str, ts, max_staleness_minutes: float) -> dict:
    ts = pd.to_datetime(ts)

    s = prices[["timestamp", asset]].copy()
    s["timestamp"] = pd.to_datetime(s["timestamp"])

    # on ne garde que les prints réellement exploitables
    s = s[s[asset].notna() & (s[asset] > 0)]
    s = s.sort_values("timestamp", kind="mergesort")

    # dernière barre à ou avant ts (side="right" inclut l'égalité exacte)
    pos = s["timestamp"].searchsorted(ts, side="right") - 1
    if pos < 0:
        return {"price": None}

    last_ts = s["timestamp"].iloc[pos]
    staleness = (ts - last_ts).total_seconds() / 60.0
    if staleness > max_staleness_minutes:
        return {"price": None}

    return {"price": float(s[asset].iloc[pos])}
