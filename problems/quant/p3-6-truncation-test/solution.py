import numpy as np
import pandas as pd


def truncation_test(build_features, prices: pd.DataFrame, cutoff: str) -> list:
    cutoff = pd.Timestamp(cutoff)

    # 1. features computed with the complete history
    full = build_features(prices)

    # 2. features computed with only the data available up to the cutoff
    truncated = build_features(prices[prices.index <= cutoff])

    # 3. on the dates up to the cutoff, both must be identical
    full_until_cutoff = full[full.index <= cutoff]

    changed = []
    for column in full.columns:
        with_future = full_until_cutoff[column].to_numpy(dtype=float)
        without_future = truncated[column].to_numpy(dtype=float)
        if not np.allclose(with_future, without_future, equal_nan=True):
            changed.append(column)      # its past values depend on data after the cutoff: look-ahead
    return changed
