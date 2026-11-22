import pandas as pd


def quality_checks(prices: pd.DataFrame) -> pd.DataFrame:
    flags = []

    # Rule 1: Brent and Dubai cannot be zero or negative -> data error
    for series in ["brent", "dubai"]:
        bad = prices[series] <= 0
        for date, value in prices.loc[bad, series].items():
            flags.append([date, series, value, "non-positive price", "set to NaN"])

    # Rule 2: a negative WTI is possible (front-month expiry squeeze) -> keep it, but document it
    negative = prices["wti"] <= 0
    for date, value in prices.loc[negative, "wti"].items():
        flags.append([date, "wti", value, "negative WTI print", "keep and document"])

    # Rule 3: Brent or Dubai more than doubles or halves versus its own recent level
    # (median of the 5 previous valid prices: only past information, robust to a single bad print)
    for series in ["brent", "dubai"]:
        valid = prices[series].dropna()
        recent_level = valid.rolling(5, min_periods=3).median().shift(1)
        ratio = valid / recent_level
        jump = (ratio > 2) | (ratio < 0.5)
        for date, value in valid[jump].items():
            flags.append([date, series, value, "jump vs last 5 days", "set to NaN"])

    report = pd.DataFrame(flags, columns=["date", "series", "value", "issue", "action"])
    report = report.sort_values(["date", "series"])
    report = report.reset_index(drop=True)
    return report
