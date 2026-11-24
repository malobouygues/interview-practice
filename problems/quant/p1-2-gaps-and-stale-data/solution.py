import pandas as pd

def treat_gaps(hours):
    hours = hours.copy()
    month = hours["local_date"].dt.month

    # SOLAR: the vendor leaves zero output blank. A blank at an hour that normally produces
    # (median of that month and hour above 500 MW) is a feed failure; elsewhere it means 0.
    # Group by the UTC hour: the sun follows solar time, not the clocks' DST change.
    utc_hour = hours.index.hour
    solar_as_zero = hours["solar_mw"].fillna(0)
    typical_solar = solar_as_zero.groupby([month, utc_hour]).transform("median")
    daylight = typical_solar > 500
    blank = hours["solar_mw"].isna()
    hours["solar_missing"] = blank & daylight
    hours.loc[blank & ~daylight, "solar_mw"] = 0.0

    # WIND: wind blows day and night, a blank is always a failure -> stays NaN, flagged
    hours["wind_missing"] = hours["wind_mw"].isna()

    # CAPACITY: a daily state sent with the first hour of the day -> carry it, 48 hours at most
    reported = hours["available_capacity_mw"].notna()
    report_time = pd.Series(hours.index, index=hours.index)
    report_time = report_time.where(reported)
    report_time = report_time.ffill()
    hours["capacity_age_h"] = (hours.index - report_time) / pd.Timedelta(hours=1)
    hours["available_capacity_mw"] = hours["available_capacity_mw"].ffill(limit=48)

    # stale = sent on an earlier LOCAL day. "24 hours old" would be wrong on the 25-hour day:
    # its last hour is 24 hours after a report that is still today's
    report_date = hours["local_date"].where(reported)
    report_date = report_date.ffill()
    hours["capacity_is_stale"] = report_date < hours["local_date"]

    # PRICE: an auction result cannot be guessed -> never filled
    return hours
