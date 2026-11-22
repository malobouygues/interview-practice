import numpy as np
import pandas as pd


def outlier_scores(returns: pd.Series) -> pd.DataFrame:
    r = returns.dropna()
    scores = pd.DataFrame(index=r.index)
    scores["return"] = r

    # 1. classic z-score: mean and standard deviation of the WHOLE sample (contaminated by outliers)
    scores["z"] = (r - r.mean()) / r.std()

    # 2. modified z-score: median and MAD, robust to the outliers themselves
    median = r.median()
    mad = (r - median).abs().median()
    scores["modified_z"] = 0.6745 * (r - median) / mad

    # 3. IQR rule (box plot): outside [Q1 - 1.5 IQR, Q3 + 1.5 IQR]
    q1 = r.quantile(0.25)
    q3 = r.quantile(0.75)
    iqr = q3 - q1
    scores["iqr_outlier"] = (r < q1 - 1.5 * iqr) | (r > q3 + 1.5 * iqr)

    # 4. rolling modified z: median and MAD of the 60 PREVIOUS days only (usable in real time)
    rolling_median = r.rolling(60, min_periods=30).median().shift(1)
    deviation = (r - rolling_median).abs()
    rolling_mad = deviation.rolling(60, min_periods=30).median().shift(1)
    scores["rolling_modified_z"] = 0.6745 * (r - rolling_median) / rolling_mad
    return scores
