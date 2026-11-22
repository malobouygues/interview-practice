#!/usr/bin/env python3
"""Rebuild the SYNTHETIC datasets of the Quantitative Methods track.

    python3 problems/quant/data/generate_data.py

Every series here is simulated with a fixed seed. None of it is market data:
the dates, units and orders of magnitude are realistic so that the economic
interpretation makes sense, but the paths are random draws. The seeds were
picked so that each statistical phenomenon the exercises teach is actually
visible in the sample (a different seed can give a different test result -
which is itself one of the lessons about statistical power).

The committed CSV files are the reference: the exercises and their tests read
them, not this script. numpy does not promise identical random streams across
major versions, so re-running this script on another numpy may change the
last digits - keep the committed CSVs unless you mean to change the data.
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))


def ttf_daily(seed=21):
    """TTF front-month gas price, EUR/MWh, business days 2017-2019.

    log price = random walk with fat-tailed (Student t, 4 d.o.f.) daily shocks,
    daily volatility about 2.2 %. A price with a stochastic trend.
    """
    dates = pd.bdate_range("2017-01-02", "2019-12-31")
    rng = np.random.default_rng(seed)
    shocks = rng.standard_t(4, size=len(dates) - 1) / np.sqrt(2) * 0.022
    log_p = np.log(18.0) + np.concatenate([[0.0], np.cumsum(shocks)])
    return pd.DataFrame({"date": dates, "ttf": np.round(np.exp(log_p), 2)})


def diesel_demand_monthly(seed=1):
    """Diesel / gasoil demand, kb/d, monthly 2010-2019.

    deterministic linear trend + fixed seasonal profile (heating season)
    + short-memory stationary noise. A trend-stationary series.
    """
    months = pd.date_range("2010-01-01", "2019-12-01", freq="MS")
    n = len(months)
    season = np.array([45, 38, 22, 2, -14, -26, -33, -36, -22, -4, 14, 34], dtype=float)
    season -= season.mean()
    rng = np.random.default_rng(seed)
    e = rng.normal(0.0, 14.0, n)
    noise = np.zeros(n)
    for t in range(n):
        noise[t] = (0.2 * noise[t - 1] if t else 0.0) + e[t]
    demand = 1150.0 + 1.1 * np.arange(n) + season[months.month - 1] + noise
    return pd.DataFrame({"month": months, "demand_kbd": np.round(demand, 1)})


def crude_history(seed_brent=61, seed_wti=1061, seed_coffee=2299):
    """Brent and WTI, USD/bbl, business days 2012-2019, plus an unrelated soft.

    Brent: log random walk (daily vol 1.8 %).
    WTI: error-correction dynamics in logs around  log WTI = a + log Brent.
      before 2016-01-01 (export ban, landlocked crude):  a = log(0.84),
          short-run pass-through 0.60, 5 % of the gap closed per day
      from 2016-01-01 (exports allowed):                 a = log(0.94),
          short-run pass-through 0.90, 10 % of the gap closed per day
      one WTI-specific supply shock (-5 %) on 2017-08-28 (hurricane-type event).
    Coffee (US cents/lb): an independent log random walk - no economic link
    with crude by construction.
    """
    dates = pd.bdate_range("2012-01-02", "2019-12-31")
    n = len(dates)
    brk = dates.searchsorted(pd.Timestamp("2016-01-01"))
    shock_day = dates.searchsorted(pd.Timestamp("2017-08-28"))

    rb = np.random.default_rng(seed_brent)
    b = np.log(105.0) + np.concatenate([[0.0], np.cumsum(rb.normal(0.0, 0.018, n - 1))])

    regimes = {"pre": (np.log(1 - 0.16), 0.60, -0.05), "post": (np.log(1 - 0.06), 0.90, -0.10)}
    eps = np.random.default_rng(seed_wti).normal(0.0, 0.008, n)
    w = np.zeros(n)
    w[0] = regimes["pre"][0] + b[0]
    for t in range(1, n):
        a, gamma, alpha = regimes["pre"] if t < brk else regimes["post"]
        w[t] = w[t - 1] + gamma * (b[t] - b[t - 1]) + alpha * (w[t - 1] - a - b[t - 1]) + eps[t]
        if t == shock_day:
            w[t] -= 0.05

    rc = np.random.default_rng(seed_coffee)
    c = np.log(135.0) + np.concatenate([[0.0], np.cumsum(rc.normal(0.0, 0.017, n - 1))])

    return pd.DataFrame({"date": dates,
                         "brent": np.round(np.exp(b), 2),
                         "wti": np.round(np.exp(w), 2),
                         "coffee": np.round(np.exp(c), 2)})


def main():
    ttf_daily().to_csv(os.path.join(HERE, "ttf_daily_synthetic.csv"), index=False)
    diesel_demand_monthly().to_csv(os.path.join(HERE, "diesel_demand_monthly_synthetic.csv"), index=False)
    hist = crude_history()
    # Cases 2-3: the exports-allowed regime only, once the 2016 re-pricing has settled
    recent = hist[hist["date"] >= "2016-07-01"]
    recent.to_csv(os.path.join(HERE, "crude_daily_synthetic.csv"), index=False)
    # Case 4: the full history, Brent and WTI only
    hist[["date", "brent", "wti"]].to_csv(os.path.join(HERE, "crude_history_synthetic.csv"), index=False)
    print("written to", HERE)


if __name__ == "__main__":
    main()
