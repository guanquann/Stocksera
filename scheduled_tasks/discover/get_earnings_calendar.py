import os
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database
import scheduled_tasks.reddit.stocks.fast_yahoo as fast_yahoo

cnx, engine = connect_mysql_database()
cur = cnx.cursor()


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
            url_ratings = "https://finance.yahoo.com/calendar/earnings?day={}" \
                          "&size=100&offset={}".format(processing_date, num)
            print(url_ratings)
            text_soup_ratings = BeautifulSoup(get_earnings_html(url_ratings), "lxml")

            for stock_rows in text_soup_ratings.findAll("tr"):
                tds = stock_rows.findAll("td")
                if len(tds) > 0:
                    ticker = tds[0].text
                    name = tds[1].text
                    earning_date = processing_date
                    earning_time = tds[2].text.replace("After Market Close", "AMC")\
                        .replace("Before Market Open", "BMO")\
                        .replace("Time Not Supplied", "TNS")
                    eps_est = tds[3].text.replace("-", "N/A") if len(tds[3].text) == 1 else tds[3].text
                    eps_act = tds[4].text.replace("-", "N/A") if len(tds[4].text) == 1 else tds[4].text
                    surprise = tds[5].text.replace("-", "N/A") if len(tds[5].text) == 1 else tds[5].text
                    full_earnings_list.append([ticker, name, eps_est, eps_act, surprise, earning_date, earning_time])
            num += 100
        current_looking_date += 1

    earnings_df = pd.DataFrame(full_earnings_list, columns=["Ticker", "company_name", "eps_est", "eps_act",
                                                            "surprise", "earning_date", "earning_time"])

    mkt_cap_df = fast_yahoo.download_quick_stats(earnings_df["Ticker"].to_list(), {'marketCap': 'mkt_cap'})
    mkt_cap_df.reset_index(inplace=True)
    mkt_cap_df.replace("N/A", 0, inplace=True)
    mkt_cap_df.rename(columns={"Symbol": "Ticker"}, inplace=True)
    results_df = pd.merge(earnings_df, mkt_cap_df, on="Ticker")
    print(results_df)
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
        ticker = stats[0]
        name = stats[1]
        eps_est = stats[2]
        eps_act = stats[3]
        surprise = stats[4]
        earning_date = str(stats[5])
        earning_time = stats[6]
        mkt_cap = stats[7]
        print(ticker, earning_date, earning_time)
        cur.execute("""INSERT INTO earnings_calendar
                      (company_name, ticker, mkt_cap, eps_est, eps_act, surprise, earning_date, earning_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
                      mkt_cap=%s, eps_est=%s, eps_act=%s, surprise=%s, earning_date=%s, earning_time=%s """,
                    (name, ticker, mkt_cap, eps_est, eps_act, surprise, earning_date, earning_time,
                     mkt_cap, eps_est, eps_act, surprise, earning_date, earning_time))
        cnx.commit()


def update_previous_earnings(earnings_df):
    """
    Update the earnings (eps_actual) for the last n days
    Parameters
    ----------
    earnings_df: pd.DataFrame()
        Dataframe of earnings data
    """
    for index, stats in earnings_df.iterrows():
        ticker = stats[0]
        eps_est = stats[2]
        eps_act = stats[3]
        surprise = stats[4]
        print(ticker, eps_est, eps_act, surprise)
        cur.execute("UPDATE earnings_calendar SET eps_est=%s, eps_act=%s, surprise=%s WHERE ticker=%s ",
                    (eps_est, eps_act, surprise, ticker))
        cnx.commit()
    print("Updated previous earnings successfully")


def delete_old_earnings(n_days_ago):
    """
    Remove old earnings till last_date
    Parameters
    ----------
    n_days_ago: int
        Keep earnings from n_days_ago till now
    """
    date_to_remove = str(datetime.utcnow().date() - timedelta(days=n_days_ago))
    cur.execute("DELETE FROM earnings_calendar WHERE earning_date<=%s", (date_to_remove,))
    cnx.commit()


if __name__ == '__main__':
    insert_earnings_into_db(get_earnings(1, forward=True))
    update_previous_earnings(get_earnings(1, forward=False))
    delete_old_earnings(1)
