import os
import pandas as pd


def convert_to_csv(ftd_txt_file_name):
    """
    If new FTD data is available from SEC, run this function.
    Parameters
    ----------
    ftd_txt_file_name: str
        file name in .txt format (e.g: cnsfails202006a.txt)
    Returns
    -------
    ftd_txt_file_name will be converted to .csv
    """
    df = pd.read_csv(ftd_txt_file_name, delimiter="|")

    if os.path.exists("database/failure_to_deliver/csv"):
        df.to_csv("database/failure_to_deliver/csv/" + ftd_txt_file_name.split("\\")[-1].replace("txt", "csv"),
                  index=None)
    else:
        os.mkdir("database/failure_to_deliver/csv")
    os.remove(ftd_txt_file_name)


def combine_df(folder_path):
    combined_df = pd.DataFrame(columns=["SETTLEMENT DATE", "SYMBOL", "QUANTITY (FAILS)", "PRICE"])
    for file in os.listdir(folder_path):
        print("Processing: ", file)
        df = pd.read_csv(os.path.join(folder_path, file))
        del df["CUSIP"]
        del df["DESCRIPTION"]
        combined_df = combined_df.append(df).drop_duplicates()
    combined_df.to_csv("database/failure_to_deliver/ftd.csv", index=False)


def get_all_tickers_csv(folder_path):
    """
    Save all ticker name and symbol into database/all_tickers.csv
    """
    df = pd.read_csv(folder_path)
    df.dropna(inplace=True)

    new_df = pd.DataFrame()
    new_df["SYMBOL"] = df["SYMBOL"]
    new_df["DESCRIPTION"] = df["DESCRIPTION"]
    new_df.drop_duplicates(inplace=True)
    new_df.sort_values(by=["SYMBOL"], inplace=True)
    new_df.to_csv("database/all_tickers.csv", index=False)


if __name__ == '__main__':
    FOLDER_PATH = r"C:\Users\Acer\PycharmProjects\StocksAnalysis\database\failure_to_deliver\csv"
    combine_df(folder_path=FOLDER_PATH)
