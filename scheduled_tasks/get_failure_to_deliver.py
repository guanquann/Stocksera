import os
import pandas as pd

list_of_tickers = ["GME", "AMC", "BB", "CLOV", "UWMC", "NIO", "TSLA", "AAPL", "SPY", "NOK", "RBLX", "F", "PLTR",
                   "COIN", "RKT", "MVIS", "VIAC", "SNDL", "SPCE", "OCGN", "QQQ", "TQQQ", "SQQQ", "IWM", "VOO",
                   "EXPR", "KOSS", "IPOE", "WKHS", "DIA"]

ftd_file_name = r"failure_to_deliver/cnsfails202105a.txt"
df = pd.read_csv(ftd_file_name, delimiter="|")

if os.path.exists("./failure_to_deliver/csv"):
    df.to_csv("failure_to_deliver/csv/" + ftd_file_name.split("/")[1].replace("txt", "csv"), index=None)
else:
    os.mkdir("./failure_to_deliver/csv")

for ticker in list_of_tickers:
    ticker_df = df[df["SYMBOL"] == ticker]
    folder_path = "./failure_to_deliver/ticker"
    file_path = os.path.join(folder_path, "{}.csv".format(ticker))

    if os.path.isfile(file_path):
        original_df = pd.read_csv(file_path)
        original_df = original_df.append(ticker_df)
        original_df.to_csv(file_path, index=False)
        print(file_path, "updated!")

    else:
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(folder_path, "created!")
        ticker_df.to_csv(file_path, index=False)
        print(file_path, "created!")

os.remove(ftd_file_name)
