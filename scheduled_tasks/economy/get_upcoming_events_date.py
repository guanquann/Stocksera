import json
import sqlite3
import tabula
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

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


def get_next_cpi_date():
    """
    Get next CPI release date
    """
    df = pd.read_html(r"https://www.bls.gov/schedule/news_release/cpi.htm")[0][:-1]
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
    holidays_df["Date"] = pd.to_datetime(holidays_df["Date"])
    print(holidays_df)
    return holidays_df


def main():
    db.execute("SELECT record_date from reverse_repo ORDER BY record_date DESC LIMIT 1")
    record_date = db.fetchone()
    rrp_treasury_date = get_next_rrp_treasury_date(datetime.strptime(record_date[0], "%Y-%m-%d") + timedelta(days=1))
    retail_df = get_next_retail_sales_date()
    cpi_df = get_next_cpi_date()

    with open(r"database/economic_date.json", "w") as r:
        information = {
            "Retail Sales": {"Ref Month": retail_df["Data Month"], "Release Date": retail_df["Release Date"]},
            "Inflation": {"Ref Month": cpi_df["Reference Month"], "Release Date": cpi_df["Release Date"]},
            "Daily Treasury": {"Release Date": rrp_treasury_date},
            "Reverse Repo": {"Release Date": rrp_treasury_date},
        }
        json.dump(information, r, indent=4)


if __name__ == '__main__':
    main()
