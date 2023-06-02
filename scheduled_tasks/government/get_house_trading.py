import os
import pandas as pd

OUT_PATH = r"database/government"
if not os.path.exists(OUT_PATH):
    os.mkdir(OUT_PATH)


def house_trades():
    """
    Get house trades of US Government
    """
    df = pd.read_json("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json")
    for i in ["transaction_date", "disclosure_date"]:
        df[i] = pd.to_datetime(df[i], errors='coerce')
        df[i] = df[i].dt.strftime('%Y-%m-%d')
    del df["state"]
    del df["industry"]
    del df["sector"]
    del df["party"]
    df.columns = ["Disclosure Year", "Disclosure Date", "Transaction Date", "Owner", "Ticker", "Asset Description",
                  "Type", "Amount", "Representative", "District", "Link", "Cap Gains Over 200USD"]

    df.fillna("Unknown", inplace=True)
    df.replace("--", "Unknown", inplace=True)
    df.replace("N/A", "Unknown", inplace=True)
    df["Owner"] = df["Owner"].str.title()
    del df["Disclosure Year"]
    df.sort_values(by="Disclosure Date", inplace=True, ascending=False)

    df["Asset Type"] = ""

    df["Type"] = df["Type"].str.title()
    df["Type"].replace("Sale_Full", "Sale (Full)", inplace=True)
    df["Type"].replace("Sale_Partial", "Sale (Partial)", inplace=True)

    df = df[["Transaction Date", "Owner", "Ticker", "Asset Description", "Asset Type", "Type", "Amount",
             "Representative", "Link", "Disclosure Date", "District", "Cap Gains Over 200USD"]]

    df["Representative"] = df["Representative"].str.replace("^Hon. |^Mr. |^Mrs. |^None ", "")
    print(df)
    df.to_csv(os.path.join(OUT_PATH, "house.csv"), index=False)


if __name__ == '__main__':
    house_trades()
