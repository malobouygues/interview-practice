def clean_tape(prices):
    df = prices.copy()
    asset_cols = [c for c in df.columns if c != 'timestamp']

    # 1. ordre chronologique (tri stable : conserve l'ordre d'arrivée à timestamp égal)
    df = df.sort_values('timestamp', kind='mergesort').reset_index(drop=True)

    # 2. une ligne par timestamp, la première APRÈS le tri
    df = df.drop_duplicates(subset='timestamp', keep='first').reset_index(drop=True)

    # 3. un prix nul ou négatif est un prix manquant
    df[asset_cols] = df[asset_cols].mask(df[asset_cols] <= 0)

    # 4. forward-fill par colonne, depuis le dernier prix valide post-tri
    df[asset_cols] = df[asset_cols].ffill()

    return df
