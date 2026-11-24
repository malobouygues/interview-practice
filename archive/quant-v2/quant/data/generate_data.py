#!/usr/bin/env python3
"""Rebuild the SYNTHETIC datasets of the Quantitative Methods track.

    python3 problems/quant/data/generate_data.py

Every value here is simulated with a fixed seed. None of it is market data: dates,
units, calendars and orders of magnitude are realistic so that the economic reading
makes sense, and some well-known episodes (a negative WTI expiry, a Gulf Coast
hurricane, the end of the US export ban) are *imitated*, but the numbers are invented.

The imperfections (vendor codes, duplicates, corrections, a fat-finger print, a frozen
feed, non-reported months, late publications, revisions) are put in on purpose: each
one is the subject of an exercise.

The committed CSV files are the reference that the exercises and tests read. numpy does
not promise identical random streams across major versions, so re-running this script
on another numpy may change the last digits.
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

US_HOLIDAYS = ["2017-01-02", "2017-01-16", "2017-02-20", "2017-04-14", "2017-05-29", "2017-07-04",
               "2017-09-04", "2017-11-23", "2017-12-25",
               "2018-01-01", "2018-01-15", "2018-02-19", "2018-03-30", "2018-05-28", "2018-07-04",
               "2018-09-03", "2018-11-22", "2018-12-25",
               "2019-01-01", "2019-01-21", "2019-02-18", "2019-04-19", "2019-05-27", "2019-07-04",
               "2019-09-02", "2019-11-28", "2019-12-25",
               "2020-01-01", "2020-01-20", "2020-02-17", "2020-04-10", "2020-05-25", "2020-07-03",
               "2020-09-07", "2020-11-26", "2020-12-25",
               "2021-01-01", "2021-01-18", "2021-02-15", "2021-04-02", "2021-05-31", "2021-07-05",
               "2021-09-06", "2021-11-25", "2021-12-24"]
UK_HOLIDAYS = ["2017-01-02", "2017-04-14", "2017-04-17", "2017-05-01", "2017-05-29", "2017-08-28",
               "2017-12-25", "2017-12-26",
               "2018-01-01", "2018-03-30", "2018-04-02", "2018-05-07", "2018-05-28", "2018-08-27",
               "2018-12-25", "2018-12-26",
               "2019-01-01", "2019-04-19", "2019-04-22", "2019-05-06", "2019-05-27", "2019-08-26",
               "2019-12-25", "2019-12-26",
               "2020-01-01", "2020-04-10", "2020-04-13", "2020-05-08", "2020-05-25", "2020-08-31",
               "2020-12-25", "2020-12-28",
               "2021-01-01", "2021-04-02", "2021-04-05", "2021-05-03", "2021-05-31", "2021-08-30",
               "2021-12-27", "2021-12-28"]


def ar_noise(rng, n, phi, sd):
    """Stationary noise: each day keeps a share phi of yesterday's deviation."""
    shocks = rng.normal(0.0, sd, n)
    noise = np.zeros(n)
    for t in range(n):
        previous = noise[t - 1] if t > 0 else 0.0
        noise[t] = phi * previous + shocks[t]
    return noise


