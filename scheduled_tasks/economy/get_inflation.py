import os
import sys
import requests
import numpy as np
import pandas as pd
import pycountry_convert as pc

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import connect_mysql_database


cnx, cur, engine = connect_mysql_database()


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

    count = 0
    most_recent_yr_avg = 0
    for _, value in df.iloc[0, 1:].items():
        if value != "N/A":
            count += 1
            most_recent_yr_avg += float(value)
    most_recent_yr_avg = round(most_recent_yr_avg / count, 1)

    df.at[df[df["Year"] == df.iloc[0]["Year"]].index[0], 'Ave'] = most_recent_yr_avg

    df.to_sql("usa_inflation", engine, if_exists="replace", index=False)


def world_inflation():
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    df = pd.read_html(requests.get("https://tradingeconomics.com/country-list/inflation-rate?continent=world",
                                   headers=header).text)[0]
    del df["Unit"]
    df.sort_values(by="Last", ascending=False, inplace=True)
    df["Continent"] = df["Country"].apply(lambda x: country_to_continent(x))
    df.to_sql("world_inflation", engine, if_exists="replace", index=False)


def main():
    print("Getting Inflation...")
    usa_inflation()
    world_inflation()
    print("Inflation Successfully Completed...\n")


if __name__ == '__main__':
    main()
