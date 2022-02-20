import os
import sys
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..\\..'))
from fast_yahoo import *
from helpers import connect_mysql_database

cnx, engine = connect_mysql_database()
cur = cnx.cursor()

logging.basicConfig(filename=r'database/logging.log', level=logging.INFO)

cur.execute("SELECT * FROM reddit_etf WHERE status=%s", ("Open", ))
prev_bought = cur.fetchall()
prev_bought_ticker = []
for bought in prev_bought:
    prev_bought_ticker.append(bought[0])


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
    cur.execute("SELECT ticker FROM wallstreetbets where date_updated=%s AND ticker NOT IN "
                "('SPY', 'QQQ', 'TQQQ', 'DIA') ORDER BY total DESC LIMIT 10", (raw_date,))
    rows = cur.fetchall()
    rows = list(map(lambda x: x[0], rows))
    rows = download_advanced_stats(rows)
    for symbol, info in rows.items():
        if symbol not in prev_bought_ticker:
            if info["marketState"] != "REGULAR":
                print("Market not open currently! {} not bought!".format(symbol))
                continue
            open_price = round(float(info["regularMarketOpen"].replace(",", "")), 2)
            num_shares = round(10000 / open_price, 2)
            message = "Ticker {} to be bought on {} for ${}.".format(symbol, str(latest_date).split()[0], open_price)
            print(message)
            logging.info(message)
            cur.execute("INSERT INTO reddit_etf VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (symbol, str(latest_date).split()[0], open_price, num_shares,
                         "N/A", "N/A", "N/A", "N/A", "Open"))
            cnx.commit()
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

    cur.execute("SELECT ticker FROM wallstreetbets where date_updated=%s AND ticker NOT IN "
                "('SPY', 'QQQ', 'TQQQ', 'DIA') ORDER BY total DESC LIMIT 10", (raw_date,))

    rows = cur.fetchall()
    rows = list(map(lambda x: x[0], rows))
    new_bought_ticker = rows

    sell = list(set(prev_bought_ticker)-set(new_bought_ticker))
    rows = download_advanced_stats(sell)
    print(sell, "yes")
    for symbol in sell:
        info = rows[symbol]
        if info["marketState"] != "REGULAR":
            print("Market not open currently! {} not sold!".format(symbol))
            continue
        close_price = round(float(info["regularMarketOpen"].replace(",", "")), 3)
        message = "Ticker {} to be sold on {} at ${} during market open.".format(symbol, str(latest_date).split()[0],
                                                                                 close_price)
        print(message)
        logging.info(message)
        cur.execute("SELECT * FROM reddit_etf WHERE ticker=%s AND status='Open'", (symbol, ))
        stats = cur.fetchone()
        difference = round(close_price - stats[2], 2)
        PnL = round(difference * stats[3], 2)
        percentage_diff = round((difference / stats[2]) * 100, 2)
        cur.execute("UPDATE reddit_etf SET close_date=%s, close_price=%s, PnL=%s, percentage=%s, status=%s "
                    "WHERE ticker=%s AND status=%s", (str(latest_date).split()[0], close_price, PnL, percentage_diff,
                                                      "Close", symbol, "Open"))
        cnx.commit()
    logging.info("-" * 50)


def update_bought_ticker_price():
    """
    Update price of ticker inside the Top 10 popular tickers on r/wallstreetbets
    Note: Run this function after running scheduled_tasks/main.py to get most trending tickers on Reddit
    """
    print("Updating ticker price now...")
    cur.execute("SELECT * FROM reddit_etf WHERE status='Open'")
    open_ticker_list = cur.fetchall()

    rows = list(map(lambda x: x[0], open_ticker_list))
    rows = download_advanced_stats(rows)

    for ticker in open_ticker_list:
        info = rows[ticker[0]]
        buy_price = ticker[2]
        today_price = round(float(info["regularMarketPrice"].replace(",", "")), 2)
        difference = today_price - buy_price
        PnL = round(difference * ticker[3], 2)
        percentage_diff = round((difference / buy_price) * 100, 2)
        cur.execute("UPDATE reddit_etf SET close_price=%s, PnL=%s, percentage=%s "
                    "WHERE ticker=%s AND status='Open'", (today_price, PnL, percentage_diff, ticker[0]))
        cnx.commit()
        print("Update {} Successful!".format(ticker[0]))


if __name__ == '__main__':
    print("Previously bought tickers: ", prev_bought_ticker)
    cur.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
    db_date = cur.fetchone()[0]
    buy_new_ticker(db_date)
    sell_ticker(db_date)
    update_bought_ticker_price()