# ---------------------------------------------------------------------------
# Project 1 — a raw vendor file of crude benchmarks, 2019-2021
# ---------------------------------------------------------------------------
def p1_crude_vendor_file(seed=7):
    dates = pd.bdate_range("2019-01-02", "2021-12-31")
    n = len(dates)
    rng = np.random.default_rng(seed)

    # Brent follows a realistic 2019-2021 shape (anchor) plus noise
    knots = pd.Series({"2019-01-02": 55, "2019-04-24": 72, "2019-08-07": 57, "2019-12-31": 66,
                       "2020-02-20": 59, "2020-03-31": 24, "2020-04-21": 19, "2020-06-30": 41,
                       "2020-12-31": 51, "2021-07-05": 77, "2021-08-20": 65, "2021-10-25": 85,
                       "2021-12-01": 69, "2021-12-31": 78})
    knot_dates = pd.to_datetime(knots.index)
    anchor = np.interp(dates.asi8, knot_dates.asi8, np.log(knots.values.astype(float)))
    brent = np.exp(anchor + ar_noise(rng, n, 0.97, 0.012))

    # WTI trades at a few dollars below Brent; the discount widens during the 2020 storage glut
    glut = np.where((dates >= "2020-03-15") & (dates <= "2020-05-15"), 4.0, 0.0)
    wti = brent - (3.6 + glut + ar_noise(rng, n, 0.9, 0.35))
    expiry = dates.get_loc(pd.Timestamp("2020-04-20"))
    wti[expiry] = -35.90                          # front-month expiry squeeze: a genuine negative print
    wti[expiry + 1] = brent[expiry + 1] - 9.0

    # Dubai (Middle East sour) sits just below Brent
    dubai = brent - (1.3 + ar_noise(rng, n, 0.9, 0.40))

    clean = pd.DataFrame({"brent": brent, "wti": wti, "dubai": dubai}, index=dates).round(2)
    clean.loc[clean.index.isin(pd.to_datetime(UK_HOLIDAYS)), "brent"] = np.nan
    clean.loc[clean.index.isin(pd.to_datetime(US_HOLIDAYS)), "wti"] = np.nan
    christmas = clean.index.strftime("%m-%d").isin(["12-25", "01-01"])
    clean.loc[christmas, "dubai"] = np.nan

    # --- build the raw export, one monthly batch at a time
    def fmt(value, holiday):
        if holiday:
            return "HOL"
        return "%.2f" % value

    rows = []
    for date, row in clean.iterrows():
        month_end = date + pd.offsets.MonthBegin(1)
        loaded_at = pd.bdate_range(month_end, periods=1)[0] + pd.Timedelta(hours=6)
        if date.strftime("%Y-%m") == "2020-06":
            loaded_at = pd.Timestamp("2020-07-15 06:00")          # this batch arrived late
        rows.append({"Date": date.strftime("%d/%m/%Y"),
                     "Brent (USD/bbl)": fmt(row["brent"], np.isnan(row["brent"])),
                     "WTI (USD/bbl)": fmt(row["wti"], np.isnan(row["wti"])),
                     "Dubai (USD/bbl)": fmt(row["dubai"], np.isnan(row["dubai"])),
                     "loaded_at": loaded_at.strftime("%Y-%m-%d %H:%M"),
                     "_date": date})
    raw = pd.DataFrame(rows)

    # values the vendor did not deliver (not holidays): coded "-"
    for day in ["2019-08-05", "2020-11-16", "2021-02-22"]:
        raw.loc[raw["_date"] == pd.Timestamp(day), "Dubai (USD/bbl)"] = "-"
    raw.loc[raw["_date"] == pd.Timestamp("2020-03-09"), "WTI (USD/bbl)"] = "-"

    # a fat-finger print, never corrected by the vendor (decimal point shifted)
    fat = raw["_date"] == pd.Timestamp("2021-03-15")
    raw.loc[fat, "Brent (USD/bbl)"] = "%.2f" % (clean.loc["2021-03-15", "brent"] * 10)

    # two settlements first sent wrong, then re-sent corrected in a later load
    corrections = []
    for day, column in [("2019-06-12", "WTI (USD/bbl)"), ("2021-09-08", "Brent (USD/bbl)")]:
        mask = raw["_date"] == pd.Timestamp(day)
        corrected = raw.loc[mask].copy()
        corrected["loaded_at"] = (pd.Timestamp(day) + pd.Timedelta(days=9)).strftime("%Y-%m-%d 06:00")
        corrections.append(corrected)
        raw.loc[mask, column] = "%.2f" % (float(raw.loc[mask, column].iloc[0]) + 1.50)

    # the late June-2020 batch is appended at the end of the file
    late = raw["_date"].dt.strftime("%Y-%m") == "2020-06"
    raw = pd.concat([raw[~late], raw[late]] + corrections, ignore_index=True)

    # five days loaded twice (identical rows)
    for day in ["2019-03-14", "2019-11-05", "2020-08-19", "2021-01-26", "2021-06-10"]:
        position = raw.index[raw["_date"] == pd.Timestamp(day)][0]
        raw = pd.concat([raw.loc[:position], raw.loc[[position]], raw.loc[position + 1:]], ignore_index=True)

    return raw.drop(columns="_date")


