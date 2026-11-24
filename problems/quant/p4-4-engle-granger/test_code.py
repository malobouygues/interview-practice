import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv")
result = relationship_by_period(prices)
print(result["periods"].round(4).to_string())
print("Chow F = %.2f, p = %.3g" % (result["chow_f"], result["chow_p"]))

# placebo dates INSIDE each regime: no break there, the test should not reject
before = prices[prices["date"] < "2016-01-01"]
after = prices[prices["date"] >= "2016-01-01"]
for part, placebo in [(before, "2014-01-01"), (before, "2014-07-01"), (after, "2017-06-01"), (after, "2018-01-01")]:
    check = relationship_by_period(part, placebo)
    print("placebo", placebo, "F = %.2f, p = %.3f" % (check["chow_f"], check["chow_p"]))

# optional extension: error-correction model in each regime
table = prices.set_index(pd.to_datetime(prices["date"]))
logs = np.log(table[["brent", "wti"]])
for name, part in [("before 2016", logs[logs.index < "2016-01-01"]), ("from 2016", logs[logs.index >= "2016-01-01"])]:
    long_run = sm.OLS(part["wti"], sm.add_constant(part["brent"])).fit()
    data = pd.DataFrame({"d_wti": part["wti"].diff(), "d_brent": part["brent"].diff(), "gap": long_run.resid.shift(1)}).dropna()
    ecm = sm.OLS(data["d_wti"], sm.add_constant(data[["d_brent", "gap"]])).fit()
    alpha = ecm.params["gap"]
    print(name, "alpha %.4f (t %.1f), half-life %.1f days" % (alpha, ecm.tvalues["gap"], np.log(0.5) / np.log(1 + alpha)))

fig, ax = plt.subplots(figsize=(10, 3.6))
(table["brent"] - table["wti"]).plot(ax=ax, linewidth=0.8, title="Brent - WTI (USD/bbl)")
ax.axvline(pd.Timestamp("2016-01-01"), color="red", linestyle="--")
ax.axhline(result["periods"].loc["full sample", "mean_spread_usd"], color="grey", linestyle=":")
