import pandas as pd


def known_at(vintages, decision_dates):
    vintages = vintages.copy()
    vintages["vintage_date"] = pd.to_datetime(vintages["vintage_date"])

    # the value as the database shows it TODAY: the last vintage of each month
    final = vintages.sort_values("vintage_date").groupby("obs_month")["demand_kbd"].last()

    rows = []
    for decision in pd.to_datetime(pd.Series(decision_dates)):
        # a vintage dated D is usable from the next day on
        published = vintages[vintages["vintage_date"] < decision]
        latest = published.sort_values("vintage_date").groupby("obs_month")["demand_kbd"].last()
        month = latest.index.max()
        a_year_before = str(pd.Period(month, freq="M") - 12)
        rows.append({"decision_date": decision,
                     "latest_month": month,
                     "demand_known_kbd": latest[month],
                     "demand_final_kbd": final[month],
                     "growth_known_pct": 100 * (latest[month] / latest[a_year_before] - 1),
                     "growth_final_pct": 100 * (final[month] / final[a_year_before] - 1)})
    return pd.DataFrame(rows)
