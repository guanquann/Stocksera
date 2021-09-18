import sqlite3
import pandas as pd
from finvizfinance.insider import Insider

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
        for index, row in insider_trader.iterrows():
            db.execute("INSERT OR IGNORE INTO latest_insider_trading VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,?)",
                       tuple(row))
            conn.commit()


if __name__ == '__main__':
    latest_insider_trading()
