import io
import os
import sys
import sqlite3
import requests
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scheduled_tasks.get_popular_tickers import full_ticker_list

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

current_date = datetime.now().date()


def short_volume(symbol):
    """
    Get short volume data from http://shortvolumes.com
    Parameters
    ----------
    symbol: str
        ticker symbol (e.g: AAPL)
    """
    url = "http://shortvolumes.com/?t={}".format(symbol)
    table = pd.read_html(url)
    print("-" * 100)
    print(f"Getting short volume data for {symbol} now ...")
    try:
        shorted_vol_daily = table[3].iloc[2:]

        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo", interval="1d")

        for index, row in shorted_vol_daily.iterrows():
            date = datetime.strptime(row[0], "%Y-%m-%d")
            close_price = round(history.loc[date]["Close"], 2)
            db.execute("INSERT OR IGNORE INTO short_volume VALUES (?, ?, ?, ?, ?, ?)",
                       (symbol, row[0], close_price, row[1], row[2], row[3]))
            conn.commit()
        print("Short volume data for {} collected successfully!".format(symbol))
    except IndexError:
        print("Short volume data for {} not found!".format(symbol))


def get_monthly_data_finra():
    last_date = datetime.now().date() - timedelta(days=30)
    combined_df = pd.DataFrame(columns=["Date", "Symbol", "ShortVolume", "ShortExemptVolume", "TotalVolume", "%Shorted"])
    while current_date != last_date:
        print("Looking at " + str(last_date))
        url = r"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{}.txt".format(str(last_date).replace("-", ""))
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), delimiter="|")

        if len(df) == 1:
            print("No data for " + str(last_date) + "\n")
        else:
            del df["Market"]
            df["%Shorted"] = 100 * (df["ShortVolume"] / df["TotalVolume"])
            df["%Shorted"] = df["%Shorted"].round(2)
            combined_df = combined_df.append(df)
        last_date = last_date + timedelta(days=1)

    combined_df["Date"] = combined_df["Date"].astype(str)
    combined_df["Date"] = combined_df["Date"].apply(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:])
    combined_df.columns = ["Date", "ticker", "short_vol", "short_exempt_vol", "total_vol", "percent"]
    combined_df.to_csv("database/short_volume.csv", index=False)


def get_daily_data_finra(date_to_process: datetime.date = datetime.now().date()):
    url = r"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{}.txt".format(str(date_to_process).replace("-", ""))
    print(url)
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')), delimiter="|")
    if len(df) == 1:
        print("No data for " + str(date_to_process) + "\n")
    else:
        df["Date"] = df["Date"].astype(str).apply(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:])
        df["%Shorted"] = 100 * (df["ShortVolume"] / df["TotalVolume"])
        df["%Shorted"] = df["%Shorted"].round(2)
        for symbol in full_ticker_list():
            ticker = yf.Ticker(symbol)
            print(symbol)
            history = ticker.history(period="1y", interval="1d")
            row = df[df["Symbol"] == symbol]
            if not row.empty:
                date = row["Date"].values[0]
                close_price = round(history.loc[date]["Close"], 2)
                db.execute("INSERT OR IGNORE INTO short_volume VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (date, symbol, row["ShortVolume"].values[0], row["ShortExemptVolume"].values[0],
                            row["TotalVolume"].values[0], row["%Shorted"].values[0], close_price))
                conn.commit()
            else:
                print("No data for ", symbol)


if __name__ == '__main__':
    get_monthly_data_finra()
    # get_daily_data_finra()
