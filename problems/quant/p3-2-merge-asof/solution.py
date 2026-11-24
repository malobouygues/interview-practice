import pandas as pd

NEW_YORK = "America/New_York"


def align_stocks(prices, stocks):
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])

    # decision time = the WTI settlement, 14:30 New York, in UTC
    settlement_local = prices["date"] + pd.Timedelta(hours=14, minutes=30)
    prices["decision_time"] = settlement_local.dt.tz_localize(NEW_YORK).dt.tz_convert("UTC")

    # merge_asof needs both sides sorted on their time key
    prices = prices.sort_values("decision_time")
    known = stocks[["available_at", "week_ending", "crude_stocks_mbbl", "surprise_mbbl"]]
    known = known.sort_values("available_at")

    # backward: for each decision, the LAST report already published (never a later one);
    # tolerance: a report more than 10 days old is not used
    aligned = pd.merge_asof(prices, known, left_on="decision_time", right_on="available_at",
                            direction="backward", tolerance=pd.Timedelta(days=10))

    aligned["age_days"] = (aligned["date"] - aligned["week_ending"]).dt.days

    matched = aligned["available_at"].notna()
    no_future = aligned.loc[matched, "available_at"] <= aligned.loc[matched, "decision_time"]
    assert no_future.all(), "a report published after the decision time was used"

    columns = ["date", "wti_settle_usd_bbl", "decision_time", "week_ending", "available_at",
               "crude_stocks_mbbl", "surprise_mbbl", "age_days"]
    return aligned[columns]
