from datetime import datetime, timedelta
import random
import requests
import sqlite3
import yfinance.ticker as yf
from bs4 import BeautifulSoup

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def get_user_agent() -> str:
    user_agent_strings = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:86.1) Gecko/20100101 Firefox/86.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:86.1) Gecko/20100101 Firefox/86.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:82.1) Gecko/20100101 Firefox/82.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:86.0) Gecko/20100101 Firefox/86.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:86.0) Gecko/20100101 Firefox/86.0",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:84.0) Gecko/20100101 Firefox/84.0",
    ]

    return random.choice(user_agent_strings)


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
        url_ratings, headers={"User-Agent": get_user_agent()}
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
    """
    full_earnings_list = []
    current_looking_date = 0
    while current_looking_date <= n_days:
        if forward:
            processing_date = datetime.now().date() + timedelta(days=current_looking_date)
        else:
            processing_date = datetime.now().date() - timedelta(days=current_looking_date)

        url_ratings = "https://finance.yahoo.com/calendar/earnings?day={}".format(processing_date)
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
        current_looking_date += 1
    return full_earnings_list


def insert_earnings_into_db(earnings_list):
    """
    Insert earnings into database
    Parameters
    ----------
    earnings_list: list
        List of earnings data
    """
    for stats in earnings_list:
        symbol = stats[0]
        name = stats[1]
        eps_est = stats[2]
        eps_act = stats[3]
        surprise = stats[4]
        earning_date = stats[5]
        earning_time = stats[6]

        ticker = yf.Ticker(symbol)
        information = ticker.info
        mkt_cap = information["marketCap"]
        img = information["logo_url"]

        db.execute("""INSERT INTO earnings_calendar
                      (name, symbol, mkt_cap, eps_est, eps_act, surprise, img_url, earning_date, earning_time)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (name, symbol) DO UPDATE SET
                      mkt_cap=?, eps_est=?, eps_act=?, surprise=?, img_url=?, earning_date=?, earning_time=? """,
                   (name, symbol, mkt_cap, eps_est, eps_act, surprise, img, earning_date, earning_time,
                    mkt_cap, eps_est, eps_act, surprise, img, earning_date, earning_time))
        conn.commit()
        print(symbol, earning_date, earning_time)


def update_previous_earnings(earnings_list):
    """
    Update the earnings (eps_actual) for the last n days
    Parameters
    ----------
    earnings_list: list
        List of earnings data
    """
    for stats in earnings_list:
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
    # insert_earnings_into_db(get_earnings(7, forward=True))
    update_previous_earnings(get_earnings(7, forward=False))
    # delete_old_earnings("2021-07-13")
    print("DONE")
