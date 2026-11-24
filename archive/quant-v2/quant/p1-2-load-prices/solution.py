import pandas as pd


def load_crude_prices(path: str) -> pd.DataFrame:
    # "HOL" = exchange holiday, "-" = value not delivered: both are missing values, not prices
    raw = pd.read_csv(path, na_values=["HOL", "-"])

    raw = raw.rename(columns={"Date": "date",
                              "Brent (USD/bbl)": "brent",
                              "WTI (USD/bbl)": "wti",
                              "Dubai (USD/bbl)": "dubai"})

    # explicit formats: 03/04/2020 is 3 April, not 4 March
    raw["date"] = pd.to_datetime(raw["date"], format="%d/%m/%Y")
    raw["loaded_at"] = pd.to_datetime(raw["loaded_at"])

    # a day loaded twice: identical rows, keep one
    prices = raw.drop_duplicates()

    # the same date sent twice with different values: the vendor corrected it, the latest load wins
    prices = prices.sort_values(["date", "loaded_at"])
    prices = prices.drop_duplicates(subset="date", keep="last")

    prices = prices.set_index("date")
    prices = prices[["brent", "wti", "dubai"]]

    assert prices.index.is_unique, "one row per date"
    assert prices.index.is_monotonic_increasing, "chronological order"
    return prices
