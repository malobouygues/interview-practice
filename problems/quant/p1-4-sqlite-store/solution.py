import sqlite3

import pandas as pd


def monthly_spreads_sql(prices: pd.DataFrame) -> pd.DataFrame:
    connection = sqlite3.connect(":memory:")

    # one row per date: the primary key makes a duplicate date impossible
    connection.execute("""
        CREATE TABLE crude_prices (
            date  TEXT PRIMARY KEY,
            brent REAL,
            wti   REAL,
            dubai REAL
        )
    """)

    rows = []
    for date, row in prices.iterrows():
        rows.append((date.strftime("%Y-%m-%d"), row["brent"], row["wti"], row["dubai"]))

    # INSERT OR REPLACE: loading the same data twice leaves the table unchanged (idempotent)
    insert = "INSERT OR REPLACE INTO crude_prices VALUES (?, ?, ?, ?)"
    connection.executemany(insert, rows)
    connection.executemany(insert, rows)

    query = """
        SELECT substr(date, 1, 7)  AS month,
               AVG(brent - wti)    AS brent_wti,
               AVG(brent - dubai)  AS brent_dubai,
               COUNT(*)            AS n_days
        FROM crude_prices
        WHERE brent IS NOT NULL AND wti IS NOT NULL AND dubai IS NOT NULL
        GROUP BY month
        ORDER BY month
    """
    result = pd.read_sql_query(query, connection)
    connection.close()
    return result
