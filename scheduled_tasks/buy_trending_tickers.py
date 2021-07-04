import sqlite3
import logging
from datetime import datetime

import yfinance.ticker as yf

logging.basicConfig(filename='logging.log', level=logging.INFO)

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

db.execute("SELECT * FROM reddit_etf WHERE status=?", ("Open", ))
prev_bought = db.fetchall()
prev_bought_ticker = []
for bought in prev_bought:
    prev_bought_ticker.append(bought[0])
new_bought_ticker = []


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
    db.execute("SELECT * FROM wallstreetbets where date_updated=? ORDER BY total DESC LIMIT 10", (raw_date,))
    rows = db.fetchall()
    for y in rows:
        symbol = y[1]
        if symbol not in prev_bought_ticker:
            ticker = yf.Ticker(symbol)
            logo_url = ticker.info["logo_url"]
            history = ticker.history(period="1mo", interval="1d")
            try:
                info = history.loc[latest_date]
            except KeyError:
                print("Market not open today! No tickers bought!")
                break
            open_price = round(info["Open"], 2)
            num_shares = round(10000 / open_price, 2)
            message = "Ticker {} to be bought on {} for ${}.".format(symbol, str(latest_date).split()[0], open_price)
            print(message)
            logging.info(message)
            db.execute("INSERT INTO reddit_etf VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (symbol, logo_url, str(latest_date).split()[0], open_price, num_shares,
                        "N/A", "N/A", "N/A", "N/A", "Open"))
            conn.commit()


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

    db.execute("SELECT * FROM wallstreetbets where date_updated=? ORDER BY total DESC LIMIT 10", (raw_date,))
    rows = db.fetchall()
    for ticker in rows:
        symbol = ticker[1]
        new_bought_ticker.append(symbol)

    sell = list(set(prev_bought_ticker)-set(new_bought_ticker))
    for symbol in sell:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo", interval="1d")
        try:
            info = history.loc[latest_date]
        except KeyError:
            print("Market not open today! No tickers sold!")
            break
        close_price = round(info["Open"], 3)
        message = "Ticker {} to be sold on {} at ${} during market open.".format(symbol, str(latest_date).split()[0], close_price)
        print(message)
        logging.info(message)
        db.execute("SELECT * FROM reddit_etf WHERE ticker=? AND status='Open'", (symbol, ))
        stats = db.fetchone()
        difference = round(close_price - stats[3], 2)
        PnL = round(difference * stats[4], 2)
        percentage_diff = round((difference / stats[3]) * 100, 2)
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
    for ticker in open_ticker_list:
        ticker_stats = yf.Ticker(ticker[0])
        buy_price = ticker[3]
        today_price = round(ticker_stats.info["regularMarketPrice"], 2)
        difference = today_price - buy_price
        PnL = round(difference * ticker[4], 2)
        percentage_diff = round((difference / ticker[3]) * 100, 2)
        db.execute("UPDATE reddit_etf SET close_price=?, PnL=?, percentage=? "
                   "WHERE ticker=? AND status='Open'", (today_price, PnL, percentage_diff, ticker[0]))
        conn.commit()


if __name__ == '__main__':
    db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
    db_date = db.fetchone()[0]
    buy_new_ticker(db_date)
    sell_ticker(db_date)
    update_bought_ticker_price()
