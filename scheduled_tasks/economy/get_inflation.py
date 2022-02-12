import sqlite3
import numpy as np
import pandas as pd

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def inflation():
    """
    Get inflation data from https://www.usinflationcalculator.com/inflation/historical-inflation-rates/
    """
    df = pd.read_html("https://www.usinflationcalculator.com/inflation/historical-inflation-rates/")[0]
    df = df[df["Year"] >= 1980][::-1]

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Year"] = df["Year"].astype(str)
    df.replace(np.nan, "N/A", inplace=True)

    most_recent_yr_avg = round(float(df.iloc[[0]].mean(axis=1)), 1)
    df.at[df[df["Year"] == df.iloc[0]["Year"]].index[0], 'Ave'] = most_recent_yr_avg

    db.execute("DELETE FROM inflation")
    for index, row in df.iterrows():
        db.execute("INSERT INTO inflation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
        conn.commit()
    print(df)


if __name__ == '__main__':
    inflation()
