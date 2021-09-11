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
        df["SETTLEMENT DATE"] = df["SETTLEMENT DATE"].apply(lambda x: str(x[:4] + "/" + x[4:6] + "/" + x[6:]))
        combined_df = combined_df.append(df).drop_duplicates()
    combined_df["SETTLEMENT DATE"] = combined_df["SETTLEMENT DATE"].astype(str)
    combined_df.rename(columns={"SETTLEMENT DATE": "Date",
                                "SYMBOL": "Symbol",
                                "QUANTITY (FAILS)": "Failure to Deliver",
                                "PRICE": "Price"}, inplace=True)
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


def get_top_ftd(filename):
    """
    Get top stocks with high/consistent FTD.
    Criteria: more than 3 days of >500000 FTD in 2 weeks
    """
    df = pd.read_csv(filename)
    df.sort_values(by=["SYMBOL", "SETTLEMENT DATE"], ascending=False, inplace=True)
    df["PRICE"] = df["PRICE"].apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0)

    original_df = df.copy()

    # Criteria
    df = df[df["QUANTITY (FAILS)"] >= 500000]
    df = df[df["PRICE"] >= 5]
    df = df.groupby("SYMBOL").filter(lambda x: len(x) >= 3)

    # We want to extract all ftd quantities from original df
    original_df = original_df[original_df["SYMBOL"].isin(df["SYMBOL"].unique())]

    del original_df["CUSIP"]
    del original_df["DESCRIPTION"]

    original_df["SETTLEMENT DATE"] = original_df["SETTLEMENT DATE"].apply(lambda x: str(x[:4] + "/" + x[4:6] + "/" + x[6:]))
    original_df["SETTLEMENT DATE"] = original_df["SETTLEMENT DATE"].astype(str)
    original_df["FTD x $"] = (original_df["QUANTITY (FAILS)"].astype(int) * original_df["PRICE"].astype(float)).astype(int)

    original_df.rename(columns={"SETTLEMENT DATE": "Date", "SYMBOL": "Symbol",
                                "QUANTITY (FAILS)": "FTD",
                                "PRICE": "Price"}, inplace=True)

    # Sort df based on number of FTD days that meet criteria and add new row between tickers
    combined_df = pd.DataFrame(columns=["Date", "Symbol", "FTD", "Price", "FTD x $"])
    for i in df["SYMBOL"].value_counts().index:
        individual_df = original_df[original_df["Symbol"] == i]
        individual_df = individual_df.append([""])
        combined_df = combined_df.append(individual_df)
    del combined_df[0]
    print(combined_df)
    combined_df.to_csv("database/failure_to_deliver/top_ftd.csv", index=False)


if __name__ == '__main__':
    # convert_to_csv(r"C:\Users\Acer\PycharmProjects\StocksAnalysis\database\failure_to_deliver\cnsfails202108a.txt")
    FOLDER_PATH = r"C:\Users\Acer\PycharmProjects\StocksAnalysis\database\failure_to_deliver\csv"
    # combine_df(folder_path=FOLDER_PATH)
    get_top_ftd(os.path.join(FOLDER_PATH, os.listdir(FOLDER_PATH)[-1]))

