import pandas as pd

def clean_prices(prices: pd.DataFrame) -> pd.DataFrame:
    df = prices.copy()
    df = df.drop_duplicates()
    df = df.sort_values("timestamp", kind="mergesort")
    df = df.reset_index(drop=True)

    assets = [c for c in df.columns if c != "timestamp"]

    # un prix <= 0 n'est pas un prix : on le traite comme manquant
    df[assets] = df[assets].mask(df[assets] <= 0)

    # on reporte le dernier bon prix ; jamais de back-fill (ce serait du futur)
    df[assets] = df[assets].ffill()

    return df
