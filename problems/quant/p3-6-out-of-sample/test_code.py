import pandas as pd
import matplotlib.pyplot as plt

decisions = pd.read_csv("data/p3_decision_table_daily_synthetic.csv")
result = validate_out_of_sample(decisions)
print({k: round(float(v), 4) for k, v in result["fixed"].items()})
print("frozen coefficients:", result["coefficients"].round(5).to_dict())
print(result["walk_forward_path"].to_string(float_format="%.5f"))
print("walk-forward MAE %.4f RMSE %.4f" % (result["walk_forward_mae"], result["walk_forward_rmse"]))

# what a random split would have reported (for comparison only — never do this for a forecast)
shuffled = decisions.dropna(subset=["surprise_mbbl", "demand_growth_known_pct", "ret_fwd_10d"]).sample(frac=1.0, random_state=0)
print("random split: training rows from", shuffled.iloc[:1000]["date"].min(), "to", shuffled.iloc[:1000]["date"].max())

# errors over time: model vs the zero forecast, cumulative absolute error difference
walk = result["walk_forward"].set_index("date")
gap = (walk["realised"] - walk["prediction"]).abs() - walk["realised"].abs()
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(walk.index, 100 * walk["realised"], color="grey", linewidth=0.7, label="realised 10-day return")
ax[0].plot(walk.index, 100 * walk["prediction"], color="tab:red", label="walk-forward prediction")
ax[0].legend()
ax[0].set_ylabel("%")
ax[1].plot(walk.index, 100 * gap.cumsum())
ax[1].axhline(0, color="grey")
ax[1].set_title("cumulative (|model error| − |zero-forecast error|), in %: above 0 = worse than zero")
plt.tight_layout()
