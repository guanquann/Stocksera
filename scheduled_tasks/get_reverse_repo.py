from datetime import datetime
import sqlite3
import pandas as pd

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def reverse_repo(start_date="01022014", end_date=None):
    """
    Get reverse repo by downloading csv file online and dump into database
    Parameters
    ----------
    start_date : str
        format: DDMMYYYY
    end_date : str
        format: DDMMYYYY
    """

    if end_date is None:
        current_date = str(datetime.now().date()).replace("-", "")
        end_date = current_date[4:6] + current_date[-2:] + current_date[:4]

    url = "https://websvcgatewayx2.frbny.org/autorates_tomo_external/services/v1_0/tomo/retrieveHistoricalExcel?f=" \
          "{}&t={}&ctt=true&&cta=true&ctm=true".format(start_date, end_date)
    print(url)
    df = pd.read_excel(url)
    df = df[df["Op Type"] == "RRP"]
    df["Deal Date"] = df["Deal Date"].str.replace("/", "-")
    # df.fillna(0, inplace=True)
    df["Total-Submit"] = df["Total-Submit"].astype(str).str.replace(",", "").astype(float)
    df["Average"] = df["Total-Submit"] / df["Participating Counterparties"].astype(float)
    df["Average"] = df["Average"].round(2)
    df.fillna(0, inplace=True)
    for index, row in df[::-1].iterrows():
        date = row["Deal Date"]
        amount = row["Total-Submit"]
        participants = row["Participating Counterparties"]
        avg = row["Average"]
        db.execute("INSERT OR IGNORE INTO reverse_repo VALUES (?, ?, ?, ?)", (date, amount, participants, avg))
        conn.commit()


if __name__ == '__main__':
    reverse_repo()
