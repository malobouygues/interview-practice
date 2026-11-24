import pandas as pd

FUNCTION = "regime_comparison"


def prices():
    p = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return p[["brent", "wti"]]


TESTS = [
    {"name": "Break on 2016-01-01 (end of the export ban)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": prices(), "break_date": "2016-01-01"}},
    {"name": "Placebo inside the post regime (2018-01-01, data from mid-2016)", "origin": "extra",
     "args": lambda: {"prices": prices().loc["2016-07-01":], "break_date": "2018-01-01"}},
    {"name": "Placebo inside the pre regime (2014-01-01, data before 2016)", "origin": "extra",
     "args": lambda: {"prices": prices().loc[:"2015-12-31"], "break_date": "2014-01-01"}},
]
