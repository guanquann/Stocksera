import io
import os
import sys
import sqlite3
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scheduled_tasks.get_popular_tickers import full_ticker_list
import scheduled_tasks.reddit.get_reddit_trending_stocks.fast_yahoo as fast_yahoo

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


def get_30d_data_finra():
    """
    Get short volume data from https://cdn.finra.org/
    This is an alternative source to shortsvolume.com because shortsvolume.com stopped updating for some reason
    But this is better in the sense that it gets all tickers short volume for the last 30 days and save them to csv
    """
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


def get_daily_data_finra(date_to_process: datetime.date = datetime.now().date() - timedelta(days=1)):
    """
    Get short volume data from https://cdn.finra.org/
    This function gets daily data for popular tickers in scheduled_tasks/get_popular_tickers.py and save them to db
    """
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

        highest_shorted = df[df["ShortVolume"] >= 3000000].nlargest(50, "%Shorted")
        del highest_shorted["Date"]
        del highest_shorted["Market"]
        highest_shorted.index = np.arange(1, len(highest_shorted) + 1)
        highest_shorted.reset_index(inplace=True)
        highest_shorted.rename(columns={"index": "Rank",
                                        "ShortVolume": "Short Volume",
                                        "ShortExemptVolume": "Short Exempt Vol",
                                        "TotalVolume": "Total Volume",
                                        "%Shorted": "% Shorted"}, inplace=True)

        quick_stats = {'regularMarketPreviousClose': 'Previous Close',
                       'regularMarketChangePercent': '1 Day Change %',
                       'marketCap': 'Market Cap'}
        stats_df = fast_yahoo.download_quick_stats(highest_shorted["Symbol"].to_list(), quick_stats)

        highest_shorted = pd.merge(highest_shorted, stats_df, on="Symbol")
        highest_shorted.replace(np.nan, "N/A", inplace=True)
        highest_shorted.to_csv("database/highest_short_volume.csv", index=False)

        for symbol in full_ticker_list():
            ticker = yf.Ticker(symbol)
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
    get_30d_data_finra()
    get_daily_data_finra()
