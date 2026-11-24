import pandas as pd
import matplotlib.pyplot as plt

raw = pd.read_csv("data/p2_products_daily_long_synthetic.csv")
print(raw.head(6).to_string())
print("rows:", len(raw), "| exact copies:", raw.duplicated().sum())
print(raw.groupby(["product", "unit"]).size().to_string())

daily = build_daily_table(raw)
print(daily.isna().sum().to_dict())
print(daily.groupby(daily.index.year)[["gasoil_crack", "ulsd_crack", "rbob_crack", "jet_crack"]].mean().round(1).to_string())

# three ways to handle the gaps, on the October 2018 gasoil crack (frozen feed blanked)
october = daily.loc["2018-10"]
print("leave blank:", round(october["gasoil_crack"].mean(), 2), "on", october["gasoil_crack"].notna().sum(), "days")
filled = daily["gasoil"].ffill() - daily["brent"]
print("forward-fill without limit:", round(filled.loc["2018-10"].mean(), 2))
complete = daily[["brent", "gasoil", "ulsd", "rbob", "jet"]].dropna()
print("drop incomplete dates:", len(complete), "of", len(daily), "dates kept")

fig, ax = plt.subplots(figsize=(10, 4))
daily[["gasoil_crack", "ulsd_crack"]].plot(ax=ax, linewidth=0.8)
ax.set_title("diesel cracks against Brent (USD/bbl)")
