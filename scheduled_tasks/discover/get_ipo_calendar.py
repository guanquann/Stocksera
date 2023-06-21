import os
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database, finnhub_client

cnx, cur, engine = connect_mysql_database()


def main():
    """
    Get recent and past IPOs
    """
    print("Getting IPO...")
    today_date = datetime.utcnow().date()
    data = finnhub_client.ipo_calendar(_from=str(today_date - timedelta(days=100)),
                                       to=str(today_date + timedelta(days=50)))

    df = pd.DataFrame(data["ipoCalendar"])
    df.columns = ["Date", "Exchange", "Name", "Number Shares", "Expected Price", "Status", "Symbol", "Mkt Cap"]
    df = df[["Date", "Symbol", "Name", "Expected Price", "Number Shares", "Mkt Cap", "Status", "Exchange"]]
    df.fillna("-", inplace=True)
    df.replace("", "-", inplace=True)
    df["Status"] = df["Status"].str.capitalize()
    df.to_sql("ipo_calendar", engine, if_exists="replace", index=False)
    print("IPO Successfully Completed...\n")


if __name__ == '__main__':
    main()
