import os
import sys
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scheduled_tasks.economy.ychart_connection import ychart_data

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def jobless_claims():
    """
    Get initial jobless claims
    """

    url = "https://ycharts.com/indicators/us_initial_claims_for_unemployment_insurance"
    df = ychart_data(url)
    df = df[6][::-1].append(df[5][::-1])

    df["Value"] = df["Value"].astype(int)
    df["Percent Change"] = df["Value"].shift(1)
    df["Percent Change"] = df["Percent Change"].astype(float)
    df["Percent Change"] = 100 * (df["Value"] - df["Percent Change"]) / \
                                    df["Percent Change"]
    df["Percent Change"] = df["Percent Change"].round(2)

    df["Date"] = df["Date"].astype('datetime64[ns]').astype(str)
    df.fillna(0, inplace=True)
    print(df)

    for index, row in df.iterrows():
        db.execute("INSERT OR IGNORE INTO initial_jobless_claims VALUES (?, ?, ?)", (row[0], row[1], row[2]))
        conn.commit()


if __name__ == '__main__':
    jobless_claims()
