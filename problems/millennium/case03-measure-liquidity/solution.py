import pandas as pd

def minmax(s):
    if s.max() == s.min():
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / (s.max() - s.min())

def liquidity_scores(prices: pd.DataFrame, requests: pd.DataFrame) -> dict:
    assets = [c for c in prices.columns if c != "timestamp"]

    vol = pd.Series({a: prices[a].pct_change().std() for a in assets})

    share = requests["asset"].value_counts(normalize=True)
    freq = pd.Series({a: share.get(a, 0.0) for a in assets})

    vol_norm = minmax(vol)
    freq_norm = minmax(freq)

    scores = 0.1 + 0.9 * (0.5 * (1 - vol_norm) + 0.5 * freq_norm)
    return {a: round(scores[a], 6) for a in assets}
