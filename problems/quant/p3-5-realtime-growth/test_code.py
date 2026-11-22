import numpy as np
import pandas as pd

vintages = pd.read_csv("data/p3_us_oil_demand_vintages_synthetic.csv")
crack = pd.read_csv("data/p3_diesel_crack_monthly_synthetic.csv")
crack["month"] = pd.to_datetime(crack["month"], format="%Y-%m")
crack = crack.set_index("month")["diesel_crack_usd_bbl"]

decision_dates = list(pd.date_range("2016-03-31", "2019-12-31", freq="ME"))
table = realtime_growth(vintages, decision_dates)
print(table.head(6).round(2))
print("mean |real-time - final| (pp):", round((table["growth_realtime"] - table["growth_final"]).abs().mean(), 2))
print("months with opposite signs:", int((np.sign(table["growth_realtime"]) != np.sign(table["growth_final"])).sum()), "of", len(table))

# point-in-time: the crack of the decision month vs the growth known at that month-end
crack_at_decision = crack.reindex(table.index.to_period("M").to_timestamp()).to_numpy()
print("PIT correlation:", round(np.corrcoef(crack_at_decision, table["growth_realtime"])[0, 1], 3))

# the colleague's chart: final growth aligned on the observation month
final = vintages.sort_values("vintage_date").groupby("obs_month")["demand_kbd"].last()
final.index = pd.to_datetime(final.index, format="%Y-%m")
chart = pd.concat([crack, final.pct_change(12) * 100], axis=1).dropna()
print("observation-month, final-data correlation:", round(chart.corr().iloc[0, 1], 3))
