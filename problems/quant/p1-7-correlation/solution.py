import pandas as pd


def correlation_report(prices: pd.DataFrame, a: str, b: str) -> dict:
    levels_a = prices[a]
    levels_b = prices[b]

    # daily changes in USD/bbl: defined even when a price is negative (log returns are not)
    changes_a = levels_a.diff()
    changes_b = levels_b.diff()

    return {
        "pearson_levels": float(levels_a.corr(levels_b)),
        "spearman_levels": float(levels_a.corr(levels_b, method="spearman")),
        "pearson_changes": float(changes_a.corr(changes_b)),
        "spearman_changes": float(changes_a.corr(changes_b, method="spearman")),
    }
