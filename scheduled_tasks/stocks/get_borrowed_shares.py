import os
import sys
import ftplib
from io import BytesIO
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, engine = connect_mysql_database()
cur = cnx.cursor()


def main():
    """
    Get shares available to borrow and fee to borrow from Interactive Brokers
    """
    ftp = ftplib.FTP('ftp3.interactivebrokers.com', 'shortstock')

    flo = BytesIO()
    ftp.retrbinary('RETR usa.txt', flo.write)
    flo.seek(0)

    df = pd.read_csv(flo, sep="|", skiprows=1)
    df = df[["#SYM", "FEERATE", "AVAILABLE"]]
    df.columns = ["ticker", "fee", "available"]
    df = df[~df["fee"].isna()]
    df["date_updated"] = str(datetime.utcnow() - timedelta(hours=5)).rsplit(":", 1)[0]
    df["available"] = df["available"].replace(">10000000", 10000000)
    print(df)

    cur.executemany("INSERT IGNORE INTO shares_available VALUES (%s, %s, %s, %s)", df.values.tolist())
    cnx.commit()

    ftp.quit()


if __name__ == '__main__':
    main()
