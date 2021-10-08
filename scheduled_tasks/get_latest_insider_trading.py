import os
import sys
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from finvizfinance.insider import Insider

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from scheduled_tasks.reddit.get_reddit_trending_stocks.fast_yahoo import download_quick_stats

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def latest_insider_trading():
    for type_trading in ["buys", "sales"]:
        print("latest {}".format(type_trading))
        finsider = Insider(option="latest {}".format(type_trading))
        insider_trader = finsider.getInsider()
        print(insider_trader)
        insider_trader["Owner"] = insider_trader["Owner"].str.title()
        insider_trader = insider_trader[insider_trader["Value ($)"] >= 50000]

        insider_trader["Date"] = insider_trader["Date"] + " 2021"
        insider_trader["Date"] = pd.to_datetime(insider_trader["Date"], format="%b %d %Y")
        insider_trader["Date"] = insider_trader["Date"].astype(str)

        insider_trader["SEC Form 4"] = insider_trader["SEC Form 4"].apply(lambda x: x.rsplit(' ', 2)[0])
        insider_trader["SEC Form 4"] = insider_trader["SEC Form 4"] + " 2021"
        insider_trader["SEC Form 4"] = pd.to_datetime(insider_trader["SEC Form 4"], format="%b %d %Y")
        insider_trader["SEC Form 4"] = insider_trader["SEC Form 4"].astype(str)

        if type_trading == "sales":
            insider_trader["Value ($)"] = -insider_trader["Value ($)"]

        print(insider_trader)
        for index, row in insider_trader.iterrows():
            db.execute("INSERT OR IGNORE INTO latest_insider_trading VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,?)",
                       tuple(row))
            conn.commit()


def latest_insider_trading_analysis():
    last_date = str(datetime.utcnow().date() - timedelta(days=30))

    insider_df = pd.read_sql_query("SELECT Ticker, SUM(Value) AS Amount "
                                   "FROM latest_insider_trading WHERE "
                                   "DateFilled>='{}' GROUP BY Ticker ORDER BY "
                                   "ABS(SUM(Value)) DESC LIMIT 50".format(last_date), conn)
    quick_stats = {'marketCap': 'mkt_cap'}
    quick_stats_df = download_quick_stats(insider_df["Ticker"].to_list(), quick_stats, threads=True)
    insider_df["MktCap"] = quick_stats_df["mkt_cap"].to_list()
    insider_df["Proportion"] = (insider_df["Amount"].abs() / insider_df["MktCap"]) * 100
    print(insider_df)


def main():
    latest_insider_trading()
    latest_insider_trading_analysis()


if __name__ == '__main__':
    main()
