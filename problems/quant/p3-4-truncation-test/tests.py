import pandas as pd

FUNCTION = "truncation_test"
CUTOFF = "2022-06-27 23:59"


def stocks():
    s = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
    s["week_ending"] = pd.to_datetime(s["week_ending"])
    release = pd.to_datetime(s["release_date"] + " " + s["release_time_et"])
    s["available_at"] = release.dt.tz_localize("America/New_York").dt.tz_convert("UTC")
    s = s.sort_values("week_ending")
    s["surprise_mbbl"] = s["crude_stocks_mbbl"].diff() - s["consensus_change_mbbl"]
    return s


def prices():
    return pd.read_csv("data/p3_wti_daily_synthetic.csv")


NEW_YORK = "America/New_York"


def decision_days(prices):
    days = prices.copy()
    days["date"] = pd.to_datetime(days["date"])
    settlement = days["date"] + pd.Timedelta(hours=14, minutes=30)
    days["decision_time"] = settlement.dt.tz_localize(NEW_YORK).dt.tz_convert("UTC")
    return days.sort_values("decision_time")


def correct_features(stocks, prices):
    """Latest surprise and stocks vs the average of the 52 previous reports, as known at the settlement."""
    known = stocks.sort_values("available_at").copy()
    known["stocks_vs_52w_mbbl"] = known["crude_stocks_mbbl"] - known["crude_stocks_mbbl"].rolling(52, min_periods=26).mean()
    table = pd.merge_asof(decision_days(prices), known[["available_at", "surprise_mbbl", "stocks_vs_52w_mbbl"]],
                          left_on="decision_time", right_on="available_at", direction="backward",
                          tolerance=pd.Timedelta(days=10))
    return table.set_index("date")[["surprise_mbbl", "stocks_vs_52w_mbbl"]]


def joined_on_week_ending(stocks, prices):
    """Same features, but each report is attached from the Friday it describes."""
    known = stocks.sort_values("week_ending").copy()
    known["stocks_vs_52w_mbbl"] = known["crude_stocks_mbbl"] - known["crude_stocks_mbbl"].rolling(52, min_periods=26).mean()
    known["key"] = known["week_ending"].dt.tz_localize("UTC")
    table = pd.merge_asof(decision_days(prices), known[["key", "surprise_mbbl", "stocks_vs_52w_mbbl"]],
                          left_on="decision_time", right_on="key", direction="backward")
    return table.set_index("date")[["surprise_mbbl", "stocks_vs_52w_mbbl"]]


def standardised_on_full_sample(stocks, prices):
    """Correct join, but the surprise is divided by its standard deviation over the whole sample."""
    table = correct_features(stocks, prices)
    table["surprise_mbbl"] = table["surprise_mbbl"] / stocks["surprise_mbbl"].std()
    return table


def centred_average(stocks, prices):
    """Correct join, but the 52-week average is centred: it uses the 26 reports that come after."""
    known = stocks.sort_values("available_at").copy()
    known["stocks_vs_52w_mbbl"] = known["crude_stocks_mbbl"] - known["crude_stocks_mbbl"].rolling(52, min_periods=26, center=True).mean()
    table = pd.merge_asof(decision_days(prices), known[["available_at", "surprise_mbbl", "stocks_vs_52w_mbbl"]],
                          left_on="decision_time", right_on="available_at", direction="backward",
                          tolerance=pd.Timedelta(days=10))
    return table.set_index("date")[["surprise_mbbl", "stocks_vs_52w_mbbl"]]


TESTS = [
    {"name": "Correct builder (backward join on availability, trailing average): nothing may change",
     "origin": "extra", "args": lambda: {"build_features": correct_features, "stocks": stocks(), "prices": prices(), "cutoff": CUTOFF}},
    {"name": "Join on week_ending: the rows just before the cutoff change", "origin": "extra",
     "args": lambda: {"build_features": joined_on_week_ending, "stocks": stocks(), "prices": prices(), "cutoff": CUTOFF}},
    {"name": "Surprise standardised with the full-sample std: every row changes", "origin": "extra",
     "args": lambda: {"build_features": standardised_on_full_sample, "stocks": stocks(), "prices": prices(), "cutoff": CUTOFF}},
    {"name": "Centred 52-week average: the last half-year before the cutoff changes", "origin": "extra",
     "args": lambda: {"build_features": centred_average, "stocks": stocks(), "prices": prices(), "cutoff": "2020-12-31 23:59"}},
]
