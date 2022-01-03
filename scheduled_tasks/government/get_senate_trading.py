import os
import pandas as pd
from datetime import datetime, timedelta

OUT_PATH = r"database/government"
if not os.path.exists(OUT_PATH):
    os.mkdir(OUT_PATH)


def senate_trades():
    df = pd.read_json("https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json")

    for i in ["transaction_date", "disclosure_date"]:
        df[i] = pd.to_datetime(df[i], errors='coerce')
        df[i] = df[i].dt.strftime('%Y-%m-%d')

    df = df[df["disclosure_date"] >= str(datetime.utcnow().date() - timedelta(days=365*5))]

    df.columns = ["Transaction Date", "Owner", "Ticker", "Asset Description", "Asset Type", "Type", "Amount", "Comment",
                  "Senator", "Link", "Disclosure Date"]

    del df["Comment"]
    df.replace("--", "Unknown", inplace=True)
    df.replace("N/A", "Unknown", inplace=True)
    print(df)
    df.to_csv(os.path.join(OUT_PATH, "senate.csv"), index=False)


if __name__ == '__main__':
    senate_trades()
