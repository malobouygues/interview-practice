import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf

events = pd.read_csv("data/p3_release_events_synthetic.csv")
decisions = pd.read_csv("data/p3_decision_table_daily_synthetic.csv")

result = reaction_and_drift(events, decisions)
print("reaction (n=%d, DW=%.2f)" % (result["n_reaction"], result["dw_reaction"]))
print(result["reaction"].round(5).to_string())
print("drift (n=%d, DW=%.2f)" % (result["n_drift"], result["dw_drift"]))
print(result["drift"].round(5).to_string())

# why the drift residuals are autocorrelated: the windows overlap
sample = decisions[pd.to_datetime(decisions["target_end_date"]) <= "2022-12-31"]
sample = sample.dropna(subset=["ret_fwd_10d", "surprise_mbbl", "demand_growth_known_pct"])
fit = sm.OLS(sample["ret_fwd_10d"], sm.add_constant(sample[["surprise_mbbl", "demand_growth_known_pct"]])).fit()
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
plot_acf(fit.resid, lags=20, ax=ax[0], title="ACF of the drift residuals (10-day windows)")
reaction_sample = events[pd.to_datetime(events["release_date"]) <= "2022-12-31"]
ax[1].scatter(reaction_sample["surprise_mbbl"], 100 * reaction_sample["ret_reaction"], s=8)
ax[1].set_xlabel("stock surprise (million barrels)")
ax[1].set_ylabel("10:29 -> settlement return (%)")
plt.tight_layout()

# is the drift the same in every sub-period? (surprise only, HAC errors)
sample = sample.copy()
sample["date"] = pd.to_datetime(sample["date"])
for start, end in [("2019-01-01", "2020-04-30"), ("2020-05-01", "2021-12-31"), ("2022-01-01", "2022-12-31")]:
    part = sample[(sample["date"] >= start) & (sample["date"] <= end)]
    part_fit = sm.OLS(part["ret_fwd_10d"], sm.add_constant(part[["surprise_mbbl"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 9})
    print(start, end, "slope %.3f %% per mb, HAC t %.2f" % (100 * part_fit.params["surprise_mbbl"], part_fit.tvalues["surprise_mbbl"]))
