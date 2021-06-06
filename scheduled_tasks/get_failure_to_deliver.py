import os
import pandas as pd

import scheduled_tasks.get_short_volume as get_short_volume


def update_all_tickers(ftd_txt_file_name):
    df = pd.read_csv(ftd_txt_file_name, delimiter="|")

    if os.path.exists("./failure_to_deliver/csv"):
        df.to_csv("failure_to_deliver/csv/" + ftd_txt_file_name.split("/")[1].replace("txt", "csv"), index=None)
    else:
        os.mkdir("./failure_to_deliver/csv")

    for ticker in get_short_volume.full_ticker_list():
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
    os.remove(ftd_txt_file_name)


def add_new_ticker(ticker):
    ticker = ticker.upper()
    folder_path = "./failure_to_deliver/ticker"
    file_path = os.path.join(folder_path, "{}.csv".format(ticker))

    if os.path.exists(file_path):
        os.remove(file_path)

    all_csv_path = "./failure_to_deliver/csv"
    for csv in os.listdir(all_csv_path):
        df = pd.read_csv(os.path.join(all_csv_path, csv))

        ticker_df = df[df["SYMBOL"] == ticker]
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


if __name__ == '__main__':
    add_new_ticker("CLNE")
