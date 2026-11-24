import pandas as pd

MARKET_TZ = "Europe/Paris"   # the market's clock (CET in winter, CEST in summer)

def load_market_hours(path):
    raw = pd.read_csv(path)

    # 1. one unambiguous clock: local wall time + its UTC offset -> UTC
    local_with_offset = raw["delivery_start_local"] + raw["utc_offset"]
    raw["delivery_start_utc"] = pd.to_datetime(local_with_offset, format="%Y-%m-%d %H:%M%z", utc=True)
    raw["loaded_at"] = pd.to_datetime(raw["loaded_at_utc"], utc=True)

    # 2. exact copies of the same record: drop them
    raw = raw.drop_duplicates()

    # 3. two different versions of the same delivery hour: keep the latest one loaded
    raw = raw.sort_values(["delivery_start_utc", "loaded_at"])
    hours = raw.drop_duplicates(subset="delivery_start_utc", keep="last")

    # 4. label every hour with the market's local delivery day and hour
    local_time = hours["delivery_start_utc"].dt.tz_convert(MARKET_TZ)
    hours["local_date"] = local_time.dt.tz_localize(None).dt.normalize()
    hours["local_hour"] = local_time.dt.hour

    hours = hours.set_index("delivery_start_utc")
    columns = ["local_date", "local_hour", "price_eur_mwh", "load_mw", "wind_mw", "solar_mw",
               "available_capacity_mw", "gas_eur_mwh"]
    return hours[columns]
