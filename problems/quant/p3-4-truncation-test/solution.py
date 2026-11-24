import pandas as pd


def truncation_test(build_features, stocks, prices, cutoff):
    cutoff = pd.Timestamp(cutoff, tz="UTC")

    # 1. features built from everything the database contains today
    full = build_features(stocks, prices)

    # 2. the database as it looked at the cutoff: reports published by then, prices settled by then
    stocks_then = stocks[stocks["available_at"] <= cutoff]
    prices_then = prices[pd.to_datetime(prices["date"]) <= cutoff.tz_localize(None)]
    truncated = build_features(stocks_then, prices_then)

    # 3. every row the truncated build has must be identical in the full build
    common = truncated.index
    before = full.loc[common]
    same = (before == truncated) | (before.isna() & truncated.isna())
    changed = ~same.all(axis=1)

    first_changed = None
    if changed.any():
        first_changed = changed[changed].index.min()
    return {"rows_compared": int(len(common)), "rows_changed": int(changed.sum()),
            "first_changed": first_changed}
