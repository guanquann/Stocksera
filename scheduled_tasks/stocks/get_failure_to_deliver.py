import os
import sys
import shutil
import requests
import pandas as pd
from datetime import timedelta
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def download_ftd():
    """
    If new FTD data is available from SEC, run this function.
    Returns
    -------
    ftd_data will be downloaded and converted to .csv
    """

    shutil.rmtree("database/failure_to_deliver/csv")
    os.mkdir("database/failure_to_deliver/csv")

    base_url = "https://www.sec.gov"
    text_soup_high_short_interested_stocks = BeautifulSoup(
        requests.get("https://www.sec.gov/data/foiadocsfailsdatahtm").text, "lxml")

    ftd_url_links = text_soup_high_short_interested_stocks.findAll("table")[1].findAll("a")
    for url_link in ftd_url_links[:24]:
        print(base_url + url_link["href"])
        df = pd.read_csv(base_url + url_link["href"], delimiter="|", error_bad_lines=False, encoding="cp1252")
        df.to_csv("database/failure_to_deliver/csv/" + url_link["href"].split("/")[-1].replace(".zip", ".csv"),
                  index=None)


def upload_to_df(files_available, limit=24):
    """
    Combine all the 1/2 monthly csv into 1 large csv file
    """
    combined_df = pd.DataFrame(columns=["SETTLEMENT DATE", "SYMBOL", "QUANTITY (FAILS)", "PRICE"])
    for file in files_available[:limit]:
        print("Processing: ", file)
        df = pd.read_csv(file)
        del df["CUSIP"]
        del df["DESCRIPTION"]
        df["SETTLEMENT DATE"] = df["SETTLEMENT DATE"].apply(lambda x: str(x[:4] + "-" + x[4:6] + "-" + x[6:]))
        combined_df = combined_df.append(df).drop_duplicates()

    combined_df["SETTLEMENT DATE"] = combined_df["SETTLEMENT DATE"].astype(str)
    combined_df.rename(columns={"SETTLEMENT DATE": "Date",
                                "SYMBOL": "Ticker",
                                "QUANTITY (FAILS)": "Failure to Deliver",
                                "PRICE": "Price"}, inplace=True)
    combined_df["T+35 Date"] = pd.to_datetime(combined_df['Date'], format='%Y-%m-%d', errors="coerce") + timedelta(days=35)
    combined_df["T+35 Date"] = combined_df["T+35 Date"].astype(str)
    combined_df = combined_df[~combined_df["Ticker"].isna()]
    combined_df.sort_values(by="Date", inplace=True)
    print(combined_df)

    start = 0
    while start < len(combined_df):
        print(start)
        cur.executemany("INSERT IGNORE INTO ftd VALUES (%s, %s, %s, %s, %s)", combined_df[start:start+50000].values.tolist())
        cnx.commit()
        start += 50000


def get_top_ftd(filename):
    """
    Get top stocks with high/consistent FTD.
    Criteria: more than 3 days of >500000 FTD in 2 weeks
    """
    print("Getting top FTD for: ", filename)
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

    original_df["SETTLEMENT DATE"] = original_df["SETTLEMENT DATE"].apply(lambda x: str(x[:4] + "-" + x[4:6] + "-" + x[6:]))
    original_df["SETTLEMENT DATE"] = original_df["SETTLEMENT DATE"].astype(str)
    original_df["FTD x $"] = (original_df["QUANTITY (FAILS)"].astype(int) * original_df["PRICE"].astype(float)).astype(int)
    original_df.rename(columns={"SETTLEMENT DATE": "Date",
                                "SYMBOL": "Ticker",
                                "QUANTITY (FAILS)": "FTD",
                                "PRICE": "Price"}, inplace=True)
    original_df["T+35 Date"] = pd.to_datetime(original_df['Date'], format='%Y-%m-%d', errors="coerce") + timedelta(
        days=35)
    original_df["T+35 Date"] = original_df["T+35 Date"].astype(str)  # .apply(lambda x: x.replace("-", "/"))

    # Sort df based on number of FTD days that meet criteria and add new row between tickers
    combined_df = pd.DataFrame(columns=["Date", "Ticker", "FTD", "Price", "FTD x $"])
    for i in df["SYMBOL"].value_counts().index:
        individual_df = original_df[original_df["Ticker"] == i]
        individual_df = individual_df.append([""])
        combined_df = combined_df.append(individual_df)
    del combined_df[0]
    combined_df.to_sql('top_ftd', engine, if_exists="replace", method="multi", index=False)


def main():
    download_ftd()
    FOLDER_PATH = r"database/failure_to_deliver/csv"
    files_available = sorted(Path(FOLDER_PATH).iterdir(), key=os.path.getmtime)
    upload_to_df(files_available, limit=1)
    get_top_ftd(files_available[0])


if __name__ == '__main__':
    main()
