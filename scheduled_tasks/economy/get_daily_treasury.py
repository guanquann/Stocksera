import os
import sys
import requests

from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def download_json(date_to_start: str = str(datetime.utcnow().date() - timedelta(days=14))):
    """
    Get daily treasury by reading from json file (no actions needed)
    Parameters
    ----------
    date_to_start : str
        format: YYYY-MM-DD
    """
    print("Getting Daily Treasury...")
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/dts_table_1" \
          "?fields=record_date,account_type,close_today_bal,open_today_bal,open_month_bal&" \
          "filter=record_date:gte:{}".format(date_to_start)
    data = requests.get(url).json()['data']
    for i in data:
        if i["account_type"] == "Treasury General Account (TGA) Opening Balance":
            open_today = int(i['open_today_bal']) / 1000
        if i["account_type"] == "Treasury General Account (TGA) Closing Balance":
            record_date = i['record_date']
            close_today = int(i['open_today_bal']) / 1000
            amount_change = round(close_today - open_today, 2)
            percent_change = round((amount_change / open_today) * 100, 2)
            cur.execute("INSERT IGNORE INTO daily_treasury VALUES (%s, %s, %s, %s, %s)",
                        (record_date, close_today, open_today, amount_change, percent_change))
            cnx.commit()
    print("Daily Treasury Successfully Completed...\n")


if __name__ == '__main__':
    download_json()
