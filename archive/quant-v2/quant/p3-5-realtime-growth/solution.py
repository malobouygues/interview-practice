import pandas as pd


def realtime_growth(vintages: pd.DataFrame, decision_dates: list) -> pd.DataFrame:
    vintages = vintages.copy()
    vintages["obs_month"] = pd.to_datetime(vintages["obs_month"], format="%Y-%m")
    vintages["vintage_date"] = pd.to_datetime(vintages["vintage_date"])
    vintages = vintages.sort_values("vintage_date")

    # the latest (revised) history, as it is known today
    final_view = vintages.groupby("obs_month")["demand_kbd"].last()
    final_growth = final_view.pct_change(12) * 100

    rows = []
    for decision_date in decision_dates:
        decision_date = pd.Timestamp(decision_date)

        # what had been published on the decision date, latest estimate per month
        known = vintages[vintages["vintage_date"] <= decision_date]
        view = known.groupby("obs_month")["demand_kbd"].last()
        growth = view.pct_change(12) * 100

        latest_month = view.index[-1]                 # the most recent month an analyst could see
        rows.append([decision_date, latest_month, growth.iloc[-1], final_growth.loc[latest_month]])

    result = pd.DataFrame(rows, columns=["decision_date", "obs_month", "growth_realtime", "growth_final"])
    result = result.set_index("decision_date")
    return result
