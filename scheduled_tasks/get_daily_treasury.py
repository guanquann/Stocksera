import sqlite3
import requests
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def download_json(date_to_start: str = str(datetime.utcnow().date() - timedelta(days=14))):
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/dts_table_1" \
          "?fields=record_date,account_type,close_today_bal,open_today_bal,open_month_bal&" \
          "filter=record_date:gte:{}".format(date_to_start)
    data = requests.get(url).json()['data']
    for i in data:
        if i["account_type"] == "Federal Reserve Account":
            record_date = i['record_date']
            close_today = int(i['close_today_bal']) / 1000
            open_today = int(i['open_today_bal']) / 1000
            amount_change = round(close_today - open_today, 2)
            percent_change = round((amount_change / open_today) * 100, 2)
            db.execute("INSERT OR IGNORE INTO daily_treasury VALUES (?, ?, ?, ?, ?)",
                       (record_date, close_today, open_today, amount_change, percent_change))
            conn.commit()


def download_csv_manual(file_path):
    df = pd.read_csv(file_path)
    df = df[df["Type of Account"] == "Federal Reserve Account"]
    for index, row in df[::-1].iterrows():
        record_date = row['Record Date']
        close_today = int(row['Closing Balance Today']) / 1000
        open_today = int(row['Opening Balance Today']) / 1000
        amount_change = round(close_today - open_today, 2)
        percent_change = round((amount_change / open_today) * 100, 2)
        db.execute("INSERT OR IGNORE INTO daily_treasury VALUES (?, ?, ?, ?, ?)",
                   (record_date, close_today, open_today, amount_change, percent_change))
        conn.commit()


if __name__ == '__main__':
    download_json()