def p1_clean_layer(raw):
    """The clean layer, built from the raw export with the rules of exercises 1.2 and 1.3:
    vendor codes -> NaN, explicit day-first dates, identical rows dropped, the latest load wins
    for a corrected date, and the confirmed x10 fat-finger set to NaN (WTI's negative print kept)."""
    prices = raw.replace({"HOL": np.nan, "-": np.nan})
    prices.columns = ["date", "brent", "wti", "dubai", "loaded_at"]
    prices["date"] = pd.to_datetime(prices["date"], format="%d/%m/%Y")
    prices["loaded_at"] = pd.to_datetime(prices["loaded_at"])
    for column in ["brent", "wti", "dubai"]:
        prices[column] = prices[column].astype(float)
    prices = prices.drop_duplicates()
    prices = prices.sort_values(["date", "loaded_at"])
    prices = prices.drop_duplicates(subset="date", keep="last")
    prices = prices.set_index("date")[["brent", "wti", "dubai"]]
    prices.loc["2021-03-15", "brent"] = np.nan
    prices.index.name = "date"
    return prices.reset_index()


# ---------------------------------------------------------------------------
# Project 2 — refined products (daily prices) and diesel imports (monthly, long format)
# ---------------------------------------------------------------------------
def p2_products_daily(seed=11):
    dates = pd.bdate_range("2017-01-02", "2019-12-31")
    n = len(dates)
    rng = np.random.default_rng(seed)
    day_of_year = dates.dayofyear.values

    brent = 56.0 * np.exp(np.concatenate([[0.0], np.cumsum(rng.normal(0.0, 0.017, n - 1))]))
    # cracks in $/bbl: diesel peaks in winter (heating), gasoline in summer (driving season)
    diesel_crack = 17.0 + 3.5 * np.cos(2 * np.pi * (day_of_year - 15) / 365.25) + ar_noise(rng, n, 0.97, 0.45)
    gasoline_crack = 11.0 + 6.0 * np.cos(2 * np.pi * (day_of_year - 196) / 365.25) + ar_noise(rng, n, 0.97, 0.55)
    # a Gulf Coast hurricane shuts refineries: US product cracks jump and fade over weeks
    hit = dates >= "2017-08-28"
    days_since = np.cumsum(hit) - 1
    gasoline_crack = gasoline_crack + np.where(hit, 14.0 * np.exp(-days_since / 6.0), 0.0)
    diesel_crack = diesel_crack + np.where(hit, 6.0 * np.exp(-days_since / 6.0), 0.0)
    gasoil_crack = diesel_crack - 1.8 + ar_noise(rng, n, 0.95, 0.35)
    jet_crack = diesel_crack + 1.5 + ar_noise(rng, n, 0.95, 0.40)

    # ICE Gasoil settles ~2 hours before Brent and NYMEX: it misses part of today's crude move
    brent_move = np.concatenate([[0.0], np.diff(brent)])
    gasoil_bbl = brent + gasoil_crack - 0.35 * brent_move

    products = pd.DataFrame({
        "brent_usd_bbl": brent.round(2),
        "ulsd_usd_gal": ((brent + diesel_crack) / 42.0).round(4),
        "rbob_usd_gal": ((brent + gasoline_crack) / 42.0).round(4),
        "gasoil_usd_t": (gasoil_bbl * 7.45).round(2),
        "jet_usd_t": ((brent + jet_crack) * 7.88).round(2),
    }, index=dates)

    us = products.index.isin(pd.to_datetime(US_HOLIDAYS))
    uk = products.index.isin(pd.to_datetime(UK_HOLIDAYS))
    products.loc[us, ["ulsd_usd_gal", "rbob_usd_gal"]] = np.nan
    products.loc[uk, ["brent_usd_bbl", "gasoil_usd_t", "jet_usd_t"]] = np.nan
    products.loc[:"2018-02-28", "jet_usd_t"] = np.nan              # the jet assessment starts later
    products.loc[products.index[-3]:, "jet_usd_t"] = np.nan          # not yet published (ragged edge)
    frozen = (products.index >= "2018-10-08") & (products.index <= "2018-10-15")
    products.loc[frozen, "gasoil_usd_t"] = products.loc["2018-10-08", "gasoil_usd_t"]   # frozen feed
    products.loc["2019-05-14", "rbob_usd_gal"] = round(products.loc["2019-05-14", "rbob_usd_gal"] * 10, 4)

    products.index.name = "date"
    out = products.reset_index()
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    for day in ["2017-06-21", "2019-02-07"]:                          # two rows delivered twice
        position = out.index[out["date"] == day][0]
        out = pd.concat([out.loc[:position], out.loc[[position]], out.loc[position + 1:]], ignore_index=True)
    return out


