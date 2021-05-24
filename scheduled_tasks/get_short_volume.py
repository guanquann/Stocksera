import sqlite3

from helpers import *

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()


def short_volume(symbol):
    url = "http://shortvolumes.com/?t={}".format(symbol)
    table = pd.read_html(url)
    try:
        shorted_vol_daily = table[3].iloc[2:]
        for index, row in shorted_vol_daily.iterrows():
            db.execute("INSERT OR IGNORE INTO short_volume VALUES (?, ?, ?, ?, ?)",
                       (symbol, row[0], row[1], row[2], row[3]))
            conn.commit()
        print("{} INSERTED INTO SHORT-VOLUME DATABASE SUCCESSFULLY".format(symbol))
    except IndexError:
        print("{} NOT FOUND!".format(symbol))


list_of_tickers = ["GME", "AMC", "BB", "CLOV", "UWMC", "NIO", "TSLA", "AAPL", "SPY", "NOK", "AMD", "NVDA", "MSFT",
                   "RBLX", "F", "PLTR", "COIN", "RKT", "MVIS", "FUBO", "DISCA", "VIAC", "SNDL", "SPCE", "FB", "SNAP",
                   "OCGN", "QQQ", "TQQQ", "ROKU", "TWTR", "ARKK", "ARKF", "ARKG", "ARKQ", "GOOG", "INTC", "BABA",
                   "IWM", "GOOGL", "BA", "SQ", "SHOP", "SE", "VOO", "PYPL"]
for i in list_of_tickers:
    short_volume(i)
