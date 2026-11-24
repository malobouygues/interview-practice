import pandas as pd
from statsmodels.tsa.stattools import acf


def price_patterns(hours):
    # 1. the daily shape: the price distribution at each local hour (a boxplot, in numbers)
    by_hour = hours.groupby("local_hour")["price_eur_mwh"]
    profile = pd.DataFrame({"q10": by_hour.quantile(0.10), "q25": by_hour.quantile(0.25),
                            "median": by_hour.median(),
                            "q75": by_hour.quantile(0.75), "q90": by_hour.quantile(0.90)})

    # 2. hour-to-hour price changes: power prices can be negative, so differences, not log returns
    change = hours["price_eur_mwh"].diff().dropna()
    change_stats = {"std": change.std(),
                    "skew": change.skew(),
                    "excess_kurtosis": change.kurt(),
                    "share_beyond_3_std_pct": 100 * (change.abs() > 3 * change.std()).mean()}

    # 3. memory of the load: autocorrelation after 1 hour, 12 hours, one day, one week
    load_acf = acf(hours["load_mw"], nlags=168)
    acf_load = {1: load_acf[1], 12: load_acf[12], 24: load_acf[24], 168: load_acf[168]}

    # 4. a correlation made by the clock: load and solar both follow the time of day.
    #    Compare the raw correlation with the one WITHIN the same local hour.
    load_gap = hours["load_mw"] - hours.groupby("local_hour")["load_mw"].transform("mean")
    solar_gap = hours["solar_mw"] - hours.groupby("local_hour")["solar_mw"].transform("mean")
    load_solar = {"raw": hours["load_mw"].corr(hours["solar_mw"]),
                  "within_hour": load_gap.corr(solar_gap)}

    # 5. rolling volatility of the daily average price (30 days)
    daily_price = hours.groupby("local_date")["price_eur_mwh"].mean()
    rolling_std = daily_price.diff().rolling(30).std()

    return {"hourly_profile": profile, "change_stats": change_stats, "acf_load": acf_load,
            "load_solar_correlation": load_solar, "rolling_std_30d": rolling_std}