def p2_treated_layer(raw):
    """Prices after the gap treatment of exercise 2.2: one row per date, stale runs of 4+ identical
    prices removed (first value kept), interior gaps forward-filled for at most 2 days.
    The RBOB fat-finger print is NOT removed here: that is the job of exercise 2.5."""
    products = raw.copy()
    products["date"] = pd.to_datetime(products["date"])
    products = products.set_index("date")
    products = products[~products.index.duplicated(keep="first")].sort_index()
    for column in products.columns:
        series = products[column]
        same_as_previous = series == series.shift(1)
        run_length = series.groupby((~same_as_previous).cumsum()).transform("count")
        products.loc[same_as_previous & (run_length >= 4), column] = np.nan
    products = products.ffill(limit=2, limit_area="inside")
    return products.reset_index()


def p2_diesel_imports_monthly(seed=12):
    months = pd.date_range("2017-01-01", "2019-12-01", freq="MS")
    rng = np.random.default_rng(seed)
    base = {("UK", "USA"): 95, ("UK", "Russia"): 120, ("UK", "Saudi Arabia"): 45, ("UK", "India"): 30,
            ("France", "USA"): 110, ("France", "Russia"): 160, ("France", "Saudi Arabia"): 70, ("France", "India"): 40,
            ("Germany", "USA"): 40, ("Germany", "Russia"): 180, ("Germany", "Saudi Arabia"): 35, ("Germany", "India"): 12,
            ("Netherlands", "USA"): 80, ("Netherlands", "Russia"): 210, ("Netherlands", "Saudi Arabia"): 60,
            ("Netherlands", "India"): 35}
    rows = []
    for month in months:
        winter = 1.0 + 0.12 * np.cos(2 * np.pi * (month.month - 1) / 12)
        for (importer, origin), level in base.items():
            volume = level * winter * (1 + rng.normal(0, 0.12))
            rows.append({"month": month.strftime("%Y-%m"), "importer": importer, "origin": origin,
                         "volume_kbd": round(max(volume, 0.0), 1)})
    imports = pd.DataFrame(rows)
    # genuine zeros: no cargo from that origin in that month
    genuine = [("Germany", "India", m) for m in ["2017-04", "2017-09", "2018-02", "2018-07", "2019-03", "2019-08"]]
    genuine += [("UK", "Saudi Arabia", m) for m in ["2017-11", "2018-12", "2019-06"]]
    for importer, origin, month in genuine:
        mask = (imports["importer"] == importer) & (imports["origin"] == origin) & (imports["month"] == month)
        imports.loc[mask, "volume_kbd"] = 0.0
    # non-reported months: the aggregator writes 0 for every origin
    for importer, month in [("France", "2018-08"), ("Netherlands", "2019-04")]:
        mask = (imports["importer"] == importer) & (imports["month"] == month)
        imports.loc[mask, "volume_kbd"] = 0.0
    # ragged edge: Germany has not reported December 2019 yet (rows absent)
    late = (imports["importer"] == "Germany") & (imports["month"] == "2019-12")
    return imports[~late].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Project 3 — weekly stocks with a release calendar, daily WTI, monthly demand vintages
