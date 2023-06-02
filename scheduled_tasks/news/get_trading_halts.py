import os
import sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def main(method=""):
    print("Getting Trading Halt...")
    if method != "historical":
        url = "https://www.nyse.com/api/trade-halts/current/download"
    else:
        url = "https://www.nyse.com/api/trade-halts/historical/download?haltDateFrom=2021-03-04"
    df = pd.read_csv(url)
    df.fillna("N/A", inplace=True)
    df["Halt Date"] = df["Halt Date"].astype(str)
    df["Halt Date"] = df["Halt Date"].apply(lambda x: str(x[6:] + "-" + x[:2] + "-" + x[3:5] if x != "N/A" else "N/A"))
    df["Resume Date"] = df["Resume Date"].astype(str)
    df["Resume Date"] = df["Resume Date"].apply(lambda x: str(x[6:] + "-" + x[:2] + "-" + x[3:5] if x != "N/A"
                                                              else "N/A"))
    del df["Name"]
    cur.executemany("INSERT IGNORE INTO trading_halts VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE "
                    "`Resume Date`=VALUES(`Resume Date`), `Resume Time`=VALUES(`Resume Time`)",
                    df.values.tolist())
    cnx.commit()
    print("Trading Halt Successfully Completed...\n")


if __name__ == '__main__':
    main()
