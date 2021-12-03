import sqlite3
import requests
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("database/database.db", check_same_thread=False)
db = conn.cursor()


def get_trending_ticker():
    trending = requests.get("https://api.stocktwits.com/api/2/trending/symbols.json").json()["symbols"]
    df = pd.DataFrame.from_dict(trending)[["symbol", "watchlist_count"]]
    df["date_updated"] = str(datetime.utcnow()).split(":")[0] + ":00"
    df.index += 1
    df.reset_index(inplace=True)
    df.rename(columns={"index": "rank", "watchlist_count": "watchlist"}, inplace=True)
    print(df.head(5))
    df.to_sql("stocktwits_trending", conn, if_exists="append", index=False)


if __name__ == '__main__':
    get_trending_ticker()
