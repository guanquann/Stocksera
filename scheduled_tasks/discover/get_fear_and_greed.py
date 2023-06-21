import os
import sys
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database, header

cnx, cur, engine = connect_mysql_database()


def main():
    print("Getting CNN fear and greed...")

    data = requests.get("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", headers=header).json()

    df = pd.DataFrame(data["fear_and_greed_historical"]["data"])
    df["x"] = df["x"].apply(lambda x: str(datetime.fromtimestamp(int(str(x)[:-5]))).split()[0])
    df["rating"] = df["rating"].str.title()

    historical_df = yf.Ticker("SPY").history(period="5y", interval="1d")
    historical_df.reset_index(inplace=True)
    historical_df["Date"] = historical_df["Date"].astype(str)

    df = df.merge(historical_df, left_on="x", right_on="Date")
    df = df[["x", "y", "Close", "rating"]]

    cur.executemany("INSERT IGNORE INTO fear_and_greed VALUES (%s, %s, %s, %s)", df.values.tolist())

    print("CNN fear and greed Successfully Completed...\n")


if __name__ == '__main__':
    main()
