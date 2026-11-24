import numpy as np
import pandas as pd

FUNCTION = "validate_out_of_sample"


def hand_made():
    # a relationship that exists until 2022 and disappears; late-December rows with huge targets that end in 2023
    rng = np.random.default_rng(41)
    days = pd.bdate_range("2019-01-02", "2024-12-31")
    surprise = rng.normal(0, 3, len(days))
    demand = np.sin(np.arange(len(days)) / 90.0) * 3
    beta = np.where(days <= "2022-12-31", -0.006, 0.0)
    target = beta * surprise + rng.normal(0, 0.05, len(days))
    end = pd.Series(days).shift(-10)
    late = (days >= "2022-12-19") & (days <= "2022-12-30")
    target[late] = 0.5 * surprise[late]             # labels that end in 2023: must not be used for training
    decisions = pd.DataFrame({"date": days.strftime("%Y-%m-%d"), "surprise_mbbl": surprise,
                              "demand_growth_known_pct": demand,
                              "target_end_date": end.dt.strftime("%Y-%m-%d").values, "ret_fwd_10d": target})
    decisions.loc[decisions.index[-10:], "ret_fwd_10d"] = np.nan
    decisions.loc[5, "surprise_mbbl"] = np.nan
    return {"decisions": decisions}


TESTS = [
    {"name": "Hand-made: a relationship that ends in 2022, and labels that end in 2023 (purging)",
     "origin": "extra", "args": hand_made},
    {"name": "The daily decision table 2019-2024", "origin": "extra",
     "args": lambda: {"decisions": pd.read_csv("data/p3_decision_table_daily_synthetic.csv")}},
]
