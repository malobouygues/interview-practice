import numpy as np
import pandas as pd
import statsmodels.api as sm

# the weekly reports with their availability (as in 3.1)
stocks = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
stocks["week_ending"] = pd.to_datetime(stocks["week_ending"])
release = pd.to_datetime(stocks["release_date"] + " " + stocks["release_time_et"])
stocks["available_at"] = release.dt.tz_localize("America/New_York").dt.tz_convert("UTC")
stocks = stocks.sort_values("week_ending")
stocks["surprise_mbbl"] = stocks["crude_stocks_mbbl"].diff() - stocks["consensus_change_mbbl"]
prices = pd.read_csv("data/p3_wti_daily_synthetic.csv")

aligned = align_stocks(prices, stocks)
print(aligned.iloc[860:878].to_string())          # June 2022: the late release
print("age of the matched report:", aligned["age_days"].describe().round(1).to_dict())

# the analyst's join: on the week the report describes
wrong_side = stocks[["week_ending", "surprise_mbbl", "available_at"]].copy()
wrong_side["week_ending_key"] = wrong_side["week_ending"].dt.tz_localize("UTC")
wrong = pd.merge_asof(aligned[["date", "decision_time"]], wrong_side.sort_values("week_ending_key"),
                      left_on="decision_time", right_on="week_ending_key", direction="backward")
print("days using a report not yet published:", (wrong["available_at"] > wrong["decision_time"]).sum(), "of", len(wrong))

# 'does the latest surprise predict tomorrow's return?' on the eve of each release
next_return = np.log(aligned["wti_settle_usd_bbl"]).diff().shift(-1)
eve = aligned["date"].shift(-1).isin(set(pd.to_datetime(stocks["release_date"])))
for name, surprise in [("week_ending join", wrong["surprise_mbbl"]), ("available_at join", aligned["surprise_mbbl"])]:
    data = pd.DataFrame({"y": next_return[eve], "x": surprise[eve]}).dropna()
    fit = sm.OLS(data["y"], sm.add_constant(data["x"])).fit()
    print(name, "| corr", round(data["y"].corr(data["x"]), 3), "| t", round(fit.tvalues["x"], 2))
