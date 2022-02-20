import os
import sys
import requests
import pandas as pd

from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, engine = connect_mysql_database()
cur = cnx.cursor()


def download_json(date_to_start: str = str(datetime.utcnow().date() - timedelta(days=14))):
    """
    Get daily treasury by reading from json file (no actions needed)
    Parameters
    ----------
    date_to_start : str
        format: YYYY-MM-DD
    """
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/dts_table_1" \
          "?fields=record_date,account_type,close_today_bal,open_today_bal,open_month_bal&" \
          "filter=record_date:gte:{}".format(date_to_start)
    data = requests.get(url).json()['data']
    for i in data:
        if i["account_type"] == "Treasury General Account (TGA)":
            record_date = i['record_date']
            close_today = int(i['close_today_bal']) / 1000
            open_today = int(i['open_today_bal']) / 1000
            amount_change = round(close_today - open_today, 2)
            percent_change = round((amount_change / open_today) * 100, 2)
            cur.execute("INSERT IGNORE INTO daily_treasury VALUES (%s, %s, %s, %s, %s)",
                        (record_date, close_today, open_today, amount_change, percent_change))
            cnx.commit()


def download_csv_manual(file_path: str):
    """
    Get daily treasury by reading from csv file (you need to download csv file manually from
    https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/operating-cash-balance first)
    Parameters
    ----------
    file_path : str
        path of csv file
    """
    df = pd.read_csv(file_path)
    df = df[(df["Type of Account"] == "Federal Reserve Account") |
            (df["Type of Account"] == "Treasury General Account (TGA)")]
    for index, row in df[::-1].iterrows():
        record_date = row['Record Date']
        print(record_date)
        close_today = int(row['Closing Balance Today']) / 1000
        open_today = int(row['Opening Balance Today']) / 1000
        amount_change = round(close_today - open_today, 2)
        percent_change = round((amount_change / open_today) * 100, 2)
        cur.execute("INSERT IGNORE INTO daily_treasury VALUES (%s, %s, %s, %s, %s)",
                    (record_date, close_today, open_today, amount_change, percent_change))
        cnx.commit()


if __name__ == '__main__':
    download_csv_manual(r"C:\Users\Acer\Downloads\DTS_OpCashBal_20170217_20220217\DTS_OpCashBal_20170217_20220217.csv")
    # download_json()
