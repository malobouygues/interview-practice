import pandas as pd
import statsmodels.api as sm

RESEARCH_END = pd.Timestamp("2022-12-31")    # 2023-2024 stays untouched for the out-of-sample test (3.6)


def reaction_and_drift(events, decisions):
    # ---- 1. reaction: from the 10:29 snapshot to the 14:30 settlement, one row per release
    events = events.copy()
    events["release_date"] = pd.to_datetime(events["release_date"])
    sample = events[events["release_date"] <= RESEARCH_END]
    sample = sample.dropna(subset=["surprise_mbbl", "ret_reaction"])
    X = sm.add_constant(sample[["surprise_mbbl"]])
    ols = sm.OLS(sample["ret_reaction"], X).fit()
    hac = sm.OLS(sample["ret_reaction"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    reaction = pd.DataFrame({"coef": ols.params, "se": ols.bse, "t": ols.tvalues,
                             "se_hac": hac.bse, "t_hac": hac.tvalues})

    # ---- 2. drift: the next 10 trading days after each settlement, one row per DAY
    decisions = decisions.copy()
    decisions["target_end_date"] = pd.to_datetime(decisions["target_end_date"])
    features = ["surprise_mbbl", "demand_growth_known_pct"]
    daily = decisions[decisions["target_end_date"] <= RESEARCH_END]
    daily = daily.dropna(subset=["ret_fwd_10d"] + features)
    X_daily = sm.add_constant(daily[features])
    ols_daily = sm.OLS(daily["ret_fwd_10d"], X_daily).fit()
    # two consecutive 10-day windows share 9 days: errors are correlated up to lag 9 by construction
    hac_daily = sm.OLS(daily["ret_fwd_10d"], X_daily).fit(cov_type="HAC", cov_kwds={"maxlags": 9})
    drift = pd.DataFrame({"coef": ols_daily.params, "se": ols_daily.bse, "t": ols_daily.tvalues,
                          "se_hac": hac_daily.bse, "t_hac": hac_daily.tvalues})

    return {"reaction": reaction, "drift": drift,
            "n_reaction": int(ols.nobs), "n_drift": int(ols_daily.nobs),
            "dw_reaction": sm.stats.durbin_watson(ols.resid),
            "dw_drift": sm.stats.durbin_watson(ols_daily.resid)}
