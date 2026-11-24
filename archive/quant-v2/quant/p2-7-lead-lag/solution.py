import pandas as pd


def lead_lag_table(x: pd.Series, y: pd.Series, max_lag: int) -> pd.Series:
    # corr(x_{t-k}, y_t): for k > 0, x moved k days BEFORE y
    correlations = {}
    for k in range(-max_lag, max_lag + 1):
        correlations[k] = x.shift(k).corr(y)

    table = pd.Series(correlations, name="corr")
    table.index.name = "lag"
    return table
