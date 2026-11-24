import numpy as np
import pandas as pd


def monthly_table(imports, outages, fundamentals, daily):
    # ---- imports: long, one row per month x importer x origin
    imports = imports.copy()
    imports["month"] = pd.PeriodIndex(imports["month"], freq="M")
    imports["is_positive"] = imports["volume_kbd"] > 0
    by_importer = imports.groupby(["month", "importer"], as_index=False).agg(
        volume_kbd=("volume_kbd", "sum"), positive_origins=("is_positive", "sum"))
    # every origin at 0 for one importer = the country did not report: missing, not zero
    not_reported = by_importer["positive_origins"] == 0
    by_importer.loc[not_reported, "volume_kbd"] = np.nan
    importers = by_importer.pivot(index="month", columns="importer", values="volume_kbd")
    table = pd.DataFrame(index=importers.index)
    table["importers_reporting"] = importers.notna().sum(axis=1)
    table["imports_kbd"] = importers.sum(axis=1, min_count=4)        # Europe total: all four countries needed

    reported = by_importer.loc[~not_reported, ["month", "importer"]]
    reported_rows = imports.merge(reported, on=["month", "importer"])
    from_russia = reported_rows[reported_rows["origin"] == "Russia"]
    table["imports_from_russia_kbd"] = from_russia.groupby("month")["volume_kbd"].sum()
    table.loc[table["imports_kbd"].isna(), "imports_from_russia_kbd"] = np.nan

    # ---- outages: one row per outage -> one row per day offline -> monthly average kb/d
    pieces = []
    for outage in outages.itertuples():
        days = pd.date_range(outage.start, outage.end, freq="D")
        pieces.append(pd.DataFrame({"day": days, "offline_kbd": outage.offline_kbd}))
    outage_days = pd.concat(pieces)
    outage_days["month"] = outage_days["day"].dt.to_period("M")
    offline = outage_days.groupby("month")["offline_kbd"].sum()
    offline = offline / offline.index.days_in_month
    # the outage list is complete: a month with no outage really had 0 kb/d offline
    table["outages_kbd"] = offline.reindex(table.index).fillna(0.0)

    # ---- fundamentals (wide already): stocks against their 5-year average
    fundamentals = fundamentals.copy()
    fundamentals["month"] = pd.PeriodIndex(fundamentals["month"], freq="M")
    fundamentals = fundamentals.set_index("month")
    table["refinery_utilisation_pct"] = fundamentals["refinery_utilisation_pct"]
    table["stocks_vs_5y_pct"] = 100 * (fundamentals["distillate_stocks_mb"] / fundamentals["stocks_5y_avg_mb"] - 1)

    # ---- daily gasoil crack -> monthly average and number of priced days
    daily = daily.copy()
    daily["month"] = daily.index.to_period("M")
    monthly_crack = daily.groupby("month")["gasoil_crack"].agg(["mean", "count"])
    table["gasoil_crack"] = monthly_crack["mean"]
    table["crack_days"] = monthly_crack["count"]
    return table
