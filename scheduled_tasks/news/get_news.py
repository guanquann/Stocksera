import os
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database, finnhub_client

cnx, cur, engine = connect_mysql_database()


def news(section="general"):
    df = pd.DataFrame(finnhub_client.general_news(section, min_id=0))
    df["datetime"] = df["datetime"].apply(lambda x: datetime.utcfromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))
    df = df[["datetime", "headline", "source", "url"]]
    df["section"] = section
    cur.executemany("INSERT IGNORE INTO market_news VALUES (%s, %s, %s, %s, %s)", df.values.tolist())
    cnx.commit()


def main():
    print("Getting Latest News...")
    news()
    news("crypto")
    news("forex")
    news("merger")
    print("Latest News Successfully Completed...\n")


if __name__ == '__main__':
    main()
