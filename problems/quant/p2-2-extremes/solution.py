import numpy as np
import pandas as pd

SISTER_MARKETS = {"brent": ["gasoil", "ulsd"], "gasoil": ["ulsd", "jet"], "ulsd": ["gasoil", "jet"],
                  "rbob": ["ulsd", "brent"], "jet": ["gasoil", "ulsd"]}
UNIT_FACTORS = [100.0, 42.0, 10.0, 0.1, 1 / 42, 0.01]     # cents vs dollars, gallons vs barrels, a decimal point


def investigate_extremes(prices, events):
    prices = prices[["brent", "gasoil", "ulsd", "rbob", "jet"]].copy()
    events = events.copy()
    events["start"] = pd.to_datetime(events["start"])
    events["end"] = pd.to_datetime(events["end"])
    decisions = []

    # ---- PASS 1: levels. Impossible values, then unit errors seen against the neighbours
    for series in prices.columns:
        impossible = prices[series] <= 0
        for date in prices.index[impossible]:
            decisions.append({"date": date, "series": series, "value": prices.loc[date, series],
                              "check": "price <= 0", "decision": "set_missing"})
        prices.loc[impossible, series] = np.nan

        observed = prices[series].dropna()
        neighbours = (observed.shift(1) + observed.shift(-1)) / 2
        ratio = observed / neighbours
        for factor in UNIT_FACTORS:
            unit_error = (ratio / factor - 1).abs() < 0.03
            for date in observed.index[unit_error]:
                decisions.append({"date": date, "series": series, "value": observed[date],
                                  "check": "x%g the neighbours" % factor, "decision": "correct_unit"})
                prices.loc[date, series] = observed[date] / factor

    # ---- PASS 2: daily log returns of the repaired prices, three scores
    returns = {}
    flag_counts = []
    for series in prices.columns:
        observed = prices[series].dropna()
        r = np.log(observed).diff().dropna()
        z = (r - r.mean()) / r.std()
        mad = (r - r.median()).abs().median()
        modified_z = 0.6745 * (r - r.median()) / mad
        q1 = r.quantile(0.25)
        q3 = r.quantile(0.75)
        iqr = q3 - q1
        iqr_flag = (r < q1 - 3 * iqr) | (r > q3 + 3 * iqr)
        returns[series] = pd.DataFrame({"ret": r, "z": z, "modified_z": modified_z, "iqr_flag": iqr_flag})
        flag_counts.append({"series": series, "z_above_4": int((z.abs() > 4).sum()),
                            "modified_z_above_6": int((modified_z.abs() > 6).sum()),
                            "iqr_3": int(iqr_flag.sum())})

    # ---- PASS 3: investigate each robust candidate (|modified z| > 6)
    for series in prices.columns:
        table = returns[series]
        candidates = table[table["modified_z"].abs() > 6]
        for date, row in candidates.iterrows():
            covering = events[(events["start"] <= date) & (events["end"] >= date)]
            covering = covering[covering["markets"].str.contains(series)]
            confirmed = False
            for sister in SISTER_MARKETS[series]:
                if date in returns[sister].index:
                    sister_ret = returns[sister].loc[date, "ret"]
                    if sister_ret * row["ret"] > 0 and abs(sister_ret) >= 0.5 * abs(row["ret"]):
                        confirmed = True
            if len(covering) > 0:
                decision = "keep_event"
                check = covering["event"].iloc[0]
            elif confirmed:
                decision = "keep_market_move"
                check = "sister markets moved the same way"
            else:
                decision = "keep_doubtful"
                check = "no event, not confirmed by sister markets"
            decisions.append({"date": date, "series": series, "value": prices.loc[date, series],
                              "ret": row["ret"], "z": row["z"], "modified_z": row["modified_z"],
                              "iqr_flag": row["iqr_flag"], "check": check, "decision": decision})

    decisions = pd.DataFrame(decisions).sort_values(["date", "series"]).reset_index(drop=True)
    flag_counts = pd.DataFrame(flag_counts).set_index("series")
    return {"decisions": decisions, "flag_counts": flag_counts, "prices": prices}
