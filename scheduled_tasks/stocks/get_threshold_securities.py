import os
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def main(start_date=datetime.utcnow() - timedelta(days=5), end_date=datetime.utcnow()):
    """
    Get stocks in threshold securities list
    """
    print("Getting Threshold Security...")
    while start_date != end_date:
        current_date = start_date

        formatted_date = current_date.strftime("%d-%b-%Y")
        nyse_df = pd.read_csv(f"https://www.nyse.com/api/regulatory/threshold-securities/download?"
                              f"selectedDate={formatted_date}", delimiter="|")[:-1]
        nyse_df = nyse_df[["Symbol"]]
        df = nyse_df

        formatted_date = current_date.strftime("%Y%m%d")
        try:
            nasdaq_df = pd.read_fwf(f"http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{formatted_date}.txt",
                                    error_bad_lines=False)[:-1]
            nasdaq_df["Symbol"] = nasdaq_df["Symbol|Security Name|Market Category|Reg SHO"].astype(str).apply(lambda x: x.split("|")[0])
            nasdaq_df = nasdaq_df[["Symbol"]]
            df = df.append(nasdaq_df)
        except:
            pass

        df["date_updated"] = str(current_date).split()[0]
        df = df.rename(columns={"Symbol": "ticker"})

        cur.executemany("INSERT IGNORE INTO threshold_securities VALUES (%s, %s)", df.values.tolist())
        cnx.commit()
        start_date += timedelta(days=1)
    print("Threshold Security Successfully Completed...\n")


if __name__ == '__main__':
    main()
