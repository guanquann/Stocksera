import os
import sys
import ftplib
from io import BytesIO
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def main():
    """
    Get shares available to borrow and fee to borrow from Interactive Brokers
    """
    print("Getting CTB...")

    full_ticker_df = pd.read_sql("SELECT DISTINCT(ticker) FROM shares_available", cnx)

    ftp = ftplib.FTP('ftp2.interactivebrokers.com', 'shortstock')

    flo = BytesIO()
    ftp.retrbinary('RETR usa.txt', flo.write)
    flo.seek(0)

    df = pd.read_csv(flo, sep="|", skiprows=1)
    df = df[["#SYM", "FEERATE", "AVAILABLE"]]
    df.columns = ["ticker", "fee", "available"]
    df["available"] = df["available"].replace(">10000000", 10000000)
    df = pd.concat([df, full_ticker_df])
    df = df.drop_duplicates(subset="ticker", keep="first")
    df["date_updated"] = str(datetime.utcnow() - timedelta(hours=5)).rsplit(":", 1)[0]
    df.fillna(0, inplace=True)

    cur.executemany("INSERT IGNORE INTO shares_available VALUES (%s, %s, %s, %s)", df.values.tolist())
    cnx.commit()

    tmp_df = df[["ticker", "fee", "available"]]
    tmp_df = tmp_df.sort_values(by="fee", ascending=False)
    cur.execute("DELETE FROM highest_shares_available")
    cur.executemany("INSERT INTO highest_shares_available VALUES (%s, %s, %s)", tmp_df.head(50).values.tolist())
    cnx.commit()

    ftp.quit()
    print("CTB Successfully Completed...\n")


if __name__ == '__main__':
    main()