# ---------------------------------------------------------------------------
MONDAY_HOLIDAYS = ["2016-01-18", "2016-02-15", "2016-05-30", "2016-09-05", "2017-01-16", "2017-02-20",
                   "2017-05-29", "2017-09-04", "2018-01-15", "2018-02-19", "2018-05-28", "2018-09-03",
                   "2019-01-21", "2019-02-18", "2019-05-27", "2019-09-02"]


def p3_stocks_and_wti(seed=49):
    rng = np.random.default_rng(seed)
    weeks = pd.date_range("2016-01-01", "2019-12-27", freq="W-FRI")
    # seasonal pattern of US crude stocks: builds in winter / spring, draws in summer
    expected_change = np.where(weeks.month.isin([1, 2, 3, 4]), 2.0,
                               np.where(weeks.month.isin([6, 7, 8, 9]), -2.5, 0.0))
    surprise = rng.normal(0.0, 3.0, len(weeks))
    change = expected_change + surprise
    stocks = 480.0 + np.cumsum(change)

    release = []
    for week_ending in weeks:
        monday = week_ending + pd.Timedelta(days=3)
        delay = 6 if monday.strftime("%Y-%m-%d") in MONDAY_HOLIDAYS else 5     # Wednesday, Thursday after a holiday
        release.append(week_ending + pd.Timedelta(days=delay))
    release = pd.DatetimeIndex(release)

    backfill_day = pd.Timestamp("2019-01-07 09:00")                 # the database was created that day
    ingested = []
    for day in release:
        if day < backfill_day:
            ingested.append(backfill_day)
        else:
            ingested.append(day + pd.Timedelta(hours=16, minutes=5))
    weekly = pd.DataFrame({"week_ending": weeks.strftime("%Y-%m-%d"),
                           "release_date": release.strftime("%Y-%m-%d"),
                           "release_time_et": "10:30",
                           "crude_stocks_mbbl": stocks.round(1),
                           "ingested_at": pd.DatetimeIndex(ingested).strftime("%Y-%m-%d %H:%M")})

    # WTI: ordinary daily noise, plus a reaction on release days to the stock surprise
    days = pd.bdate_range("2016-01-04", "2019-12-31")
    returns = rng.normal(0.0, 0.016, len(days))
    for i, day in enumerate(release):
        if day in days:
            returns[days.get_loc(day)] += -0.015 * surprise[i] / 3.0     # a 3 mbbl surprise moves WTI ~1.5 %
    wti = 37.0 * np.exp(np.cumsum(returns))
    daily = pd.DataFrame({"date": days.strftime("%Y-%m-%d"), "wti_usd_bbl": wti.round(2)})
    return weekly, daily


