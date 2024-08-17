import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from scheduled_tasks.economy.ychart_connection import ychart_data
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def jobless_claims():
    """
    Get initial jobless claims
    """
    print("Getting Initial Jobless Claims...")

    url = "https://ycharts.com/indicators/us_initial_claims_for_unemployment_insurance"
    df = ychart_data(url)
    df = pd.concat([df[6][::-1], df[5][::-1]], axis=0)

    df["Value"] = df["Value"].astype(int)
    df["Percent Change"] = df["Value"].shift(1)
    df["Percent Change"] = df["Percent Change"].astype(float)
    df["Percent Change"] = (
        100 * (df["Value"] - df["Percent Change"]) / df["Percent Change"]
    )
    df["Percent Change"] = df["Percent Change"].round(2)

    df["Date"] = df["Date"].astype("datetime64[ns]").astype(str)
    df.fillna(0, inplace=True)

    for index, row in df.iterrows():
        cur.execute(
            "INSERT IGNORE INTO initial_jobless_claims VALUES (%s, %s, %s)",
            (row[0], row[1], row[2]),
        )
        cnx.commit()

    print("Initial Jobless Claims Successfully Completed...\n")


if __name__ == "__main__":
    jobless_claims()
