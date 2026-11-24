import pandas as pd

stocks = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
stocks["week_ending"] = pd.to_datetime(stocks["week_ending"])
release = pd.to_datetime(stocks["release_date"] + " " + stocks["release_time_et"])
stocks["available_at"] = release.dt.tz_localize("America/New_York").dt.tz_convert("UTC")
stocks = stocks.sort_values("week_ending")
stocks["surprise_mbbl"] = stocks["crude_stocks_mbbl"].diff() - stocks["consensus_change_mbbl"]
prices = pd.read_csv("data/p3_wti_daily_synthetic.csv")

# four ways of building the same two features (only the first is point-in-time)
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


for cutoff in ["2022-06-27 23:59", "2022-06-30 23:59"]:          # a Monday, then a Thursday
    for builder in [correct_features, joined_on_week_ending, standardised_on_full_sample, centred_average]:
        print(cutoff, builder.__name__, truncation_test(builder, stocks, prices, cutoff))

# a manual check of three rows: what did the correct builder attach, and when was it published?
table = correct_features(stocks, prices)
print(table.loc["2022-06-22":"2022-06-30"].round(2).to_string())
print(stocks[stocks["week_ending"] >= "2022-06-10"][["week_ending", "available_at", "surprise_mbbl"]].head(3).to_string())
