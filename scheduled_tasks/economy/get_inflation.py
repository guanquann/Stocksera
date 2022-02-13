import sqlite3
import numpy as np
import pandas as pd

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def usa_inflation():
    """
    Get inflation data from https://www.usinflationcalculator.com/inflation/historical-inflation-rates/
    """
    df = pd.read_html("https://www.usinflationcalculator.com/inflation/historical-inflation-rates/")[0]
    df = df[df["Year"] >= 1960][::-1]

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Year"] = df["Year"].astype(str)
    df.replace(np.nan, "N/A", inplace=True)

    most_recent_yr_avg = round(float(df.iloc[[0]].mean(axis=1)), 1)
    df.at[df[df["Year"] == df.iloc[0]["Year"]].index[0], 'Ave'] = most_recent_yr_avg

    df.to_sql("usa_inflation", conn, if_exists="replace", index=False)
    print(df)


def world_inflation():
    url = "https://tradingeconomics.com/country-list/inflation-rate?continent=world"
    df = pd.read_html(url)[0]
    del df["Unit"]
    df.sort_values(by="Last", ascending=False, inplace=True)
    df.to_sql("world_inflation", conn, if_exists="replace", index=False)
    print(df)


if __name__ == '__main__':
    usa_inflation()
    world_inflation()
