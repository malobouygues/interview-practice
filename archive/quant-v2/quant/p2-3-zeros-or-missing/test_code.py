import pandas as pd

imports = pd.read_csv("data/p2_diesel_imports_monthly_synthetic.csv")
print(imports.head(8))

table = total_imports(imports)
print(table.loc["2018-06":"2018-10"].round(1))
print(table.tail(3).round(1))

naive = imports.groupby("month")["volume_kbd"].sum()             # what a careless sum gives
print("naive totals:", naive.loc[["2018-07", "2018-08", "2018-09", "2019-12"]].round(1).to_dict())
print("genuine zeros (one origin, country reporting):")
print(imports[(imports["volume_kbd"] == 0)].groupby(["month", "importer"]).size().head(12))