def p3_demand_vintages(seed=32):
    rng = np.random.default_rng(seed)
    months = pd.date_range("2015-01-01", "2019-12-01", freq="MS")
    n = len(months)
    season = 250.0 * np.cos(2 * np.pi * (months.month - 7) / 12)            # driving season peak
    cycle = 180.0 * np.sin(2 * np.pi * np.arange(n) / 40.0)                 # slow activity cycle
    true_demand = 19500.0 + 12.0 * np.arange(n) + season + cycle + ar_noise(rng, n, 0.9, 50.0)

    rows = []
    for i, month in enumerate(months):
        first = month + pd.offsets.MonthEnd(3)          # first estimate: end of month + 2
        second = month + pd.offsets.MonthEnd(4)         # second estimate one month later
        annual = pd.Timestamp("%d-08-31" % (month.year + 1))   # annual revision of the previous year
        estimates = [(first, true_demand[i] - 150.0 + rng.normal(0, 110.0)),
                     (second, true_demand[i] - 50.0 + rng.normal(0, 45.0)),
                     (annual, true_demand[i])]
        for vintage_date, value in estimates:
            rows.append({"obs_month": month.strftime("%Y-%m"),
                         "vintage_date": vintage_date.strftime("%Y-%m-%d"),
                         "demand_kbd": round(value, 0)})
    vintages = pd.DataFrame(rows)

    # monthly average diesel crack: the market reacts to TRUE demand conditions as they happen
    growth = pd.Series(true_demand, index=months).pct_change(12) * 100
    crack = 16.0 + 1.1 * growth.fillna(0.0).values + rng.normal(0, 0.9, n)
    crack_monthly = pd.DataFrame({"month": months.strftime("%Y-%m"), "diesel_crack_usd_bbl": crack.round(2)})
    return vintages, crack_monthly


# ---------------------------------------------------------------------------
# Project 4 — crude research panel 2012-2019 and monthly diesel demand
# ---------------------------------------------------------------------------
def p4_crude_research(seed_brent=61, seed_wti=1061, seed_coffee=2299, seed_dubai=4061):
    """Brent: log random walk. WTI: error-correction dynamics around log WTI = a + log Brent,
    with a regime change on 2016-01-01 (end of the export ban): discount 16 % -> 6 %,
    short-run pass-through 0.60 -> 0.90, adjustment 5 % -> 10 % of the gap per day.
    Dubai: Brent plus a small stationary differential. Coffee: independent of crude."""
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

    d = b - 0.025 + ar_noise(np.random.default_rng(seed_dubai), n, 0.9, 0.006)

    return pd.DataFrame({"date": dates.strftime("%Y-%m-%d"),
                         "brent": np.round(np.exp(b), 2),
                         "wti": np.round(np.exp(w), 2),
                         "dubai": np.round(np.exp(d), 2),
                         "coffee": np.round(np.exp(c), 2)})


def p4_diesel_demand_monthly(seed=1):
    """Monthly diesel demand, kb/d: linear trend + fixed seasonal profile + short-memory noise."""
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


def main():
    def save(frame, name):
        frame.to_csv(os.path.join(HERE, name), index=False)

    raw = p1_crude_vendor_file()
    save(raw, "p1_crude_prices_vendor_synthetic.csv")
    clean = p1_clean_layer(raw)
    clean["date"] = clean["date"].dt.strftime("%Y-%m-%d")
    save(clean, "p1_crude_prices_clean_synthetic.csv")
    products = p2_products_daily()
    save(products, "p2_products_daily_synthetic.csv")
    treated = p2_treated_layer(products)
    treated["date"] = treated["date"].dt.strftime("%Y-%m-%d")
    save(treated, "p2_products_treated_synthetic.csv")
    save(p2_diesel_imports_monthly(), "p2_diesel_imports_monthly_synthetic.csv")
    weekly, daily = p3_stocks_and_wti()
    save(weekly, "p3_us_crude_stocks_weekly_synthetic.csv")
    save(daily, "p3_wti_daily_synthetic.csv")
    vintages, crack = p3_demand_vintages()
    save(vintages, "p3_us_oil_demand_vintages_synthetic.csv")
    save(crack, "p3_diesel_crack_monthly_synthetic.csv")
    save(p4_crude_research(), "p4_crude_research_daily_synthetic.csv")
    save(p4_diesel_demand_monthly(), "p4_diesel_demand_monthly_synthetic.csv")
    print("written to", HERE)


if __name__ == "__main__":
    main()
