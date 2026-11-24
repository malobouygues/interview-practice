import pandas as pd


def align_stocks(prices: pd.DataFrame, stocks: pd.DataFrame) -> pd.DataFrame:
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])

    # decision time = the WTI settlement, 14:30 New York: what was known at that moment?
    prices["decision_time"] = prices["date"] + pd.Timedelta(hours=14, minutes=30)

    # merge_asof needs both tables sorted on their time key
    prices = prices.sort_values("decision_time")
    known = stocks[["available_at", "week_ending", "crude_stocks_mbbl"]]
    known = known.sort_values("available_at")

    # backward: for each decision, the LAST report already available (never a later one);
    # tolerance: a report older than 10 days is not used
    aligned = pd.merge_asof(prices, known,
                            left_on="decision_time", right_on="available_at",
                            direction="backward", tolerance=pd.Timedelta(days=10))

    aligned["age_days"] = (aligned["decision_time"] - aligned["week_ending"]).dt.days

    matched = aligned["available_at"].notna()
    assert (aligned.loc[matched, "available_at"] <= aligned.loc[matched, "decision_time"]).all(), "future information"

    columns = ["date", "wti_usd_bbl", "week_ending", "available_at", "crude_stocks_mbbl", "age_days"]
    return aligned[columns]
