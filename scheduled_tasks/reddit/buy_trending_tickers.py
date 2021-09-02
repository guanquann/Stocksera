import os
import sys
import sqlite3
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..\\..'))
from fast_yahoo import *

logging.basicConfig(filename=r'database/logging.log', level=logging.INFO)

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

db.execute("SELECT * FROM reddit_etf WHERE status=?", ("Open", ))
prev_bought = db.fetchall()
prev_bought_ticker = []
for bought in prev_bought:
    prev_bought_ticker.append(bought[0])
new_bought_ticker = []
print("Previously bought tickers: ", prev_bought_ticker)


def buy_new_ticker(date):
    """
    Buy ticker if ticker is inside the Top 10 popular tickers on r/wallstreetbets
    Note: Run this function after running scheduled_tasks/main.py to get most trending tickers on Reddit
    Parameters
    ----------
    date: str
        Format: DD/MM/YYYY HH:MM:SS
    """
    raw_date = date
    latest_date = date
    if " " in latest_date:
        latest_date = latest_date.split()[0]
        latest_date = datetime.strptime(latest_date, "%d/%m/%Y")
    db.execute("SELECT ticker FROM wallstreetbets where date_updated=? AND ticker NOT IN "
               "('SPY', 'QQQ', 'TQQQ', 'DIA') ORDER BY total DESC LIMIT 10", (raw_date,))
    rows = db.fetchall()
    rows = list(map(lambda x: x[0], rows))
    rows = download_advanced_stats(rows)
    for symbol, info in rows.items():
        if symbol not in prev_bought_ticker:
            if info["marketState"] == "CLOSED":
                print("Market not open today! No tickers bought!")
                break
            open_price = round(float(info["regularMarketOpen"]), 2)
            num_shares = round(10000 / open_price, 2)
            message = "Ticker {} to be bought on {} for ${}.".format(symbol, str(latest_date).split()[0], open_price)
            print(message)
            logging.info(message)
            db.execute("INSERT INTO reddit_etf VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (symbol, str(latest_date).split()[0], open_price, num_shares,
                        "N/A", "N/A", "N/A", "N/A", "Open"))
            conn.commit()
        else:
            print("{} not bought, since it is already Top-10 in the previous day!".format(symbol))


def sell_ticker(date):
    """
    Sell ticker if ticker is outside the Top 10 popular tickers on r/wallstreetbets
    Note: Run this function after running scheduled_tasks/main.py to get most trending tickers on Reddit
    Parameters
    ----------
    date: str
        Format: DD/MM/YYYY HH:MM:SS
    """
    raw_date = date
    latest_date = date
    if " " in latest_date:
        latest_date = latest_date.split()[0]
        latest_date = datetime.strptime(latest_date, "%d/%m/%Y")

    db.execute("SELECT ticker FROM wallstreetbets where date_updated=? AND ticker NOT IN "
               "('SPY', 'QQQ', 'TQQQ', 'DIA') ORDER BY total DESC LIMIT 10", (raw_date,))

    rows = db.fetchall()
    rows = list(map(lambda x: x[0], rows))
    rows = download_advanced_stats(rows)

    for symbol, info in rows.items():
        new_bought_ticker.append(symbol)
    sell = list(set(prev_bought_ticker)-set(new_bought_ticker))
    for symbol in sell:
        info = rows[symbol]
        if info["marketState"] == "CLOSED":
            print("Market not open today! No tickers sold!")
            break
        close_price = round(float(info["regularMarketOpen"]), 3)
        message = "Ticker {} to be sold on {} at ${} during market open.".format(symbol, str(latest_date).split()[0], close_price)
        print(message)
        logging.info(message)
        db.execute("SELECT * FROM reddit_etf WHERE ticker=? AND status='Open'", (symbol, ))
        stats = db.fetchone()
        difference = round(close_price - stats[2], 2)
        PnL = round(difference * stats[4], 2)
        percentage_diff = round((difference / stats[2]) * 100, 2)
        db.execute("UPDATE reddit_etf SET close_date=?, close_price=?, PnL=?, percentage=?, status=? "
                   "WHERE ticker=? AND status=?", (str(latest_date).split()[0], close_price, PnL, percentage_diff,
                                                   "Close", symbol, "Open"))
        conn.commit()
    logging.info("-" * 50)


def update_bought_ticker_price():
    """
    Update price of ticker inside the Top 10 popular tickers on r/wallstreetbets
    Note: Run this function after running scheduled_tasks/main.py to get most trending tickers on Reddit
    """
    print("Updating ticker price now...")
    db.execute("SELECT * FROM reddit_etf WHERE status='Open'")
    open_ticker_list = db.fetchall()

    rows = list(map(lambda x: x[0], open_ticker_list))
    rows = download_advanced_stats(rows)

    for ticker in open_ticker_list:
        info = rows[ticker[0]]
        buy_price = ticker[2]
        today_price = round(float(info["regularMarketPrice"]), 2)
        difference = today_price - buy_price
        PnL = round(difference * ticker[3], 2)
        percentage_diff = round((difference / buy_price) * 100, 2)
        db.execute("UPDATE reddit_etf SET close_price=?, PnL=?, percentage=? "
                   "WHERE ticker=? AND status='Open'", (today_price, PnL, percentage_diff, ticker[0]))
        conn.commit()
        print("Update {} Successful!".format(ticker[0]))


if __name__ == '__main__':
    db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
    db_date = db.fetchone()[0]
    buy_new_ticker(db_date)
    sell_ticker(db_date)
    update_bought_ticker_price()
