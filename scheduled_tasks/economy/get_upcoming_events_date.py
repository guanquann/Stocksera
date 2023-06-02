import os
import sys
import json
import tabula
import requests
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scheduled_tasks.economy.ychart_connection import ychart_data
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()

current_date = datetime.utcnow()


def get_next_retail_sales_date():
    """
    Get next retail sales release date
    """
    df = tabula.read_pdf(r"https://www.census.gov/retail/marts/www/martsdates.pdf", pages=1)[0]
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors='coerce')
    df = df[df["Release Date"] >= current_date].iloc[0]
    df['Release Date'] = df['Release Date'].strftime('%Y-%m-%d')
    return df


def get_next_initial_jobless_date():
    """
    Get next initial jobless claim date
    """
    url = "https://ycharts.com/indicators/us_initial_claims_for_unemployment_insurance"
    release_date = ychart_data(url)[3].iloc[3][1].split(",")[0]
    release_date = str(datetime.strptime(release_date, "%b %d %Y")).split()[0]
    return release_date


def get_next_cpi_date():
    """
    Get next CPI release date
    """
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    df = pd.read_html(requests.get(r"https://www.bls.gov/schedule/news_release/cpi.htm", headers=header).text)[0][:-1]
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors='coerce')
    df = df[df["Release Date"] >= current_date].iloc[0]
    df['Release Date'] = df['Release Date'].strftime('%Y-%m-%d')
    return df


def to_week_day(date):
    """
    Get the next closest weekday
    Parameters
    ----------
    date : datetime
        Date to find the next closest weekday
    """
    if date.weekday() in {5, 6}:
        date += timedelta(days=-date.weekday() + 7)
    return str(date.date())


def get_next_rrp_treasury_date(date):
    return to_week_day(date)


def get_holidays():
    """
    Get holidays in US when stock market is closed
    """
    holidays_df = pd.read_html(r"https://www.sec.gov/edgar/filer-information/calendar")[0]
    holidays_df["Date"] = pd.to_datetime(holidays_df["Date"], errors='coerce')
    return holidays_df


def main():
    print("Getting Upcoming Economic Release Date...")
    get_next_initial_jobless_date()
    cur.execute("SELECT record_date from reverse_repo ORDER BY record_date DESC LIMIT 1")
    record_date = cur.fetchone()
    rrp_treasury_date = get_next_rrp_treasury_date(datetime.strptime(record_date[0], "%Y-%m-%d") + timedelta(days=1))
    retail_df = get_next_retail_sales_date()
    cpi_df = get_next_cpi_date()
    ijp_date = get_next_initial_jobless_date()

    with open(r"database/economic_date.json", "w") as r:
        information = {
            "Retail Sales": {"Ref Month": retail_df["Data Month"], "Release Date": retail_df["Release Date"]},
            "Inflation": {"Ref Month": cpi_df["Reference Month"], "Release Date": cpi_df["Release Date"]},
            "Initial Jobless Claims": {"Release Date": ijp_date},
            "Daily Treasury": {"Release Date": rrp_treasury_date},
            "Reverse Repo": {"Release Date": rrp_treasury_date},
        }
        json.dump(information, r, indent=4)
    print("Upcoming Economic Release Date Successfully Completed...\n")


if __name__ == '__main__':
    main()
