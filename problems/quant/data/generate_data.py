#!/usr/bin/env python3
"""Rebuild the SYNTHETIC datasets of the Quantitative Methods track.

    python3 problems/quant/data/generate_data.py

Every value is simulated with a fixed seed. None of it is market data: dates, units, calendars
and orders of magnitude are realistic so that the economic reading makes sense, and some
well-known episodes (a Gulf Coast hurricane, the 2020 price war and lockdowns, a 2022-style
distillate squeeze, the end of the US crude export ban, a cold and windless winter week) are
*imitated*, but the numbers are invented. The power market, its zones and weather stations are
fictional.

Two kinds of files are written:
- raw files, deliberately imperfect (each defect is the subject of an exercise);
- derived layers (clean / treated tables) that later exercises start from. They are produced
  by running the REFERENCE SOLUTION of the exercise that builds them, so a derived file is
  always exactly what a correct answer to that exercise returns.

numpy does not promise identical random streams across major versions: re-running this script
on another numpy may change the last digits. The committed CSV files are the reference.
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PROBLEMS = os.path.dirname(HERE)


def ar1(rng, n, phi, sd):
    """Stationary noise: each step keeps a share phi of the previous deviation."""
    e = rng.normal(0.0, sd, n)
    x = np.zeros(n)
    for t in range(n):
        x[t] = (phi * x[t - 1] if t else 0.0) + e[t]
    return x




# ---------------------------------------------------------------------------
# Project 1 — Gas & Power: hourly market data, zone load, weather (fictional market)
# ---------------------------------------------------------------------------
MARKET_TZ = "Europe/Paris"
ZONES = pd.DataFrame({
    "zone": ["NORTH", "CENTRAL", "SOUTH"],
    "description": ["northern zone: electric heating, mild summers",
                    "central zone: largest load, mixed heating and cooling",
                    "southern zone: air conditioning, mild winters"],
    "station": ["N-01 (synthetic)", "C-04 (synthetic)", "S-07 (synthetic)"],
    "hdd_base_c": [15.5, 16.0, 17.0],
    "cdd_base_c": [20.0, 22.0, 21.0],
})
CLIMATE = {"NORTH": (7.5, 8.5), "CENTRAL": (10.5, 9.0), "SOUTH": (14.5, 8.0)}    # annual mean, amplitude
LOAD = {"NORTH": (9000.0, 260.0, 40.0), "CENTRAL": (14000.0, 180.0, 150.0), "SOUTH": (7000.0, 60.0, 320.0)}
PROFILE = np.array([0.82, 0.78, 0.76, 0.75, 0.76, 0.80, 0.90, 1.02, 1.08, 1.09, 1.08, 1.07,
                    1.06, 1.04, 1.03, 1.03, 1.06, 1.12, 1.16, 1.14, 1.08, 1.00, 0.93, 0.86])
PROFILE = PROFILE / PROFILE.mean()




def bump(days, start, end, depth, ramp=2):
    """Smooth anomaly between two dates (ramps of `ramp` days)."""
    s, e = pd.Timestamp(start), pd.Timestamp(end)
    out = np.zeros(len(days))
    for i, d in enumerate(days):
        if s - pd.Timedelta(days=ramp) <= d <= e + pd.Timedelta(days=ramp):
            if d < s:
                w = 1 - (s - d).days / (ramp + 1)
            elif d > e:
                w = 1 - (d - e).days / (ramp + 1)
            else:
                w = 1.0
            out[i] = depth * w
    return out


def climatology(zone, doy):
    mean, amp = CLIMATE[zone]
    return mean - amp * np.cos(2 * np.pi * (doy - 20) / 365.25)


def weather_normals(seed=500, years=30):
    """'30-year' normals: mean daily HDD / CDD by zone and calendar month, simulated with the
    same climate (no special events)."""
    rng = np.random.default_rng(seed)
    days = pd.date_range("1991-01-01", periods=365 * years, freq="D")
    rows = []
    shared = ar1(rng, len(days), 0.8, 1.6)
    for _, z in ZONES.iterrows():
        own = ar1(rng, len(days), 0.8, 1.0)
        t = climatology(z["zone"], days.dayofyear.values) + 0.8 * shared + 0.6 * own
        hdd = np.maximum(z["hdd_base_c"] - t, 0)
        cdd = np.maximum(t - z["cdd_base_c"], 0)
        frame = pd.DataFrame({"month": days.month, "t": t, "hdd": hdd, "cdd": cdd})
        g = frame.groupby("month").mean()
        for m, r in g.iterrows():
            rows.append({"zone": z["zone"], "month": int(m), "normal_temp_c": round(r["t"], 1),
                         "normal_hdd": round(r["hdd"], 2), "normal_cdd": round(r["cdd"], 2)})
    return pd.DataFrame(rows)


def power_world(seed=23):
    rng = np.random.default_rng(seed)
    days = pd.date_range("2022-12-25", "2025-01-05", freq="D")          # padding around 2023-2024
    doy = days.dayofyear.values
    # --- daily temperature anomalies: shared European weather + zone noise + planted episodes
    shared = ar1(rng, len(days), 0.8, 1.6)
    shared += bump(days, "2023-01-02", "2023-02-10", 2.0, 5)            # mild Jan 2023
    shared += bump(days, "2024-01-01", "2024-02-20", -1.2, 5)           # colder Jan-Feb 2024
    shared += bump(days, "2024-01-08", "2024-01-19", -6.5, 3)           # cold, still spell
    shared += bump(days, "2023-12-11", "2023-12-15", -4.0, 2)
    shared += bump(days, "2023-08-18", "2023-08-25", 5.5, 2)            # heat waves
    shared += bump(days, "2024-07-29", "2024-08-02", 5.0, 2)
    temps = {}
    for _, z in ZONES.iterrows():
        own = ar1(rng, len(days), 0.8, 1.0)
        temps[z["zone"]] = climatology(z["zone"], doy) + 0.8 * shared + 0.6 * own
    daily = pd.DataFrame(temps, index=days)
    # still air during cold spells: a daily wind factor partly driven by the shared anomaly
    winter = np.isin(days.month, [11, 12, 1, 2, 3])
    wind_state = ar1(rng, len(days), 0.75, 0.55) + np.where(winter, 0.12 * shared, 0.0)
    wind_state += np.where(winter, 0.25, -0.15)
    wind_state += bump(days, "2024-01-08", "2024-01-19", -0.9, 2)
    wind_state += bump(days, "2023-10-02", "2023-10-13", -0.2, 1)
    cloud = np.clip(0.75 + ar1(rng, len(days), 0.6, 0.18), 0.15, 1.0)
    return days, daily, wind_state, cloud, shared, rng


def build_p1(seed=23):
    days, daily_t, wind_state, cloud, shared, rng = power_world(seed)
    hours = pd.date_range("2022-12-31 23:00", "2024-12-31 22:00", freq="h", tz="UTC")
    local = hours.tz_convert(MARKET_TZ)
    local_day = pd.DatetimeIndex(local.tz_localize(None).normalize())
    lhour = local.hour.values
    day_pos = days.get_indexer(local_day)
    weekend = local_day.dayofweek.values >= 5
    year24 = local_day.year.values == 2024

    # --- hourly temperature by zone: daily mean + diurnal cycle (min 05:00, max 15:00 local)
    diurnal = 3.5 * np.cos(2 * np.pi * (lhour - 15) / 24)
    zone_load = {}
    zone_temp = {}
    for _, z in ZONES.iterrows():
        name = z["zone"]
        tmean = daily_t[name].values[day_pos]
        zone_temp[name] = tmean + diurnal + rng.normal(0, 0.4, len(hours))
        hdd = np.maximum(z["hdd_base_c"] - tmean, 0)
        cdd = np.maximum(tmean - z["cdd_base_c"], 0)
        base, b_h, b_c = LOAD[name]
        level = base * np.where(year24, 0.975, 1.0) * np.where(weekend, 0.88, 1.0)
        dnoise = ar1(rng, len(days), 0.5, 0.015 * base)[day_pos]
        day_avg = level + b_h * hdd + b_c * cdd + dnoise
        zone_load[name] = day_avg * PROFILE[lhour] * (1 + rng.normal(0, 0.01, len(hours)))
    load = sum(zone_load.values())

    # --- wind: hourly capacity factor around the daily weather state
    cap_w = np.where(year24, 24000.0, 22000.0)
    x = wind_state[day_pos] + ar1(rng, len(hours), 0.9, 0.18)
    cf_w = 1 / (1 + np.exp(-(x - 0.75) * 2.2))
    wind = cap_w * np.clip(cf_w, 0.01, 0.92)
    # --- solar: daylight bell (solar noon ~13:20 local summer / 12:20 winter) x season x clouds
    cap_s = np.where(year24, 20000.0, 16000.0)
    doy = local_day.dayofyear.values
    day_len = 12 + 4.2 * np.sin(2 * np.pi * (doy - 80) / 365.25)
    solar_hour = hours.hour.values + 0.5 + 0.7          # UTC + ~0.7 h longitude
    angle = np.pi * (solar_hour - 12.2) / day_len
    bell = np.where(np.abs(solar_hour - 12.2) < day_len / 2, np.cos(angle), 0.0) ** 1.4
    peak = 0.42 + 0.33 * np.sin(2 * np.pi * (doy - 80) / 365.25)
    solar = cap_s * peak * bell * cloud[day_pos]
    solar = np.where(solar < 5, 0.0, solar)

    # --- dispatchable capacity (daily state) and gas
    month = local_day.month.values
    cap = 49500.0 - 6500.0 * np.isin(month, [5, 6, 7, 8, 9]) - 3000.0 * np.isin(month, [4, 10])
    out_oct = (local_day >= "2023-10-02") & (local_day <= "2023-10-13")
    cap = np.where(out_oct, cap - 8000.0, cap)
    cold = (local_day >= "2024-01-10") & (local_day <= "2024-01-18")
    cap = np.where(cold, cap - 1500.0, cap)
    cap_noise = ar1(rng, len(days), 0.9, 300.0)[day_pos]
    cap = np.round((cap + cap_noise) / 10) * 10
    knots = pd.Series({"2022-12-25": 78, "2023-02-15": 52, "2023-04-15": 42, "2023-06-01": 28,
                       "2023-08-15": 36, "2023-10-15": 45, "2023-12-15": 38, "2024-02-20": 26,
                       "2024-05-15": 32, "2024-08-15": 38, "2024-11-15": 45, "2025-01-05": 48})
    anchor = np.interp(days.asi8, pd.to_datetime(knots.index).asi8, knots.values.astype(float))
    gas_daily = anchor * np.exp(ar1(rng, len(days), 0.9, 0.025))
    gas = gas_daily[day_pos]

    # --- price: merit order on residual load / available capacity, scarcity above ~80 %
    residual = load - wind - solar
    u = residual / cap
    price = gas * (0.45 + 1.9 * u ** 2) + 12 * np.exp((u - 0.80) / 0.045) * (u > 0.80)
    price = price - 70 * np.clip((0.11 - u) / 0.11, 0, None) - 12 * (u < 0.11)
    price = price * np.exp(rng.normal(0, 0.06, len(hours))) + rng.normal(0, 3, len(hours))
    price = np.minimum(price, 4000.0)

    world = pd.DataFrame({"utc": hours, "local": local, "local_date": local_day, "local_hour": lhour,
                          "price": price, "load": load, "wind": wind, "solar": solar, "cap": cap,
                          "gas": gas, "u": u, "residual": residual})
    for name in zone_load:
        world["load_" + name] = zone_load[name]
        world["temp_" + name] = zone_temp[name]
    return world


def fmt_utc(index):
    return pd.DatetimeIndex(index).tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


def p1_files(seed=23):
    w = build_p1(seed)
    rng = np.random.default_rng(seed + 1000)
    local = pd.DatetimeIndex(w["local"])
    offset = local.strftime("%z")
    offset = [o[:3] + ":" + o[3:] for o in offset]
    # the vendor loads each delivery day the morning after (06:00 local), once actual load and
    # generation are known; a correction is loaded later as a new version of the same record
    pub_local = (w["local_date"] + pd.Timedelta(days=1) + pd.Timedelta(hours=6)).dt.tz_localize(MARKET_TZ)
    vendor = pd.DataFrame({
        "delivery_start_local": local.strftime("%Y-%m-%d %H:%M"),
        "utc_offset": offset,
        "price_eur_mwh": w["price"].round(2),
        "load_mw": w["load"].round(0),
        "wind_mw": w["wind"].round(0),
        "solar_mw": w["solar"].round(0),
        "available_capacity_mw": w["cap"].round(0),
        "gas_eur_mwh": w["gas"].round(2),
        "loaded_at_utc": fmt_utc(pub_local),
    })
    key = vendor["delivery_start_local"]
    # solar blank when there is no production (vendor convention)
    vendor.loc[vendor["solar_mw"] <= 0, "solar_mw"] = np.nan
    # capacity: a daily figure, sent with the first hour of each local day only
    vendor.loc[w["local_hour"].values != 0, "available_capacity_mw"] = np.nan
    for day in ["2023-05-08"] + list(pd.date_range("2024-09-02", "2024-09-06").strftime("%Y-%m-%d")):
        vendor.loc[key == day + " 00:00", "available_capacity_mw"] = np.nan
    # feed failures
    def local_range(start, end):
        return (key >= start) & (key <= end)
    vendor.loc[local_range("2023-11-14 08:00", "2023-11-14 19:00"), "wind_mw"] = np.nan
    vendor.loc[local_range("2024-02-06 03:00", "2024-02-06 05:00"), "wind_mw"] = np.nan
    vendor.loc[local_range("2024-05-16 03:00", "2024-05-16 04:00"), "price_eur_mwh"] = np.nan
    vendor.loc[local_range("2024-06-12 10:00", "2024-06-12 14:00"), "solar_mw"] = np.nan
    # three records first published wrong, then re-published (correction appended at the end)
    corrections = []
    fixes = [("2023-11-21 18:00", "price_eur_mwh", lambda v: round(v * 10, 1), "2023-11-23 09:15"),
             ("2024-03-12 19:00", "price_eur_mwh", None, "2024-03-14 08:40"),
             ("2024-06-03 13:00", "solar_mw", lambda v: np.nan, "2024-06-05 10:05")]
    for when, column, wrong, republished in fixes:
        mask = key == when
        good = vendor.loc[mask].copy()
        good["loaded_at_utc"] = fmt_utc(pd.DatetimeIndex([pd.Timestamp(republished)]).tz_localize(MARKET_TZ))[0]
        corrections.append(good)
        value = vendor.loc[mask, column].iloc[0]
        if wrong is None:
            text = "%.2f" % value
            swapped = text[1] + text[0] + text[2:]          # two digits swapped
            vendor.loc[mask, column] = float(swapped)
        else:
            vendor.loc[mask, column] = wrong(value)
    out = pd.concat([vendor] + corrections, ignore_index=True)
    # six records sent twice, identically
    for when in ["2023-02-07 09:00", "2023-06-19 15:00", "2023-09-01 00:00", "2024-01-23 18:00",
                 "2024-08-14 11:00", "2024-12-02 07:00"]:
        pos = out.index[out["delivery_start_local"] == when][0]
        out = pd.concat([out.loc[:pos], out.loc[[pos]], out.loc[pos + 1:]], ignore_index=True)

    # --- zone load, UTC, long
    rows = []
    for zone in ZONES["zone"]:
        frame = pd.DataFrame({"delivery_start_utc": fmt_utc(w["utc"]), "zone": zone,
                              "load_mw": w["load_" + zone].round(0)})
        rows.append(frame)
    zone_load = pd.concat(rows, ignore_index=True)
    stamp = zone_load["delivery_start_utc"]
    gap = (zone_load["zone"] == "SOUTH") & (stamp >= "2024-03-05T06:00:00Z") & (stamp <= "2024-03-05T13:00:00Z")
    zone_load = zone_load[~gap]
    zone_load.loc[(zone_load["zone"] == "NORTH") & (zone_load["delivery_start_utc"] == "2023-07-19T03:00:00Z"), "load_mw"] = np.nan
    zone_load = zone_load.reset_index(drop=True)

    # --- temperature observations, UTC, irregular
    rows = []
    hours = pd.DatetimeIndex(w["utc"])
    for zone in ZONES["zone"]:
        t = w["temp_" + zone].values
        main = rng.random(len(hours)) < 0.97
        extra = rng.random(len(hours)) < 0.06
        obs_main = pd.DataFrame({"observed_at": hours[main] + pd.Timedelta(minutes=50), "zone": zone,
                                 "temperature_c": (t[main] + 0.3 * rng.normal(0, 1, main.sum())).round(1)})
        nxt = np.r_[t[1:], t[-1]]
        obs_extra = pd.DataFrame({"observed_at": hours[extra] + pd.Timedelta(minutes=20), "zone": zone,
                                  "temperature_c": ((2 * t[extra] + nxt[extra]) / 3).round(1)})
        rows += [obs_main, obs_extra]
    obs = pd.concat(rows, ignore_index=True)
    outage = (obs["zone"] == "NORTH") & (obs["observed_at"] >= "2023-02-14 00:00") & (obs["observed_at"] < "2023-02-15 12:00")
    obs = obs[~outage]
    obs = obs.sort_values(["observed_at", "zone"]).reset_index(drop=True)
    bad = obs.index[(obs["zone"] == "SOUTH") & (obs["observed_at"] == pd.Timestamp("2023-07-04 12:50", tz="UTC"))]
    obs.loc[bad, "temperature_c"] = 99.9                  # sensor error code
    obs["observed_at_utc"] = fmt_utc(obs["observed_at"])
    obs = obs[["observed_at_utc", "zone", "temperature_c"]]
    return {"vendor": out, "zone_load": zone_load, "temps": obs, "zones": ZONES.copy(),
            "normals": weather_normals(), "world": w}


# ---------------------------------------------------------------------------
# Project 2 — oil products: daily prices (long), events, imports, outages, fundamentals
# ---------------------------------------------------------------------------
US_HOL = ["2017-01-02","2017-01-16","2017-02-20","2017-04-14","2017-05-29","2017-07-04","2017-09-04","2017-11-23","2017-12-25",
          "2018-01-01","2018-01-15","2018-02-19","2018-03-30","2018-05-28","2018-07-04","2018-09-03","2018-11-22","2018-12-25",
          "2019-01-01","2019-01-21","2019-02-18","2019-04-19","2019-05-27","2019-07-04","2019-09-02","2019-11-28","2019-12-25",
          "2020-01-01","2020-01-20","2020-02-17","2020-04-10","2020-05-25","2020-07-03","2020-09-07","2020-11-26","2020-12-25",
          "2021-01-01","2021-01-18","2021-02-15","2021-04-02","2021-05-31","2021-07-05","2021-09-06","2021-11-25","2021-12-24",
          "2022-01-17","2022-02-21","2022-04-15","2022-05-30","2022-06-20","2022-07-04","2022-09-05","2022-11-24","2022-12-26",
          "2023-01-02","2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19"]
UK_HOL = ["2017-01-02","2017-04-14","2017-04-17","2017-05-01","2017-05-29","2017-08-28","2017-12-25","2017-12-26",
          "2018-01-01","2018-03-30","2018-04-02","2018-05-07","2018-05-28","2018-08-27","2018-12-25","2018-12-26",
          "2019-01-01","2019-04-19","2019-04-22","2019-05-06","2019-05-27","2019-08-26","2019-12-25","2019-12-26",
          "2020-01-01","2020-04-10","2020-04-13","2020-05-08","2020-05-25","2020-08-31","2020-12-25","2020-12-28",
          "2021-01-01","2021-04-02","2021-04-05","2021-05-03","2021-05-31","2021-08-30","2021-12-27","2021-12-28",
          "2022-01-03","2022-04-15","2022-04-18","2022-05-02","2022-06-02","2022-06-03","2022-08-29","2022-09-19","2022-12-26","2022-12-27",
          "2023-01-02","2023-04-07","2023-04-10","2023-05-01","2023-05-08","2023-05-29"]




def anchor(dates, knots):
    k = pd.Series(knots)
    return np.interp(dates.asi8, pd.to_datetime(k.index).asi8, k.values.astype(float))


def p2_monthly_world(seed=31):
    rng = np.random.default_rng(seed)
    months = pd.date_range("2017-01-01", "2023-06-01", freq="MS")
    n = len(months)
    # middle-distillate stocks vs their 5-year average (%): glut in 2020, very tight in 2022
    dev = anchor(months, {"2017-01-01": 2, "2018-06-01": -4, "2019-06-01": 0, "2020-01-01": 1, "2020-06-01": 14,
                          "2020-12-01": 10, "2021-06-01": 2, "2021-12-01": -9, "2022-05-01": -20, "2022-10-01": -26,
                          "2023-01-01": -15, "2023-06-01": -8}) + ar1(rng, n, 0.6, 2.2)
    util = 86.5 + ar1(rng, n, 0.6, 1.2) - 9 * ((months >= "2020-04-01") & (months <= "2020-09-01"))
    # refinery outages, kb/d offline (monthly average) come from the event list
    return months, dev, util, rng


OUTAGES = [  # refinery, region, start, end, capacity offline kb/d, cause
    ("Gulf Coast cluster", "US Gulf Coast", "2017-08-25", "2017-09-20", 2200, "hurricane"),
    ("Rotterdam R2", "NW Europe", "2017-11-06", "2017-11-30", 180, "fire"),
    ("Antwerp A1", "NW Europe", "2018-03-12", "2018-04-15", 140, "planned maintenance"),
    ("Pernis P3", "NW Europe", "2018-09-03", "2018-10-05", 200, "planned maintenance"),
    ("Philadelphia PE", "US East Coast", "2019-06-21", "2019-12-31", 330, "fire"),
    ("Grandpuits G1", "France", "2019-10-01", "2019-10-25", 100, "planned maintenance"),
    ("Leuna L1", "Germany", "2020-04-01", "2020-05-31", 220, "economic run cuts"),
    ("Lake Charles LC", "US Gulf Coast", "2020-08-26", "2020-09-15", 750, "hurricane"),
    ("Gulf Coast cluster", "US Gulf Coast", "2021-02-15", "2021-03-05", 1800, "winter storm"),
    ("Ida cluster", "US Gulf Coast", "2021-08-29", "2021-09-20", 900, "hurricane"),
    ("Schwedt S1", "Germany", "2022-04-01", "2022-05-15", 120, "crude supply"),
    ("French strikes", "France", "2022-09-27", "2022-11-08", 650, "strike"),
    ("Pernis P3", "NW Europe", "2023-02-06", "2023-03-10", 200, "planned maintenance"),
    ("French strikes", "France", "2023-03-07", "2023-03-31", 400, "strike"),
]


def outage_monthly(months):
    rows = []
    for name, region, start, end, kbd, cause in OUTAGES:
        days = pd.date_range(start, end, freq="D")
        rows.append(pd.DataFrame({"day": days, "kbd": kbd}))
    daily = pd.concat(rows)
    daily["month"] = daily["day"].dt.to_period("M").dt.to_timestamp()
    total = daily.groupby("month")["kbd"].sum()
    days_in = pd.Series(months.days_in_month, index=months)
    return (total.reindex(months).fillna(0.0) / days_in).values


def p2_build(seed=31):
    months, dev, util, rng = p2_monthly_world(seed)
    out_kbd = outage_monthly(months)
    sd = 0.5 + 0.42 * np.clip(-dev, 0, None)
    crack_m = 13.5 - 0.85 * dev + 0.004 * out_kbd + 0.035 * np.clip(-dev - 8, 0, None) ** 2 + rng.normal(0, 1, len(months)) * sd
    crack_m = crack_m - 6 * ((months >= "2020-04-01") & (months <= "2020-07-01"))
    return months, dev, util, out_kbd, crack_m


EVENTS = [  # start, end, event, markets
    ("2017-08-25", "2017-09-15", "Hurricane shuts Gulf Coast refineries", "ulsd;rbob;jet"),
    ("2020-03-09", "2020-03-10", "OPEC+ talks collapse, price war", "brent;gasoil;ulsd;rbob;jet"),
    ("2020-03-16", "2020-05-29", "Lockdowns: jet fuel demand collapses", "jet"),
    ("2022-02-24", "2022-03-15", "Invasion of Ukraine: distillate supply fears", "brent;gasoil;ulsd;jet"),
    ("2022-09-27", "2022-11-08", "French refinery strikes", "gasoil;jet"),
    ("2022-10-26", "2022-11-07", "New York Harbor distillate squeeze", "ulsd"),
]


def p2_daily(seed=37):
    months, dev, util, out_kbd, crack_m = p2_build()
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2017-01-02", "2023-06-30")
    n = len(dates)
    brent_anchor = anchor(dates, {"2017-01-02": 56, "2017-06-21": 45, "2018-01-15": 69, "2018-10-03": 86, "2018-12-24": 50,
                                  "2019-04-25": 75, "2019-12-31": 66, "2020-01-07": 68, "2020-03-06": 50, "2020-03-09": 39,
                                  "2020-04-21": 19, "2020-06-30": 41, "2020-12-31": 51, "2021-07-05": 77, "2021-10-25": 86,
                                  "2021-12-01": 69, "2022-03-08": 125, "2022-06-14": 122, "2022-09-26": 84, "2022-11-07": 98,
                                  "2022-12-09": 76, "2023-04-12": 87, "2023-06-30": 75})
    shocks = rng.standard_t(5, n) / np.sqrt(5 / 3) * 0.014
    log_brent = np.log(brent_anchor)
    dev_noise = np.zeros(n)
    for t in range(n):
        dev_noise[t] = (0.94 * dev_noise[t - 1] if t else 0) + shocks[t]
    brent = np.exp(log_brent + dev_noise)
    # monthly crack level -> daily, plus fat-tailed daily noise
    month_mid = months + pd.Timedelta(days=14)
    level = np.interp(dates.asi8, month_mid.asi8, crack_m)
    tight = np.interp(dates.asi8, month_mid.asi8, np.clip(-dev, 0, None))
    crack_noise = np.zeros(n)
    t_shock = rng.standard_t(5, n) / np.sqrt(5 / 3) * (0.5 + 0.06 * tight)
    for t in range(n):
        crack_noise[t] = (0.9 * crack_noise[t - 1] if t else 0) + t_shock[t]
    gasoil_crack = level + crack_noise
    doy = dates.dayofyear.values
    ulsd_crack = gasoil_crack + 4.0 + ar1(rng, n, 0.9, 0.6)
    rbob_crack = 10.0 + 7.0 * np.cos(2 * np.pi * (doy - 196) / 365.25) + ar1(rng, n, 0.95, 0.7)
    jet_crack = gasoil_crack + 1.5 + ar1(rng, n, 0.9, 0.5)
    def fade(start, size, tau):
        hit = dates >= start
        since = np.cumsum(hit) - 1
        return np.where(hit, size * np.exp(-since / tau), 0.0)
    ulsd_crack += fade("2017-08-28", 9.0, 6.0)
    rbob_crack += fade("2017-08-28", 16.0, 6.0)
    jet_crack += fade("2017-08-28", 7.0, 6.0)
    covid = anchor(dates, {"2017-01-02": 0, "2020-03-13": 0, "2020-04-03": 11, "2020-06-01": 11, "2020-07-31": 0, "2023-06-30": 0})
    jet_crack = jet_crack - covid
    invasion = fade("2022-02-24", 12.0, 12.0)
    gasoil_crack += invasion
    ulsd_crack += invasion
    jet_crack += invasion
    ulsd_crack += fade("2022-10-31", 24.0, 3.0)
    jet_doubt = dates.get_loc(pd.Timestamp("2021-06-15"))
    jet_crack[jet_doubt] += 8.5
    jet_crack[jet_doubt + 1] += 3.0
    gasoil_bbl = brent + gasoil_crack
    wide = pd.DataFrame({"brent": brent, "gasoil": gasoil_bbl, "ulsd": brent + ulsd_crack,
                         "rbob": brent + rbob_crack, "jet": brent + jet_crack}, index=dates)
    return wide


BBL_PER_T = {"gasoil": 7.45, "jet": 7.88}


def p2_files():
    wide = p2_daily()
    dates = wide.index
    rows = []
    units = {"brent": "USD/bbl", "gasoil": "USD/t", "ulsd": "USD/gal", "rbob": "USD/gal", "jet": "USD/t"}
    us = dates.isin(pd.to_datetime(US_HOL))
    uk = dates.isin(pd.to_datetime(UK_HOL))
    for product in ["brent", "gasoil", "ulsd", "rbob", "jet"]:
        bbl = wide[product].values
        unit = np.array([units[product]] * len(dates), dtype=object)
        if product in BBL_PER_T:
            value = np.round(bbl * BBL_PER_T[product], 2)
        elif units[product] == "USD/gal":
            value = np.round(bbl / 42.0, 4)
        else:
            value = np.round(bbl, 2)
        if product == "ulsd":                       # the vendor quoted ULSD in cents until end-2020
            cents = dates < "2021-01-01"
            unit[cents] = "USc/gal"
            value = np.where(cents, np.round(bbl / 0.42, 2), value)
        keep = np.ones(len(dates), bool)
        if product in ["ulsd", "rbob"]:
            keep &= ~us
        else:
            keep &= ~uk
        if product == "jet":
            keep &= dates >= "2018-03-01"           # the jet assessment starts later
            keep[-3:] = False                       # not yet published (ragged edge)
        frame = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "product": product, "unit": unit, "price": value})
        rows.append(frame[keep])
    raw = pd.concat(rows, ignore_index=True)
    def at(day, product):
        return (raw["date"] == day) & (raw["product"] == product)
    # frozen gasoil feed: the same price repeated for six sessions
    frozen = (raw["product"] == "gasoil") & (raw["date"] >= "2018-10-08") & (raw["date"] <= "2018-10-15")
    raw.loc[frozen, "price"] = raw.loc[at("2018-10-08", "gasoil"), "price"].iloc[0]
    # RBOB sent in cents per gallon under a USD/gal label
    raw.loc[at("2019-05-14", "rbob"), "price"] = np.round(raw.loc[at("2019-05-14", "rbob"), "price"] * 100, 2)
    # an impossible print
    raw.loc[at("2021-11-25", "gasoil"), "price"] = 0.0
    # sort by date then product, as a vendor export would be
    raw = raw.sort_values(["date", "product"]).reset_index(drop=True)
    for day, product in [("2017-06-21", "ulsd"), ("2019-02-07", "gasoil"), ("2022-03-07", "brent")]:
        pos = raw.index[at(day, product)][0]
        raw = pd.concat([raw.loc[:pos], raw.loc[[pos]], raw.loc[pos + 1:]], ignore_index=True)
    events = pd.DataFrame(EVENTS, columns=["start", "end", "event", "markets"])
    outages = pd.DataFrame(OUTAGES, columns=["refinery", "region", "start", "end", "offline_kbd", "cause"])
    return raw, events, outages, wide


def p2_imports(seed=12):
    months = pd.date_range("2017-01-01", "2023-06-01", freq="MS")
    rng = np.random.default_rng(seed)
    base = {("UK", "USA"): 95, ("UK", "Russia"): 120, ("UK", "Saudi Arabia"): 45, ("UK", "India"): 30,
            ("France", "USA"): 110, ("France", "Russia"): 160, ("France", "Saudi Arabia"): 70, ("France", "India"): 40,
            ("Germany", "USA"): 40, ("Germany", "Russia"): 180, ("Germany", "Saudi Arabia"): 35, ("Germany", "India"): 12,
            ("Netherlands", "USA"): 80, ("Netherlands", "Russia"): 210, ("Netherlands", "Saudi Arabia"): 60,
            ("Netherlands", "India"): 35}
    rows = []
    for month in months:
        winter = 1.0 + 0.12 * np.cos(2 * np.pi * (month.month - 1) / 12)
        covid = 0.8 if "2020-04-01" <= month.strftime("%Y-%m-%d") <= "2020-09-01" else 1.0
        for (importer, origin), level in base.items():
            if origin == "Russia" and month >= pd.Timestamp("2023-02-01"):
                level = 0.0                                   # EU embargo on Russian products
            elif origin in ("India", "Saudi Arabia", "USA") and month >= pd.Timestamp("2023-02-01"):
                level = level * 1.9                           # replacement barrels
            volume = level * winter * covid * (1 + rng.normal(0, 0.12))
            rows.append({"month": month.strftime("%Y-%m"), "importer": importer, "origin": origin,
                         "volume_kbd": round(max(volume, 0.0), 1)})
    imports = pd.DataFrame(rows)
    genuine = [("Germany", "India", m) for m in ["2017-04", "2017-09", "2018-02", "2018-07", "2019-03", "2019-08", "2021-05"]]
    genuine += [("UK", "Saudi Arabia", m) for m in ["2017-11", "2018-12", "2019-06", "2022-01"]]
    for importer, origin, month in genuine:
        mask = (imports["importer"] == importer) & (imports["origin"] == origin) & (imports["month"] == month)
        imports.loc[mask, "volume_kbd"] = 0.0
    for importer, month in [("France", "2018-08"), ("Netherlands", "2019-04"), ("UK", "2022-08")]:
        mask = (imports["importer"] == importer) & (imports["month"] == month)
        imports.loc[mask, "volume_kbd"] = 0.0                # non-reported: written as 0 by the aggregator
    late = (imports["importer"] == "Germany") & (imports["month"] == "2023-06")
    return imports[~late].reset_index(drop=True)


def p2_fundamentals():
    months, dev, util, out_kbd, crack_m = p2_build()
    avg = 430.0 + 25.0 * np.cos(2 * np.pi * (months.month - 2) / 12)
    stocks = avg * (1 + dev / 100)
    return pd.DataFrame({"month": months.strftime("%Y-%m"),
                         "refinery_utilisation_pct": np.round(util, 1),
                         "distillate_stocks_mb": np.round(stocks, 1),
                         "stocks_5y_avg_mb": np.round(avg, 1)})


# ---------------------------------------------------------------------------
# Project 3 — crude: weekly stocks, release calendar, WTI, demand vintages
# ---------------------------------------------------------------------------
US_TRADING_HOLIDAYS = ["2019-01-01","2019-01-21","2019-02-18","2019-04-19","2019-05-27","2019-07-04","2019-09-02","2019-11-28","2019-12-25",
    "2020-01-01","2020-01-20","2020-02-17","2020-04-10","2020-05-25","2020-07-03","2020-09-07","2020-11-26","2020-12-25",
    "2021-01-01","2021-01-18","2021-02-15","2021-04-02","2021-05-31","2021-07-05","2021-09-06","2021-11-25","2021-12-24",
    "2022-01-17","2022-02-21","2022-04-15","2022-05-30","2022-06-20","2022-07-04","2022-09-05","2022-11-24","2022-12-26",
    "2023-01-02","2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-04","2023-09-04","2023-11-23","2023-12-25",
    "2024-01-01","2024-01-15","2024-02-19","2024-03-29","2024-05-27","2024-06-19","2024-07-04","2024-09-02","2024-11-28","2024-12-25"]
MONDAY_HOLIDAYS = [d for d in US_TRADING_HOLIDAYS if pd.Timestamp(d).dayofweek == 0]




def p3_world(seed=68, drift_size=0.0008):
    rng = np.random.default_rng(seed)
    weeks = pd.date_range("2018-12-28", "2024-12-27", freq="W-FRI")
    seasonal = np.where(weeks.month.isin([1, 2, 3, 4]), 2.0, np.where(weeks.month.isin([6, 7, 8, 9]), -2.5, 0.0))
    covid_builds = np.where((weeks >= "2020-04-01") & (weeks <= "2020-05-31"), 7.0, 0.0)   # storage glut, expected
    consensus = np.round(seasonal + covid_builds + rng.normal(0, 0.8, len(weeks)), 1)
    surprise = rng.normal(0.0, 3.0, len(weeks))
    change = consensus + surprise
    stocks = 440.0 + np.cumsum(change)
    release = []
    for week_ending in weeks:
        delay = 5
        if (week_ending + pd.Timedelta(days=3)).strftime("%Y-%m-%d") in MONDAY_HOLIDAYS:
            delay = 6                                          # Monday holiday: Thursday release
        if week_ending.strftime("%Y-%m-%d") in ["2019-11-22", "2023-11-17"]:
            delay = 5                                          # Thanksgiving week stays on Wednesday
        if week_ending.strftime("%Y-%m-%d") == "2022-06-17":
            delay = 12                                         # systems outage: published 12 days later
        day = week_ending + pd.Timedelta(days=delay)
        while day.strftime("%Y-%m-%d") in US_TRADING_HOLIDAYS:
            day = day + pd.Timedelta(days=1)                   # holiday: published the next day
        release.append(day)
    release = pd.DatetimeIndex(release)

    days = pd.bdate_range("2019-01-02", "2024-12-31")
    days = days[~days.isin(pd.to_datetime(US_TRADING_HOLIDAYS))]
    n = len(days)
    vol = np.full(n, 0.019)
    vol[(days >= "2020-03-01") & (days <= "2020-06-30")] = 0.050
    vol[(days >= "2022-03-01") & (days <= "2022-07-29")] = 0.031
    anchor_knots = pd.Series({"2019-01-02": 46, "2019-04-23": 66, "2019-08-07": 51, "2019-12-31": 61, "2020-02-28": 45,
                              "2020-04-21": 16, "2020-06-30": 39, "2020-12-31": 48, "2021-07-06": 75, "2021-10-26": 84,
                              "2021-12-01": 66, "2022-03-08": 118, "2022-06-08": 120, "2022-09-26": 77, "2022-11-07": 92,
                              "2022-12-09": 71, "2023-04-12": 83, "2023-06-12": 67, "2023-09-27": 93, "2023-12-13": 69,
                              "2024-04-05": 87, "2024-06-04": 73, "2024-07-05": 83, "2024-09-10": 66, "2024-12-31": 72})
    log_anchor = np.interp(days.asi8, pd.to_datetime(anchor_knots.index).asi8, np.log(anchor_knots.values.astype(float)))
    noise = rng.normal(0, 1, n) * vol
    reaction = np.zeros(n)
    pre_share = np.zeros(n)
    latest_surprise = np.zeros(n)
    for i, day in enumerate(release):
        if day not in days:
            continue
        k = days.get_loc(day)
        reaction[k] += -0.004 * surprise[i]                  # 10:30 -> settle reaction to the surprise
        pre_share[k] = 1.0
        latest_surprise[k + 1:] = surprise[i]                # known from the next session on
    # recovery regime only: the market kept drifting for days after a surprise
    regime = (days >= "2020-05-01") & (days <= "2021-12-31")
    drift = np.where(regime, -drift_size * latest_surprise, 0.0)
    # price = anchor path + mean-reverting noise + PERMANENT effect of the information released
    log_p = np.zeros(n)
    pre = np.full(n, np.nan)
    deviation = 0.0
    information = 0.0
    for t in range(n):
        if pre_share[t]:
            deviation = 0.97 * deviation + 0.6 * noise[t]
            pre[t] = log_anchor[t] + deviation + information
            deviation = deviation + 0.8 * noise[t]
        else:
            deviation = 0.97 * deviation + noise[t]
        information = information + reaction[t] + drift[t]
        log_p[t] = log_anchor[t] + deviation + information
    wti = np.exp(log_p)
    snapshots = pd.DataFrame({"release_date": days[pre_share > 0].strftime("%Y-%m-%d"), "snapshot_time_et": "10:29",
                              "wti_usd_bbl": np.round(np.exp(pre[pre_share > 0]), 2)})
    daily = pd.DataFrame({"date": days.strftime("%Y-%m-%d"), "wti_settle_usd_bbl": np.round(wti, 2)})
    backfill = pd.Timestamp("2020-03-02 09:00")
    ingested = []
    for day in release:
        if day < backfill:
            ingested.append(backfill)
        else:
            ingested.append((day + pd.Timedelta(hours=10, minutes=30)).tz_localize("America/New_York").tz_convert("UTC").tz_localize(None) + pd.Timedelta(minutes=7))
    weekly = pd.DataFrame({"week_ending": weeks.strftime("%Y-%m-%d"), "release_date": release.strftime("%Y-%m-%d"),
                           "release_time_et": "10:30", "crude_stocks_mbbl": np.round(stocks, 1),
                           "consensus_change_mbbl": consensus,
                           "ingested_at_utc": pd.DatetimeIndex(ingested).strftime("%Y-%m-%dT%H:%M:%SZ")})
    return weekly, daily, snapshots, surprise


def p3_demand_vintages(seed=32):
    rng = np.random.default_rng(seed)
    months = pd.date_range("2017-01-01", "2024-12-01", freq="MS")
    n = len(months)
    season = 250.0 * np.cos(2 * np.pi * (months.month - 7) / 12)
    covid = np.interp(months.asi8, pd.to_datetime(["2017-01-01", "2020-02-01", "2020-04-01", "2020-07-01", "2021-06-01", "2024-12-01"]).asi8,
                      [0, 0, -3200, -1600, -300, 0])
    true = 19800.0 + 8.0 * np.arange(n) + season + covid + ar1(rng, n, 0.85, 60.0)
    rows = []
    for i, month in enumerate(months):
        first = month + pd.offsets.MonthEnd(3)
        second = month + pd.offsets.MonthEnd(4)
        annual = pd.Timestamp("%d-08-31" % (month.year + 1))
        for vintage_date, value in [(first, true[i] - 150 + rng.normal(0, 120)), (second, true[i] - 50 + rng.normal(0, 50)),
                                    (annual, true[i])]:
            if vintage_date <= pd.Timestamp("2025-03-31"):
                rows.append({"obs_month": month.strftime("%Y-%m"), "vintage_date": vintage_date.strftime("%Y-%m-%d"),
                             "demand_kbd": round(value, 0)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Project 3 — the desk's pipeline: release events and the daily decision table
# (built with the reference solutions of 3.1 and 3.3: availability in UTC, demand as known at
#  the time; backward as-of joins; the 10-day target is a label and looks forward)
# ---------------------------------------------------------------------------
NEW_YORK = "America/New_York"


def build_release_events(stocks, daily, snapshots):
    horizon = 10
    add_availability = solution("p3-1-five-dates", "add_availability")
    events = add_availability(stocks)
    daily = daily.copy()
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.reset_index(drop=True)
    snapshots = snapshots.copy()
    snapshots["release_date"] = pd.to_datetime(snapshots["release_date"])
    events["release_date"] = pd.to_datetime(events["release_date"])
    events = events.merge(snapshots[["release_date", "wti_usd_bbl"]].rename(columns={"wti_usd_bbl": "wti_pre_release"}),
                          on="release_date", how="inner")
    position = pd.Series(daily.index, index=daily["date"])
    events["day_pos"] = events["release_date"].map(position)
    events["wti_settle"] = daily.loc[events["day_pos"], "wti_settle_usd_bbl"].values
    end_pos = events["day_pos"] + horizon
    inside = end_pos < len(daily)
    events["target_end_date"] = pd.NaT
    events.loc[inside, "target_end_date"] = daily.loc[end_pos[inside], "date"].values
    events["wti_target_end"] = np.nan
    events.loc[inside, "wti_target_end"] = daily.loc[end_pos[inside], "wti_settle_usd_bbl"].values
    events["ret_reaction"] = np.log(events["wti_settle"] / events["wti_pre_release"])
    events["ret_drift_10d"] = np.log(events["wti_target_end"] / events["wti_settle"])
    columns = ["week_ending", "release_date", "available_at", "crude_stocks_mbbl", "stocks_change_mbbl",
               "consensus_change_mbbl", "surprise_mbbl", "wti_pre_release", "wti_settle", "ret_reaction",
               "target_end_date", "ret_drift_10d"]
    events = events[columns].copy()
    events["week_ending"] = events["week_ending"].dt.strftime("%Y-%m-%d")
    events["release_date"] = events["release_date"].dt.strftime("%Y-%m-%d")
    events["available_at"] = events["available_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    events["target_end_date"] = events["target_end_date"].dt.strftime("%Y-%m-%d")
    return events.round(6)


def build_decision_table(stocks, daily, vintages, horizon=10):
    """One row per trading day: what was known at the 14:30 ET settlement, and the next 10-day return."""
    add_availability = solution("p3-1-five-dates", "add_availability")
    known_at = solution("p3-3-vintages", "known_at")
    reports = add_availability(stocks)
    days = daily.copy()
    days["date"] = pd.to_datetime(days["date"])
    settle_local = days["date"] + pd.Timedelta(hours=14, minutes=30)
    days["decision_time"] = settle_local.dt.tz_localize(NEW_YORK).dt.tz_convert("UTC")
    days = days.sort_values("decision_time")
    known = reports[["available_at", "week_ending", "surprise_mbbl"]].sort_values("available_at")
    table = pd.merge_asof(days, known, left_on="decision_time", right_on="available_at",
                          direction="backward", tolerance=pd.Timedelta(days=10))
    # the demand information only changes the day after a vintage is published
    change_days = pd.Series(sorted(pd.to_datetime(vintages["vintage_date"]).unique())) + pd.Timedelta(days=1)
    change_days = change_days[change_days > days["date"].min() - pd.Timedelta(days=100)]
    growth = known_at(vintages, change_days)[["decision_date", "growth_known_pct"]]
    table = pd.merge_asof(table.sort_values("date"), growth, left_on="date", right_on="decision_date",
                          direction="backward")
    table = table.rename(columns={"growth_known_pct": "demand_growth_known_pct"}).drop(columns="decision_date")
    table["target_end_date"] = table["date"].shift(-horizon)
    table["ret_fwd_10d"] = np.log(table["wti_settle_usd_bbl"].shift(-horizon) / table["wti_settle_usd_bbl"])
    table = table.rename(columns={"week_ending": "latest_report_week"})
    columns = ["date", "wti_settle_usd_bbl", "latest_report_week", "surprise_mbbl", "demand_growth_known_pct",
               "target_end_date", "ret_fwd_10d"]
    table = table[columns].copy()
    table["date"] = table["date"].dt.strftime("%Y-%m-%d")
    table["latest_report_week"] = table["latest_report_week"].dt.strftime("%Y-%m-%d")
    table["target_end_date"] = table["target_end_date"].dt.strftime("%Y-%m-%d")
    return table.round(6)


# ---------------------------------------------------------------------------
# Project 4 — crude research panel 2012-2019 and monthly diesel demand
# ---------------------------------------------------------------------------
def p4_crude_research(seed_brent=22, seed_wti=1061, seed_coffee=40, seed_dubai=4061):
    """Brent: log random walk whose volatility changes by regime, with a slump drift mid-2014 -> early 2016.
    WTI: error correction around log WTI = a + log Brent; regime change on 2016-01-01 (end of the export ban).
    Dubai: Brent plus a small stationary differential. Coffee: independent of crude."""
    dates = pd.bdate_range("2012-01-02", "2019-12-31")
    n = len(dates)
    brk = dates.searchsorted(pd.Timestamp("2016-01-01"))
    shock_day = dates.searchsorted(pd.Timestamp("2017-08-28"))
    vol = np.full(n, 0.012)
    vol[(dates >= "2014-07-01") & (dates <= "2016-03-31")] = 0.026
    vol[(dates >= "2016-04-01") & (dates <= "2018-09-30")] = 0.016
    vol[(dates >= "2018-10-01") & (dates <= "2018-12-31")] = 0.025
    vol[dates >= "2019-01-01"] = 0.017
    drift = np.zeros(n)
    drift[(dates >= "2014-07-01") & (dates <= "2016-01-20")] = -0.0029
    drift[(dates > "2016-01-20") & (dates <= "2018-09-30")] = 0.0009
    rb = np.random.default_rng(seed_brent)
    shocks = rb.normal(0.0, 1.0, n) * vol + drift
    shocks[0] = 0.0
    b = np.log(111.0) + np.cumsum(shocks)
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
    rd = np.random.default_rng(seed_dubai)
    dn = np.zeros(n)
    e = rd.normal(0, 0.006, n)
    for t in range(n):
        dn[t] = (0.9 * dn[t - 1] if t else 0) + e[t]
    d = b - 0.025 + dn
    return pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "brent": np.round(np.exp(b), 2), "wti": np.round(np.exp(w), 2),
                         "dubai": np.round(np.exp(d), 2), "coffee": np.round(np.exp(c), 2)})


def p4_diesel_demand_monthly(seed=1):
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
    return pd.DataFrame({"month": months.strftime("%Y-%m"), "demand_kbd": np.round(demand, 1)})


# ---------------------------------------------------------------------------
# derived layers: produced by the reference solutions of the exercises
# ---------------------------------------------------------------------------
def solution(problem, function):
    """Load `function` from problems/quant/<problem>/solution.py."""
    path = os.path.join(PROBLEMS, problem, "solution.py")
    namespace = {"__name__": "reference"}
    with open(path, encoding="utf-8") as f:
        exec(compile(f.read(), path, "exec"), namespace)
    return namespace[function]


def path(name):
    return os.path.join(HERE, name)


def save(frame, name, index=False):
    frame.to_csv(path(name), index=index)


def main():
    old_cwd = os.getcwd()
    os.chdir(HERE)
    try:
        build_all()
    finally:
        os.chdir(old_cwd)
    print("written to", HERE)


def build_all():
    # ---- Project 1: power
    p1 = p1_files()
    save(p1["vendor"], "p1_power_hourly_vendor_synthetic.csv")
    save(p1["zone_load"], "p1_zone_load_hourly_synthetic.csv")
    save(p1["temps"], "p1_zone_temperature_obs_synthetic.csv")
    save(p1["zones"], "p1_zones_reference_synthetic.csv")
    save(p1["normals"], "p1_weather_normals_synthetic.csv")
    clean = solution("p1-1-delivery-hours", "load_market_hours")("p1_power_hourly_vendor_synthetic.csv")
    save(clean, "p1_power_hourly_clean_synthetic.csv", index=True)
    clean = pd.read_csv(path("p1_power_hourly_clean_synthetic.csv"))
    clean["delivery_start_utc"] = pd.to_datetime(clean["delivery_start_utc"], utc=True)
    clean["local_date"] = pd.to_datetime(clean["local_date"])
    treated = solution("p1-2-gaps-and-stale-data", "treat_gaps")(clean.set_index("delivery_start_utc"))
    save(treated, "p1_power_hourly_treated_synthetic.csv", index=True)
    temps = pd.read_csv(path("p1_zone_temperature_obs_synthetic.csv"))
    zone_load = pd.read_csv(path("p1_zone_load_hourly_synthetic.csv"))
    zones = pd.read_csv(path("p1_zones_reference_synthetic.csv"))
    daily = solution("p1-3-degree-days", "daily_zone_table")(temps, zone_load, zones)
    save(daily, "p1_zone_daily_synthetic.csv")

    # ---- Project 2: oil products
    raw, events, outages, _ = p2_files()
    save(raw, "p2_products_daily_long_synthetic.csv")
    save(events, "p2_market_events_synthetic.csv")
    save(outages, "p2_refinery_outages_synthetic.csv")
    save(p2_imports(), "p2_diesel_imports_monthly_synthetic.csv")
    save(p2_fundamentals(), "p2_distillate_fundamentals_monthly_synthetic.csv")
    raw = pd.read_csv(path("p2_products_daily_long_synthetic.csv"))
    wide = solution("p2-1-cracks", "build_daily_table")(raw)
    save(wide, "p2_products_wide_synthetic.csv", index=True)
    wide = pd.read_csv(path("p2_products_wide_synthetic.csv"), index_col="date", parse_dates=["date"])
    events = pd.read_csv(path("p2_market_events_synthetic.csv"))
    investigated = solution("p2-2-extremes", "investigate_extremes")(wide, events)
    repaired = investigated["prices"]
    for product in ["gasoil", "ulsd", "rbob", "jet"]:
        repaired[product + "_crack"] = repaired[product] - repaired["brent"]
    save(repaired, "p2_products_repaired_synthetic.csv", index=True)
    repaired = pd.read_csv(path("p2_products_repaired_synthetic.csv"), index_col="date", parse_dates=["date"])
    imports = pd.read_csv(path("p2_diesel_imports_monthly_synthetic.csv"))
    outages = pd.read_csv(path("p2_refinery_outages_synthetic.csv"))
    fundamentals = pd.read_csv(path("p2_distillate_fundamentals_monthly_synthetic.csv"))
    monthly = solution("p2-3-imports-and-outages", "monthly_table")(imports, outages, fundamentals, repaired)
    save(monthly, "p2_monthly_table_synthetic.csv", index=True)

    # ---- Project 3: crude, point-in-time
    weekly, daily_wti, snapshots, _ = p3_world()
    save(weekly, "p3_us_crude_stocks_weekly_synthetic.csv")
    save(daily_wti, "p3_wti_daily_synthetic.csv")
    save(snapshots, "p3_wti_release_snapshots_synthetic.csv")
    save(p3_demand_vintages(), "p3_us_oil_demand_vintages_synthetic.csv")
    weekly = pd.read_csv(path("p3_us_crude_stocks_weekly_synthetic.csv"))
    daily_wti = pd.read_csv(path("p3_wti_daily_synthetic.csv"))
    snapshots = pd.read_csv(path("p3_wti_release_snapshots_synthetic.csv"))
    vintages = pd.read_csv(path("p3_us_oil_demand_vintages_synthetic.csv"))
    events = build_release_events(weekly, daily_wti, snapshots)
    save(events, "p3_release_events_synthetic.csv")
    decisions = build_decision_table(weekly, daily_wti, vintages)
    save(decisions, "p3_decision_table_daily_synthetic.csv")

    # ---- Project 4: crude research panel
    save(p4_crude_research(), "p4_crude_research_daily_synthetic.csv")
    save(p4_diesel_demand_monthly(), "p4_diesel_demand_monthly_synthetic.csv")


if __name__ == "__main__":
    main()
