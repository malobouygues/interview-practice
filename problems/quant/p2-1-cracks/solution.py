import numpy as np
import pandas as pd

USD_PER_BBL_FACTOR = {"USD/bbl": 1.0, "USD/gal": 42.0, "USc/gal": 0.42}   # 42 gallons per barrel
BARRELS_PER_TONNE = {"gasoil": 7.45, "jet": 7.88}                          # density, product by product


def build_daily_table(raw):
    prices = raw.copy()
    prices["date"] = pd.to_datetime(prices["date"])

    # 1. a row sent twice is dropped; after that the key (date, product) must be unique
    prices = prices.drop_duplicates()
    assert not prices.duplicated(subset=["date", "product"]).any(), "two different prices for one date/product"

    # 2. every price to USD/bbl, row by row, with the unit written on that row
    factor = prices["unit"].map(USD_PER_BBL_FACTOR)
    per_tonne = prices["unit"] == "USD/t"
    factor[per_tonne] = 1 / prices.loc[per_tonne, "product"].map(BARRELS_PER_TONNE)
    assert factor.notna().all(), "a unit without a conversion factor"
    prices["usd_bbl"] = prices["price"] * factor

    # 3. long -> wide: one row per date, one column per product (a gap becomes NaN)
    wide = prices.pivot(index="date", columns="product", values="usd_bbl")
    wide = wide[["brent", "gasoil", "ulsd", "rbob", "jet"]]

    # 4. frozen feed: 4+ identical settlements in a row -> keep the first, blank the copies
    for product in wide.columns:
        series = wide[product]
        same_as_previous = series == series.shift(1)
        run_id = (~same_as_previous).cumsum()
        run_length = series.groupby(run_id).transform("count")
        frozen = same_as_previous & (run_length >= 4)
        wide.loc[frozen, product] = np.nan

    # 5. cracks against Brent, only where both prices exist (no filling)
    for product in ["gasoil", "ulsd", "rbob", "jet"]:
        wide[product + "_crack"] = wide[product] - wide["brent"]
    return wide
