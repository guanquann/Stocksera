import os
import sys
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from finvizfinance.insider import Insider

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from scheduled_tasks.reddit.stocks.fast_yahoo import download_quick_stats

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def latest_insider_trading():
    for type_trading in ["buys", "sales"]:
        print("latest {}".format(type_trading))
        finsider = Insider(option="latest {}".format(type_trading))
        insider_trader = finsider.getInsider()

        insider_trader["Owner"] = insider_trader["Owner"].str.title()
        insider_trader = insider_trader[insider_trader["Value ($)"] >= 50000]

        insider_trader["Date"] = insider_trader["Date"] + " 2022"
        insider_trader["Date"] = pd.to_datetime(insider_trader["Date"], format="%b %d %Y", errors='coerce')
        insider_trader["Date"] = insider_trader["Date"].astype(str)

        insider_trader["SEC Form 4"] = insider_trader["SEC Form 4"].apply(lambda x: x.rsplit(' ', 2)[0])
        insider_trader["SEC Form 4"] = insider_trader["SEC Form 4"] + " 2022"
        insider_trader["SEC Form 4"] = pd.to_datetime(insider_trader["SEC Form 4"], format="%b %d %Y", errors='coerce')
        insider_trader["SEC Form 4"] = insider_trader["SEC Form 4"].astype(str)

        if type_trading == "sales":
            insider_trader["Value ($)"] = -insider_trader["Value ($)"]

        print(insider_trader)
        for index, row in insider_trader.iterrows():
            db.execute("INSERT OR IGNORE INTO latest_insider_trading VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,?, ?)",
                       tuple(row))
            conn.commit()


def latest_insider_trading_analysis():
    last_date = str(datetime.utcnow().date() - timedelta(days=30))

    insider_df = pd.read_sql_query("SELECT * FROM latest_insider_trading", conn)
    insider_df = insider_df.drop_duplicates(subset=["Ticker", "TransactionDate", "Cost", "Shares", "Value",
                                                    "DateFilled"], keep='first')
    insider_df = insider_df[insider_df["DateFilled"] > last_date]
    insider_df = pd.DataFrame(insider_df.groupby(["Ticker"])['Value'].agg('sum'))

    insider_df = insider_df.reindex(insider_df["Value"].abs().sort_values(ascending=False).index).head(50)
    insider_df.reset_index(inplace=True)
    insider_df.rename(columns={"Ticker": "Symbol", "Value": "Amount"}, inplace=True)

    # insider_df = pd.read_sql_query("SELECT Ticker AS Symbol, SUM(Value) AS Amount "
    #                                "FROM latest_insider_trading WHERE "
    #                                "DateFilled>='{}' GROUP BY Ticker ORDER BY "
    #                                "ABS(SUM(Value)) DESC LIMIT 50".format(last_date), conn)
    quick_stats = {'marketCap': 'MktCap'}
    quick_stats_df = download_quick_stats(insider_df["Symbol"].to_list(), quick_stats, threads=True).reset_index()
    quick_stats_df = quick_stats_df[quick_stats_df["MktCap"] != "N/A"]
    insider_df = insider_df.merge(quick_stats_df, on="Symbol")
    insider_df["Proportion"] = (insider_df["Amount"].abs() / insider_df["MktCap"]) * 100
    insider_df["Proportion"] = insider_df["Proportion"].astype(float).round(3)
    insider_df.to_sql("latest_insider_trading_analysis", conn, if_exists="replace", index=False)


def main():
    latest_insider_trading()
    latest_insider_trading_analysis()


if __name__ == '__main__':
    main()
