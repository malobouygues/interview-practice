import numpy as np
import pandas as pd


def treat_gaps(products: pd.DataFrame) -> dict:
    # 1. one row per date (drop_duplicates() would ignore the date index and could
    #    delete two different holidays whose rows are both entirely empty)
    prices = products[~products.index.duplicated(keep="first")]
    prices = prices.sort_index()
    prices = prices.copy()

    # 2. stale feed: 4 or more identical consecutive prices -> keep the first, the rest are missing
    for column in prices.columns:
        series = prices[column]
        same_as_previous = series == series.shift(1)
        run_id = (~same_as_previous).cumsum()                     # a new run starts when the price changes
        run_length = series.groupby(run_id).transform("count")
        stale = same_as_previous & (run_length >= 4)
        prices.loc[stale, column] = np.nan

    # 3. short interior gaps (holidays, a lost day): carry the last price for at most 2 days.
    #    Never backward-fill (that uses the future), never fill before the first or after the last price.
    treated = prices.ffill(limit=2, limit_area="inside")

    filled = prices.isna() & treated.notna()                       # trace every imputed value
    return {"prices": treated, "filled": filled}
