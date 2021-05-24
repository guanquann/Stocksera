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
    raw_date = date
    latest_date = date
    if " " in latest_date:
        latest_date = latest_date.split()[0]
        latest_date = datetime.strptime(latest_date, "%d/%m/%Y")
    db.execute("SELECT * FROM wallstreetbets where date_updated=? LIMIT 10", (raw_date,))
    rows = db.fetchall()
    for y in rows:
        symbol = y[0]

        if symbol not in prev_bought_ticker:
            ticker = yf.Ticker(symbol)
            # history = ticker.history(period="1mo", interval="1d")
            information = ticker.info
            # try:
            #     info = history.loc[latest_date]
            # except KeyError:
            #     print("Market not open today! No tickers bought!")
            #     break
            # open_price = round(info["Open"], 2)
            open_price = round(information["regularMarketOpen"], 2)
            num_shares = round(10000 / open_price, 2)
            message = "Ticker {} to be bought on {} for ${}.".format(symbol, str(latest_date).split()[0], open_price)
            print(message)
            logging.info(message)
            db.execute("INSERT INTO reddit_etf VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (symbol, str(latest_date).split()[0], open_price, num_shares, "N/A", "N/A", "Open"))
            conn.commit()


def sell_ticker(date):
    raw_date = date
    latest_date = date
    if " " in latest_date:
        latest_date = latest_date.split()[0]
        latest_date = datetime.strptime(latest_date, "%d/%m/%Y")

    db.execute("SELECT * FROM wallstreetbets where date_updated=? LIMIT 10", (raw_date,))
    rows = db.fetchall()
    for ticker in rows:
        symbol = ticker[0]
        new_bought_ticker.append(symbol)

    sell = list(set(prev_bought_ticker)-set(new_bought_ticker))
    for symbol in sell:
        ticker = yf.Ticker(symbol)
        information = ticker.info
        # history = ticker.history(period="1mo", interval="1d")
        # try:
        #     info = history.loc[latest_date]
        # except KeyError:
        #     print("Market not open today! No tickers sold!")
        #     break
        # close_price = round(info["Open"], 2)
        close_price = round(information["regularMarketOpen"], 2)
        message = "Ticker {} to be sold on {} at ${} during market open.".format(symbol, str(latest_date).split()[0], close_price)
        print(message)
        logging.info(message)
        db.execute("UPDATE reddit_etf SET close_date=?, close_price=?, status=? WHERE ticker=?",
                   (str(latest_date).split()[0], close_price, "Close", symbol))
        conn.commit()
    logging.info("-" * 50)


if __name__ == '__main__':
    db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
    db_date = db.fetchone()[0]
    buy_new_ticker(db_date)
    sell_ticker(db_date)
