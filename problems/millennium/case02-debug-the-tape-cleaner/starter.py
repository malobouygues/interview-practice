import pandas as pd
import numpy as np

def clean_tape(prices):
    df = prices.copy()
    asset_cols = [c for c in df.columns if c != 'timestamp']

    # Carry the last good print forward over any gaps in the tape
    df[asset_cols] = df[asset_cols].ffill()

    # Put the tape into chronological order
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Collapse repeated timestamps down to a single row
    df = df.drop_duplicates(subset='timestamp', keep='last').reset_index(drop=True)

    return df
