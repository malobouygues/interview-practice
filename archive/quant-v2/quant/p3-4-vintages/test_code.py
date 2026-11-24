import pandas as pd

vintages = pd.read_csv("data/p3_us_oil_demand_vintages_synthetic.csv")
print(vintages[vintages["obs_month"] == "2016-01"])

for date in ["2016-06-15", "2016-06-30", "2017-09-15"]:
    view = as_of(vintages, date)
    print(date, "-> latest month visible:", view.index[-1].strftime("%Y-%m"),
          "| January 2016 =", view.get(pd.Timestamp("2016-01-01")))

ordered = vintages.sort_values("vintage_date")
first_release = ordered.groupby("obs_month")["demand_kbd"].first()
final = ordered.groupby("obs_month")["demand_kbd"].last()
revision = final - first_release
print("revision first -> final (kb/d): mean", round(revision.mean(), 1), "| std", round(revision.std(), 1))
