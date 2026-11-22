import numpy as np
import pandas as pd


def correlation_report(prices: pd.DataFrame, a: str, b: str) -> dict:
    la, lb = np.log(prices[a]), np.log(prices[b])
    ra, rb = la.diff(), lb.diff()          # daily log returns (first row NaN, dropped pairwise by corr)
    return {
        "pearson_levels": float(la.corr(lb)),
        "spearman_levels": float(la.corr(lb, method="spearman")),
        "pearson_returns": float(ra.corr(rb)),
        "spearman_returns": float(ra.corr(rb, method="spearman")),
    }
