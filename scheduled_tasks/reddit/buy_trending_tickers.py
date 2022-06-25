import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..//..'))
from helpers import *

cnx, cur, engine = connect_mysql_database()
cur = cnx.cursor(buffered=True)

from datetime import datetime, timedelta

start_datetime = str(datetime.utcnow() - timedelta(days=0))
previous_datetime = str(datetime.utcnow() - timedelta(days=1))
previous_previous_datetime = str(datetime.utcnow() - timedelta(days=2))

cur.execute("SELECT ticker FROM wsb_trending_24H where date_updated >= %s AND date_updated <= %s AND ticker NOT IN "
            "('SPY', 'QQQ', 'TQQQ', 'DIA') GROUP BY ticker ORDER BY SUM(mentions) DESC LIMIT 10",
            (previous_previous_datetime, previous_datetime,))
previously_bought = cur.fetchall()
previously_bought = list(map(lambda x: x[0], previously_bought))

cur.execute("SELECT ticker FROM wsb_trending_24H where date_updated >= %s AND date_updated <= %s AND ticker NOT IN "
            "('SPY', 'QQQ', 'TQQQ', 'DIA') GROUP BY ticker ORDER BY SUM(mentions) DESC LIMIT 10", (previous_datetime, start_datetime))
to_buy = cur.fetchall()
to_buy = list(map(lambda x: x[0], to_buy))

print("Previous: ", previously_bought)
print("To buy: ", to_buy)


def get_open_price(ticker_selected, date_selected=datetime.utcnow().date()):
    ticker = yf.Ticker(ticker_selected)
    history_df = ticker.history(period="1y", interval="1d")
    history_df.reset_index(inplace=True)
    history_df["Date"] = history_df["Date"].astype(str)
    while (str(date_selected) in history_df["Date"].values) is False:
        date_selected = date_selected - timedelta(days=1)
    open_price = history_df[history_df["Date"] == str(date_selected)]["Open"].values[0]
    return open_price


def buy_tickers():
    cur.execute("SELECT * FROM wsb_etf WHERE status='Open'")
    stats = cur.fetchone()
    if stats is None:
        tickers_to_buy = to_buy
    else:
        update_previous_tickers()
        sell_tickers()
        tickers_to_buy = set(to_buy) - set(previously_bought)
    print("To buy, after removing duplicates: ", tickers_to_buy)
    for ticker_selected in tickers_to_buy:
        open_price = get_open_price(ticker_selected)
        print(ticker_selected, float(open_price))
        cur.execute("INSERT INTO wsb_etf VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (ticker_selected, previous_datetime.split()[0], round(open_price, 2),   # previous_datetime
                     "N/A", "N/A", "N/A", "Open"))
        cnx.commit()


def update_previous_tickers():
    cur.execute("SELECT * FROM wsb_etf WHERE status='Open'")
    tickers_bought = cur.fetchall()
    for stats in tickers_bought:
        ticker_selected = stats[0]
        latest_price = get_open_price(ticker_selected)

        buy_price = float(stats[2])

        difference = latest_price - buy_price
        percentage = round((difference / buy_price) * 100, 2)
        cur.execute("UPDATE wsb_etf SET percentage=%s WHERE ticker=%s AND status=%s",
                    (percentage, ticker_selected, "Open"))
        cnx.commit()


def sell_tickers():
    to_sell_tickers = set(previously_bought).difference(set(to_buy))
    print("To sell: ", to_sell_tickers)
    for ticker_selected in to_sell_tickers:
        latest_price = get_open_price(ticker_selected)
        print("selling {} now...".format(ticker_selected))
        cur.execute("UPDATE wsb_etf SET close_date=%s, close_price=%s, status=%s WHERE ticker=%s AND status=%s",
                    (start_datetime.split()[0], latest_price, "Close", ticker_selected, "Open"))
        cnx.commit()


if __name__ == '__main__':
    # sell_tickers()
    # update_previous_tickers()
    buy_tickers()
