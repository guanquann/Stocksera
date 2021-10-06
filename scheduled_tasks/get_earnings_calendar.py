import os
import sys
from datetime import datetime, timedelta
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import scheduled_tasks.reddit.get_reddit_trending_stocks.fast_yahoo as fast_yahoo

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def get_earnings_html(url_ratings: str) -> str:
    """
    Parameters
    ----------
    url_ratings : str
        Ratings URL

    Returns
    -------
    str
        HTML page of earnings
    """
    ratings_html = requests.get(
        url_ratings, headers={"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:86.1) "
                                            "Gecko/20100101 Firefox/86.1"}
    ).text

    return ratings_html


def get_earnings(n_days=7, forward=True):
    """
    Get the earnings for the next/previous n days
    Parameters
    ----------
    n_days: int
        Number of days from today
    forward: bool
        True-> get earnings for next n days
        False-> get earnings for previous n days
    Returns
    -------
    pd.DataFrame()
        dataframe of earnings
    """
    full_earnings_list = []
    current_looking_date = 0
    while current_looking_date <= n_days:
        if forward:
            processing_date = datetime.now().date() + timedelta(days=current_looking_date)
        else:
            processing_date = datetime.now().date() - timedelta(days=current_looking_date)

        num = 0
        for i in range(5):
            url_ratings = "https://finance.yahoo.com/calendar/earnings?day={}&size=100&offset={}".format(processing_date, num)
            print(url_ratings)
            text_soup_ratings = BeautifulSoup(get_earnings_html(url_ratings), "lxml")

            for stock_rows in text_soup_ratings.findAll("tr"):
                tds = stock_rows.findAll("td")
                if len(tds) > 0:
                    symbol = tds[0].text
                    name = tds[1].text
                    earning_date = processing_date
                    earning_time = tds[2].text.replace("After Market Close", "AMC").replace("Before Market Open", "BMO")\
                        .replace("Time Not Supplied", "TNS")
                    eps_est = tds[3].text.replace("-", "N/A") if len(tds[3].text) == 1 else tds[3].text
                    eps_act = tds[4].text.replace("-", "N/A") if len(tds[4].text) == 1 else tds[4].text
                    surprise = tds[5].text.replace("-", "N/A") if len(tds[5].text) == 1 else tds[5].text
                    full_earnings_list.append([symbol, name, eps_est, eps_act, surprise, earning_date, earning_time])
            num += 100
        current_looking_date += 1

    earnings_df = pd.DataFrame(full_earnings_list, columns=["Symbol", "name", "eps_est", "eps_act",
                                                            "surprise", "earning_date", "earning_time"])
    mkt_cap_df = fast_yahoo.download_quick_stats(earnings_df["Symbol"].to_list(), {'marketCap': 'mkt_cap'})
    mkt_cap_df.reset_index(inplace=True)
    results_df = pd.merge(earnings_df, mkt_cap_df, on="Symbol")
    return results_df


def insert_earnings_into_db(earnings_df):
    """
    Insert earnings into database
    Parameters
    ----------
    earnings_df: pd.DataFrame()
        Dataframe of earnings data
    """
    for index, stats in earnings_df.iterrows():
        symbol = stats[0]
        name = stats[1]
        eps_est = stats[2]
        eps_act = stats[3]
        surprise = stats[4]
        earning_date = stats[5]
        earning_time = stats[6]
        mkt_cap = stats[7]

        db.execute("""INSERT INTO earnings_calendar
                      (name, symbol, mkt_cap, eps_est, eps_act, surprise, earning_date, earning_time)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (name, symbol) DO UPDATE SET
                      mkt_cap=?, eps_est=?, eps_act=?, surprise=?, earning_date=?, earning_time=? """,
                   (name, symbol, mkt_cap, eps_est, eps_act, surprise, earning_date, earning_time,
                    mkt_cap, eps_est, eps_act, surprise, earning_date, earning_time))
        conn.commit()
        print(symbol, earning_date, earning_time)


def update_previous_earnings(earnings_df):
    """
    Update the earnings (eps_actual) for the last n days
    Parameters
    ----------
    earnings_df: pd.DataFrame()
        Dataframe of earnings data
    """
    for index, stats in earnings_df.iterrows():
        symbol = stats[0]
        eps_est = stats[2]
        eps_act = stats[3]
        surprise = stats[4]
        print(symbol, eps_est, eps_act, surprise)
        db.execute("UPDATE earnings_calendar SET eps_est=?, eps_act=?, surprise=? WHERE symbol=? ",
                   (eps_est, eps_act, surprise, symbol))
        conn.commit()
    print("Updated previous earnings successfully")


def delete_old_earnings(last_date):
    """
    Remove old earnings till last_date
    Parameters
    ----------
    last_date: str
        Date format: YYYY-MM-DD
    """
    db.execute("SELECT DISTINCT earning_date FROM earnings_calendar")
    all_dates = db.fetchall()
    for date in sorted(all_dates):
        if date[0] == last_date:
            print("All earnings date till {} removed from database.".format(last_date))
            break
        db.execute("DELETE FROM earnings_calendar WHERE earning_date=?", (date[0],))
        conn.commit()


if __name__ == '__main__':
    insert_earnings_into_db(get_earnings(1, forward=True))
    # update_previous_earnings(get_earnings(7, forward=False))
    # delete_old_earnings("2021-07-13")
