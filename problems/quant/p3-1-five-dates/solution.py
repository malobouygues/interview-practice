import pandas as pd


def add_availability(stocks: pd.DataFrame) -> pd.DataFrame:
    stocks = stocks.copy()
    # All timestamps are New York time (the agency's and NYMEX's clock): one time zone, kept naive.

    # 1. observation date: the stock level is measured at the end of the report week (a Friday)
    stocks["week_ending"] = pd.to_datetime(stocks["week_ending"])

    # 2. publication: the report is released on its release day at a fixed time
    stocks["release_date"] = pd.to_datetime(stocks["release_date"])
    release_time = pd.to_timedelta(stocks["release_time_et"] + ":00")

    # 3. availability: the first moment a trader could use the number
    stocks["available_at"] = stocks["release_date"] + release_time

    # 4. ingestion: when the number entered OUR database (a backfill can be years later)
    stocks["ingested_at"] = pd.to_datetime(stocks["ingested_at"])

    stocks["publication_lag_days"] = (stocks["release_date"] - stocks["week_ending"]).dt.days
    stocks["backfilled"] = (stocks["ingested_at"] - stocks["available_at"]) > pd.Timedelta(days=7)

    assert (stocks["available_at"] > stocks["week_ending"]).all(), "a value cannot be known before its week ends"

    columns = ["week_ending", "crude_stocks_mbbl", "release_date", "available_at",
               "ingested_at", "publication_lag_days", "backfilled"]
    return stocks[columns]
