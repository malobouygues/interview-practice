import pandas as pd

def minmax(s):
    if s.max() == s.min():
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / (s.max() - s.min())

def liquidity_scores(prices: pd.DataFrame, requests: pd.DataFrame) -> dict:
    assets = [c for c in prices.columns if c != "timestamp"]

    vol = prices[assets].pct_change().std()

    share = requests["asset"].value_counts(normalize=True)
    freq = share.reindex(assets, fill_value=0.0)     # never requested = 0, not missing

    vol_norm = minmax(vol)
    freq_norm = minmax(freq)

    scores = 0.1 + 0.9 * (0.5 * (1 - vol_norm) + 0.5 * freq_norm)
    return {a: round(scores[a], 6) for a in assets}
