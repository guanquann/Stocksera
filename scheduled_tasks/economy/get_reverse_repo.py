from datetime import datetime
import sqlite3
import pandas as pd

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def reverse_repo(start_date="2014-01-01", end_date=None):
    """
    Get reverse repo by downloading csv file online and dump into database
    Parameters
    ----------
    start_date : str
        format: YYYY-MM-DD
    end_date : str
        format: YYYY-MM-DD
    """

    if end_date is None:
        end_date = str(datetime.utcnow().date())

    url = "https://markets.newyorkfed.org/read?startDt={}&endDt={}&productCode=70&eventCodes=730&format=csv".format(start_date, end_date)

    df = pd.read_csv(url)
    df = df[df["Operation Type"] == "Reverse Repo"]

    df["Total Amt Submitted ($Billions)"] = df["Total Amt Submitted ($Billions)"].astype(float)
    df["Average"] = df["Total Amt Submitted ($Billions)"] / df["Participating Counterparties"].astype(float)
    df["Average"] = df["Average"].round(2)
    df.fillna(0, inplace=True)
    for index, row in df[::-1].iterrows():
        date = row["Operation Date"]
        date = date[-4:] + "-" + date[:2] + "-" + date[3:5]
        amount = row["Total Amt Submitted ($Billions)"]
        participants = row["Participating Counterparties"]
        avg = row["Average"]
        print(date, amount, participants, avg)
        db.execute("INSERT OR IGNORE INTO reverse_repo VALUES (?, ?, ?, ?)", (date, amount, participants, avg))
        conn.commit()


if __name__ == '__main__':
    reverse_repo()
