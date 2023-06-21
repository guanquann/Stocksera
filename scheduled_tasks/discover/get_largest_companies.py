import io
import os
import sys
import requests
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import header, get_ticker_list_stats, connect_mysql_database, long_number_format

cnx, cur, engine = connect_mysql_database()


def main():
    print("Getting Largest Companies...")
    s = requests.get("https://companiesmarketcap.com/?download=csv", headers=header).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    df["Symbol"] = df["Symbol"].astype(str)
    df = df[~df["Symbol"].str.contains(r"\.")]
    df = df.head(500)

    stats_df = pd.DataFrame(get_ticker_list_stats(df["Symbol"].to_list()))
    stats_df = stats_df[["symbol", "price", "changesPercentage", "marketCap"]]
    stats_df["marketCap"] = stats_df["marketCap"].apply(lambda x: long_number_format(x))
    stats_df = stats_df.rename(columns={"symbol": "Ticker", "price": "Price", "change": "Change",
                                        "changesPercentage": "% Change", "marketCap": "Market Cap"})

    stats_df.to_sql("largest_companies", engine, if_exists="replace", index=False)
    print("Largest Companies Successfully Completed...\n")


if __name__ == '__main__':
    main()
