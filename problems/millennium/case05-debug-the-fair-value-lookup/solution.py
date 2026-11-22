import pandas as pd

def fair_value_at(ts, asset, prices, max_staleness_minutes):
    df = prices.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    query_ts = pd.to_datetime(ts)

    # la série n'est pas garantie triée : on la remet dans le temps
    df = df.sort_values('timestamp', kind='mergesort')

    # barres à ou avant ts (règle 1 + règle 5), en sautant les nulls (règle 2)
    eligible = df[(df['timestamp'] <= query_ts) & df[asset].notna()]

    # règle 4 : rien avant le premier print
    if eligible.empty:
        return {"price": None}

    last = eligible.iloc[-1]

    # règle 3 : exactement max_staleness_minutes reste acceptable
    staleness = (query_ts - last['timestamp']).total_seconds() / 60.0
    if staleness > max_staleness_minutes:
        return {"price": None}

    return {"price": float(last[asset])}
