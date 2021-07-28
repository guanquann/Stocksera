# import pandas as pd
# x = pd.read_html("https://apps.newyorkfed.org/markets/autorates/tomo-results-display?SHOWMORE=TRUE&startDate=01/01/2000&enddate=01/01/2000")
#
# print(x[3].iloc[2, 0])
# print()
# # print(x[3].iloc[4, 0])
# print(x[3].iloc[6, 0])
# print()
# print(x[3].iloc[10, 0])
# print(x[6])
# print(x[10])

from datetime import datetime
import sqlite3
import pandas as pd
import yfinance.ticker as yf
import requests_cache

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                'Chrome/91.0.4472.124 Safari/537.36'

df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits", "Symbol"])
db.execute("SELECT DISTINCT(ticker) FROM reddit_etf")
for symbol in db.fetchall():
    print(symbol[0])
    ticker_df = yf.Ticker(symbol[0]).history(interval="1d", period="1y")
    ticker_df["Symbol"] = symbol[0]
    df = df.append(ticker_df)
    # ticker_df = yf.Ticker(symbol).history(interval="1d", period="1y")
    # ticker_df["Symbol"] = symbol
    # df = df.append(ticker_df)

df.reset_index(inplace=True)
df["index"] = df["index"].astype(str)

print(len(df), "LEN")
price_dict = dict()
price_list = []
current_date = ""
db.execute("SELECT * FROM wallstreetbets")
for i in db.fetchall()[:1436]:
    if i[0] in range(1, 11):
        date_string = i[-3].split()[0]
        date = date_string[6:] + "-" + date_string[3:5] + "-" + date_string[:2]
        try:
            price = df[(df["index"] == date) & (df["Symbol"] == i[1])]["Open"].iloc[0]
            if i[1] in price_list:
                price_list.remove(i[1])

            # if len(price_list) == 1 and date != "2021-05-28":
            #     price_dict.pop(price_list[0])

            if i[1] not in price_dict:
                price_dict[i[1]] = round(price, 3)
                #####
                if current_date != date:
                    price_list = list(price_dict.keys())
                    current_date = date

            # if len(price_dict) <= 10:
            #     price_dict[i[1]] = round(price, 3)
            #     price_list = list(price_dict.keys())
            print(i[0], i[1], date)
            print(price_dict, '\n', price_list)
            print()
        except IndexError:
            # print("error")
            continue
# print(df)
