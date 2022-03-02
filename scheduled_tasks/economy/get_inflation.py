import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database


cnx, engine = connect_mysql_database()
cur = cnx.cursor()


def usa_inflation():
    """
    Get inflation data from https://www.usinflationcalculator.com/inflation/historical-inflation-rates/
    """
    df = pd.read_html("https://www.usinflationcalculator.com/inflation/historical-inflation-rates/")[0]
    print(df)
    df = df[df["Year"] >= 1960][::-1]

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Year"] = df["Year"].astype(str)
    df.replace(np.nan, "N/A", inplace=True)

    most_recent_yr_avg = round(float(df.iloc[[0]].mean(axis=1)), 1)
    df.at[df[df["Year"] == df.iloc[0]["Year"]].index[0], 'Ave'] = most_recent_yr_avg

    df.to_sql("usa_inflation", engine, if_exists="replace", index=False)
    print(df)


def world_inflation():
    url = "https://tradingeconomics.com/country-list/inflation-rate?continent=world"
    df = pd.read_html(url)[0]
    del df["Unit"]
    df.sort_values(by="Last", ascending=False, inplace=True)
    df.to_sql("world_inflation", engine, if_exists="replace", index=False)
    print(df)


if __name__ == '__main__':
    usa_inflation()
    world_inflation()
