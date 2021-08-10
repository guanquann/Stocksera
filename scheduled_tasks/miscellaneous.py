import os
import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from helpers import *
import scheduled_tasks.get_reddit_trending_stocks.fast_yahoo as fast_yahoo

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def get_high_short_interest():
    """
    Returns a high short interest DataFrame.
    Adapted from https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal
    """

    url_high_short_interested_stocks = "https://www.highshortinterest.com"

    text_soup_high_short_interested_stocks = BeautifulSoup(requests.get(url_high_short_interested_stocks,).text, "lxml")

    a_high_short_interest_header = list()
    for high_short_interest_header in text_soup_high_short_interested_stocks.findAll(
        "td", {"class": "tblhdr"}
    ):
        a_high_short_interest_header.append(
            high_short_interest_header.text.strip("\n").split("\n")[0]
        )
    df_high_short_interest = pd.DataFrame(columns=a_high_short_interest_header)

    stock_list_tr = text_soup_high_short_interested_stocks.find_all("tr")

    for a_stock in stock_list_tr:
        a_stock_txt = a_stock.text

        if a_stock_txt == "":
            continue

        shorted_stock_data = a_stock_txt.split("\n")

        if len(shorted_stock_data) == 8:
            df_high_short_interest.loc[
                len(df_high_short_interest.index)
            ] = shorted_stock_data[:-1]

    quick_stats = {'regularMarketPreviousClose': 'PreviousClose',
                   'regularMarketChangePercent': '1DayChange%',
                   'marketCap': 'MktCap'}
    yf_stats_df = fast_yahoo.download_quick_stats(df_high_short_interest["Ticker"].to_list(), quick_stats)
    yf_stats_df.reset_index(inplace=True)
    yf_stats_df.rename(columns={"Symbol": "Ticker"}, inplace=True)

    results_df = pd.merge(df_high_short_interest, yf_stats_df, on="Ticker")
    print(results_df)
    db.execute("DELETE FROM short_interest")
    for index, row in results_df.iterrows():
        db.execute("INSERT INTO short_interest VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (row['Ticker'], row['Company'], row['Exchange'], row['PreviousClose'], round(row['1DayChange%'], 2),
                    row['ShortInt'], row['Float'], row['Outstd'], long_number_format(row['MktCap']), row['Industry']))
        conn.commit()


def get_low_float():
    """
    Returns low float DataFrame
    Adapted from https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal
    """

    url_high_short_interested_stocks = "https://www.lowfloat.com"

    text_soup_low_float_stocks = BeautifulSoup(requests.get(url_high_short_interested_stocks).text, "lxml")

    a_low_float_header = list()
    for low_float_header in text_soup_low_float_stocks.findAll(
        "td", {"class": "tblhdr"}
    ):
        a_low_float_header.append(low_float_header.text.strip("\n").split("\n")[0])
    df_low_float = pd.DataFrame(columns=a_low_float_header)

    stock_list_tr = text_soup_low_float_stocks.find_all("tr")

    for a_stock in stock_list_tr:
        a_stock_txt = a_stock.text

        if a_stock_txt == "":
            continue

        low_float_data = a_stock_txt.split("\n")

        if len(low_float_data) == 8:
            df_low_float.loc[len(df_low_float.index)] = low_float_data[:-1]

    quick_stats = {'regularMarketPreviousClose': 'PreviousClose',
                   'regularMarketChangePercent': '1DayChange%',
                   'marketCap': 'MktCap'}
    yf_stats_df = fast_yahoo.download_quick_stats(df_low_float["Ticker"].to_list(), quick_stats)
    yf_stats_df.reset_index(inplace=True)
    yf_stats_df.rename(columns={"Symbol": "Ticker"}, inplace=True)

    results_df = pd.merge(df_low_float, yf_stats_df, on="Ticker")
    print(results_df)
    db.execute("DELETE FROM low_float")
    for index, row in results_df.iterrows():
        db.execute("INSERT INTO low_float VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (row['Ticker'], row['Company'], row['Exchange'], row['PreviousClose'], round(row['1DayChange%'], 2),
                    row['Float'], row['Outstd'], row['ShortInt'], long_number_format(row['MktCap']), row['Industry']))
        conn.commit()


if __name__ == '__main__':
    get_high_short_interest()
    get_low_float()
