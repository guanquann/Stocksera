import os
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def main(start_date=datetime.utcnow() - timedelta(days=365), end_date=datetime.utcnow()):
    """
    Get stocks in threshold securities list
    """
    while start_date != end_date:
        print(start_date)
        current_date = start_date
        formatted_date = current_date.strftime("%d-%b-%Y")
        df = pd.read_csv(f"https://www.nyse.com/api/regulatory/threshold-securities/download?"
                         f"selectedDate={formatted_date}", delimiter="|")[:-1]
        df = df[["Symbol"]]
        df["date_updated"] = str(current_date).split()[0]
        df = df.rename(columns={"Symbol": "ticker"})
        print(df)
        cur.executemany("INSERT IGNORE INTO threshold_securities VALUES (%s, %s)", df.values.tolist())
        start_date += timedelta(days=1)


if __name__ == '__main__':
    main()
