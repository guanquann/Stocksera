import os
import sys
import sqlite3
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scheduled_tasks.get_popular_tickers import full_ticker_list
from helpers import *

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


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
        print("{} INSERTED INTO SHORT-VOLUME DATABASE SUCCESSFULLY".format(symbol))
    except IndexError:
        print("{} NOT FOUND!".format(symbol))


if __name__ == '__main__':
    for i in full_ticker_list():
        short_volume(i)
