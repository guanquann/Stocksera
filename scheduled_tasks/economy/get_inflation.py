import os
import sys
import numpy as np
import pandas as pd
import pycountry_convert as pc

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database


cnx, engine = connect_mysql_database()
cur = cnx.cursor()


def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except KeyError:
        return "Unknown"


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

    df.to_sql("usa_inflation", engine, if_exists="replace", index=False)
    print(df)


def world_inflation():
    url = "https://tradingeconomics.com/country-list/inflation-rate?continent=world"
    df = pd.read_html(url)[0]
    del df["Unit"]
    df.sort_values(by="Last", ascending=False, inplace=True)
    df["Continent"] = df["Country"].apply(lambda x: country_to_continent(x))
    df.to_sql("world_inflation", engine, if_exists="replace", index=False)
    print(df)


if __name__ == '__main__':
    usa_inflation()
    world_inflation()
