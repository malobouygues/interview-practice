import pandas as pd
import statsmodels.api as sm


def weather_adjusted_load(daily, normals):
    daily = daily.copy()
    daily["local_date"] = pd.to_datetime(daily["local_date"])
    daily["month"] = daily["local_date"].dt.month
    daily["is_weekend"] = (daily["local_date"].dt.dayofweek >= 5).astype(float)

    # the zone's normal (30-year) degree days for that calendar month = the reference weather
    daily = daily.merge(normals[["zone", "month", "normal_hdd", "normal_cdd"]], on=["zone", "month"], how="left")

    coefficients = []
    adjusted = []
    for zone in sorted(daily["zone"].unique()):
        sample = daily[daily["zone"] == zone]
        sample = sample.dropna(subset=["load_avg_mw", "hdd", "cdd"])
        sample = sample.sort_values("local_date")      # Durbin-Watson reads the errors in time order

        # average MW of the day = a + b_hdd * HDD + b_cdd * CDD + c * weekend + error
        X = sm.add_constant(sample[["hdd", "cdd", "is_weekend"]])
        model = sm.OLS(sample["load_avg_mw"], X).fit()
        interval = model.conf_int()
        coefficients.append({"zone": zone,
                             "b_hdd": model.params["hdd"],
                             "b_hdd_low": interval.loc["hdd", 0], "b_hdd_high": interval.loc["hdd", 1],
                             "b_cdd": model.params["cdd"],
                             "b_cdd_low": interval.loc["cdd", 0], "b_cdd_high": interval.loc["cdd", 1],
                             "b_weekend": model.params["is_weekend"],
                             "r2": model.rsquared, "n_days": int(model.nobs),
                             "durbin_watson": sm.stats.durbin_watson(model.resid),
                             "cdd_days": int((sample["cdd"] > 0).sum())})

        # how much the ACTUAL weather added or removed compared with NORMAL weather
        hdd_gap = sample["hdd"] - sample["normal_hdd"]
        cdd_gap = sample["cdd"] - sample["normal_cdd"]
        part = sample[["zone", "local_date", "hdd", "normal_hdd", "cdd", "normal_cdd", "load_avg_mw"]].copy()
        part["weather_effect_mw"] = model.params["hdd"] * hdd_gap + model.params["cdd"] * cdd_gap
        part["load_adjusted_mw"] = part["load_avg_mw"] - part["weather_effect_mw"]
        adjusted.append(part)

    coefficients = pd.DataFrame(coefficients)
    adjusted = pd.concat(adjusted, ignore_index=True)

    # January-February 2023 against January-February 2024, zone by zone
    winter = adjusted[adjusted["local_date"].dt.month <= 2].copy()
    winter["year"] = winter["local_date"].dt.year
    comparison = winter.groupby(["zone", "year"])[["hdd", "load_avg_mw", "load_adjusted_mw"]].mean()
    return {"coefficients": coefficients, "daily": adjusted, "winter_comparison": comparison}
