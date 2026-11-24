import pandas as pd

SPIKE_EUR_MWH = 300.0


def explain_spikes(hours, daily):
    hours = hours.copy()
    # what thermal plants must cover, and how much spare capacity is left
    hours["residual_load_mw"] = hours["load_mw"] - hours["wind_mw"] - hours["solar_mw"]
    hours["margin_mw"] = hours["available_capacity_mw"] - hours["residual_load_mw"]

    days = hours.groupby("local_date").agg(max_price=("price_eur_mwh", "max"),
                                           mean_price=("price_eur_mwh", "mean"),
                                           min_margin_mw=("margin_mw", "min"),
                                           wind_mean_mw=("wind_mw", "mean"),
                                           capacity_mw=("available_capacity_mw", "mean"),
                                           gas_eur_mwh=("gas_eur_mwh", "mean"))

    # national heating degree days: simple average of the three zones
    daily = daily.copy()
    daily["local_date"] = pd.to_datetime(daily["local_date"])
    days["hdd"] = daily.groupby("local_date")["hdd"].mean()

    # is today's capacity normal? compare with the median of the same calendar month
    month = days.index.month
    days["capacity_ratio"] = days["capacity_mw"] / days.groupby(month)["capacity_mw"].transform("median")

    # rank correlations over all days: spikes make Pearson unreliable
    drivers = ["hdd", "wind_mean_mw", "min_margin_mw", "capacity_ratio"]
    correlations = days[["max_price"] + drivers].corr(method="spearman")["max_price"].drop("max_price")

    # spike days and a first, transparent attribution
    spikes = days[days["max_price"] >= SPIKE_EUR_MWH].copy()
    cold_and_still = (spikes["hdd"] >= 12) & (spikes["wind_mean_mw"] < 4000)
    low_capacity = spikes["capacity_ratio"] < 0.9
    spikes["driver"] = "unexplained"
    spikes.loc[low_capacity, "driver"] = "low available capacity"
    spikes.loc[cold_and_still, "driver"] = "cold and still"
    return {"spike_days": spikes, "rank_correlations": correlations}
