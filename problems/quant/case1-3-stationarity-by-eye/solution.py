import numpy as np
import pandas as pd


def subsample_stats(x: pd.Series, parts: int = 4) -> dict:
    values = x.dropna().to_numpy(dtype=float)
    blocks = np.array_split(values, parts)          # consecutive blocks, in time order
    means = [float(b.mean()) for b in blocks]
    stds = [float(b.std(ddof=1)) for b in blocks]
    return {
        "means": means,
        "stds": stds,
        # how far apart the block means are, in units of the typical within-block std
        "mean_shift": (max(means) - min(means)) / float(np.mean(stds)),
        # how unequal the dispersion is across blocks
        "std_ratio": max(stds) / min(stds),
    }
