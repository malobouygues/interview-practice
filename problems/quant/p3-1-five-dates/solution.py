import pandas as pd

NEW_YORK = "America/New_York"


def add_availability(stocks):
    stocks = stocks.copy()

    # observation date: the week the number describes (ending Friday)
    stocks["week_ending"] = pd.to_datetime(stocks["week_ending"])

    # publication = availability: release date + 10:30 New York time, expressed in UTC
    release_local = pd.to_datetime(stocks["release_date"] + " " + stocks["release_time_et"])
    stocks["available_at"] = release_local.dt.tz_localize(NEW_YORK).dt.tz_convert("UTC")

    # ingestion: when OUR database received it (already UTC)
    stocks["ingested_at"] = pd.to_datetime(stocks["ingested_at_utc"], utc=True)

    stocks["publication_lag_days"] = (release_local.dt.normalize() - stocks["week_ending"]).dt.days
    stocks["backfilled"] = stocks["ingested_at"] - stocks["available_at"] > pd.Timedelta(days=2)

    # the information content of a release: the change against the previous week, and the surprise
    stocks = stocks.sort_values("week_ending")
    stocks["stocks_change_mbbl"] = stocks["crude_stocks_mbbl"].diff()
    stocks["surprise_mbbl"] = stocks["stocks_change_mbbl"] - stocks["consensus_change_mbbl"]
    return stocks.reset_index(drop=True)
