import pandas as pd
import numpy as np

def client_markout(fills: pd.DataFrame, prices: pd.DataFrame, horizon_minutes) -> dict:
    fills = fills.copy()
    fills["timestamp"] = pd.to_datetime(fills["timestamp"])
    fills["mark_time"] = fills["timestamp"] + pd.Timedelta(minutes=horizon_minutes)

    # tape en format long : une ligne par (timestamp, asset)
    tape = prices.melt(id_vars="timestamp", var_name="asset", value_name="price_h")
    tape["timestamp"] = pd.to_datetime(tape["timestamp"])
    tape = tape.dropna(subset=["price_h"])
    tape = tape.rename(columns={"timestamp": "mark_time"})

    fills = fills.sort_values("mark_time")
    tape = tape.sort_values("mark_time")

    # P_h = dernier prix à ou avant fill + horizon (au-delà du tape : dernier prix)
    df = pd.merge_asof(
        fills,
        tape,
        on="mark_time",
        by="asset",
        direction="backward"
    )

    # markout du point de vue du MM, qui prend le côté opposé du client
    df["markout"] = np.where(
        df["side"] == "BUY",
        (df["fill_price"] - df["price_h"]) * df["quantity"],
        (df["price_h"] - df["fill_price"]) * df["quantity"],
    )

    avg = df.groupby("client_id")["markout"].mean()

    result = {}
    for client, value in avg.items():
        value = round(float(value), 6)
        result[client] = {"avg_markout": value, "toxic": value < 0}

    return result
