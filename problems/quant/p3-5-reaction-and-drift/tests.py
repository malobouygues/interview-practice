import numpy as np
import pandas as pd

FUNCTION = "reaction_and_drift"


def hand_made():
    rng = np.random.default_rng(17)
    releases = pd.date_range("2021-01-06", "2023-06-28", freq="7D")
    surprise = rng.normal(0, 3, len(releases))
    events = pd.DataFrame({"release_date": releases.strftime("%Y-%m-%d"), "surprise_mbbl": surprise,
                           "ret_reaction": -0.004 * surprise + rng.normal(0, 0.01, len(releases))})
    events.loc[0, "surprise_mbbl"] = np.nan
    days = pd.bdate_range("2021-01-04", "2023-06-30")
    noise = rng.normal(0, 0.02, len(days))
    returns = pd.Series(noise, index=days)
    forward = np.log(np.exp(returns.cumsum())).diff(10).shift(-10)
    decisions = pd.DataFrame({"date": days.strftime("%Y-%m-%d"),
                              "surprise_mbbl": np.repeat(surprise, 5)[:len(days)],
                              "demand_growth_known_pct": np.linspace(-3, 3, len(days)),
                              "target_end_date": pd.Series(days).shift(-10).dt.strftime("%Y-%m-%d").values,
                              "ret_fwd_10d": forward.values})
    return {"events": events, "decisions": decisions}


TESTS = [
    {"name": "Hand-made: weekly reactions and overlapping 10-day returns, research sample to 2022",
     "origin": "extra", "args": hand_made},
    {"name": "Release events and the daily decision table, 2019-2022", "origin": "extra",
     "args": lambda: {"events": pd.read_csv("data/p3_release_events_synthetic.csv"),
                      "decisions": pd.read_csv("data/p3_decision_table_daily_synthetic.csv")}},
]
