import pandas as pd


def build_features(cracks: pd.DataFrame) -> pd.DataFrame:
    # Forecast origin: the MORNING of day t, before day t's settlement.
    # Information set: settlements up to t-1 -> every market feature is shifted by one day.
    crack = cracks["diesel_crack"]
    change = crack.diff()                          # what we want to explain: today's change, USD/bbl
    gasoil_change = cracks["gasoil_crack"].diff()

    features = pd.DataFrame(index=cracks.index)
    features["crack_change"] = change                                     # the target y_t (not a feature)

    # persistence: yesterday's move
    features["change_lag1"] = change.shift(1)

    # recent drift and recent volatility of the crack (20 business days ~ one month)
    features["mean_change_20"] = change.rolling(20).mean().shift(1)
    features["vol_change_20"] = change.rolling(20).std().shift(1)

    # stretch: how far yesterday's crack is from its 60-day average (mean reversion)
    average_60 = crack.rolling(60).mean()
    features["gap_to_mean_60"] = (crack - average_60).shift(1)

    # transatlantic link: rolling correlation of US diesel and European gasoil cracks
    features["corr_gasoil_60"] = change.rolling(60).corr(gasoil_change).shift(1)

    # calendar: known in advance, no shift needed
    features["month"] = cracks.index.month
    features["heating_season"] = cracks.index.month.isin([11, 12, 1, 2, 3]).astype(int)
    return features
