import pandas as pd
import matplotlib.pyplot as plt

vintages = pd.read_csv("data/p3_us_oil_demand_vintages_synthetic.csv")
print(vintages[vintages["obs_month"] == "2020-12"].to_string())

print(known_at(vintages, ["2021-03-15", "2024-03-15", "2024-09-15"]).to_string(float_format="%.2f"))

# one decision per month: what the desk knew vs what the database says today
dates = pd.date_range("2019-01-15", "2024-12-15", freq="MS") + pd.Timedelta(days=14)
history = known_at(vintages, dates).set_index("decision_date")
revision = history["demand_final_kbd"] - history["demand_known_kbd"]
print("final minus known: mean", round(revision.mean(), 1), "| mean absolute", round(revision.abs().mean(), 1))
print("growth gap (pp), mean absolute:", round((history["growth_final_pct"] - history["growth_known_pct"]).abs().mean(), 2))

fig, ax = plt.subplots(figsize=(10, 3.8))
history["growth_known_pct"].plot(ax=ax, label="growth as known (genuine point-in-time)")
history["growth_final_pct"].plot(ax=ax, label="growth from today's values (pseudo point-in-time)")
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_title("US oil demand, year-on-year growth seen at each decision date (%)")
ax.legend()
