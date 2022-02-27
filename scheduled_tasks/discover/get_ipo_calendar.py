import os
import sys
import yaml
import finnhub
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database

cnx, engine = connect_mysql_database()

with open("config.yaml") as config_file:
    config_keys = yaml.load(config_file, Loader=yaml.Loader)

finnhub_client = finnhub.Client(api_key=config_keys["FINNHUB_KEY1"])


def main():
    """
    Get recent and past IPOs
    """
    today_date = datetime.utcnow().date()
    data = finnhub_client.ipo_calendar(_from=str(today_date - timedelta(days=100)),
                                       to=str(today_date + timedelta(days=50)))

    df = pd.DataFrame(data["ipoCalendar"])
    df.columns = ["Date", "Exchange", "Name", "Number Shares", "Expected Price", "Status", "Symbol", "Mkt Cap"]
    df = df[["Date", "Symbol", "Name", "Expected Price", "Number Shares", "Mkt Cap", "Status", "Exchange"]]
    df.fillna("-", inplace=True)
    df.replace("", "-", inplace=True)
    df["Status"] = df["Status"].str.capitalize()
    print(df)
    df.to_sql("ipo_calendar", engine, if_exists="replace", index=False)


if __name__ == '__main__':
    main()
