import numpy as np
import pandas as pd

MARKET_TZ = "Europe/Paris"

def daily_zone_table(temps, load, zones):
    # ---- temperature: irregular UTC observations -> hourly means -> local-day mean
    temps = temps.copy()
    temps["observed_at"] = pd.to_datetime(temps["observed_at_utc"], utc=True)
    plausible = temps["temperature_c"].between(-40, 50)
    temps = temps[plausible]
    temps["hour_utc"] = temps["observed_at"].dt.floor("h")
    hourly_temp = temps.groupby(["zone", "hour_utc"], as_index=False)["temperature_c"].mean()
    local_time = hourly_temp["hour_utc"].dt.tz_convert(MARKET_TZ)
    hourly_temp["local_date"] = local_time.dt.tz_localize(None).dt.normalize()
    daily_temp = hourly_temp.groupby(["zone", "local_date"], as_index=False).agg(
        temp_mean_c=("temperature_c", "mean"), temp_hours=("temperature_c", "count"))
    too_few_hours = daily_temp["temp_hours"] < 18
    daily_temp.loc[too_few_hours, "temp_mean_c"] = np.nan

    # ---- degree days, each zone with its own base temperature
    daily = daily_temp.merge(zones[["zone", "hdd_base_c", "cdd_base_c"]], on="zone", how="left")
    daily["hdd"] = (daily["hdd_base_c"] - daily["temp_mean_c"]).clip(lower=0)
    daily["cdd"] = (daily["temp_mean_c"] - daily["cdd_base_c"]).clip(lower=0)

    # ---- load: hourly MW in UTC -> local day: average MW, and energy in MWh
    load = load.copy()
    load["delivery_start"] = pd.to_datetime(load["delivery_start_utc"], utc=True)
    local_time = load["delivery_start"].dt.tz_convert(MARKET_TZ)
    load["local_date"] = local_time.dt.tz_localize(None).dt.normalize()
    daily_load = load.groupby(["zone", "local_date"], as_index=False).agg(
        load_avg_mw=("load_mw", "mean"), load_hours=("load_mw", "count"))

    # hours in the local day: 23 on the spring DST Sunday, 25 in October, else 24
    day_start = daily_load["local_date"].dt.tz_localize(MARKET_TZ)
    next_day_start = (daily_load["local_date"] + pd.Timedelta(days=1)).dt.tz_localize(MARKET_TZ)
    daily_load["hours_in_day"] = (next_day_start - day_start) / pd.Timedelta(hours=1)
    too_few_hours = daily_load["load_hours"] < 0.9 * daily_load["hours_in_day"]
    daily_load.loc[too_few_hours, "load_avg_mw"] = np.nan
    daily_load["load_mwh"] = daily_load["load_avg_mw"] * daily_load["hours_in_day"]

    daily = daily.merge(daily_load, on=["zone", "local_date"], how="outer")
    daily = daily.sort_values(["zone", "local_date"]).reset_index(drop=True)
    return daily
