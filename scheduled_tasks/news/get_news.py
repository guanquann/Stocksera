import os
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database, finnhub_client2

cnx, cur, engine = connect_mysql_database()


def main(section="general"):
    df = pd.DataFrame(finnhub_client2.general_news(section, min_id=0))
    df["datetime"] = df["datetime"].apply(lambda x: datetime.utcfromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))
    df = df[["datetime", "headline", "source", "url"]]
    df["section"] = section
    print(df)

    cur.executemany("INSERT IGNORE INTO market_news VALUES (%s, %s, %s, %s, %s)", df.values.tolist())
    cnx.commit()


if __name__ == '__main__':
    main()
    main("crypto")
    main("forex")
    main("merger")
