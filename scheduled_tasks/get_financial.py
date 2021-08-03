import json
import requests
import numpy as np
import requests_cache
import yfinance.ticker as yf
from bs4 import BeautifulSoup

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scheduled_tasks.get_popular_tickers import full_ticker_list
from helpers import *

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                'Chrome/91.0.4472.124 Safari/537.36'


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
        url_ratings, headers={"User-Agent": session.headers['User-agent']}
    ).text

    return ratings_html


def financial(ticker_symbol):
    """
    Get balance sheet of company and save it to json file. Data is from yahoo finance
    Parameters
    ----------
    ticker_symbol: str
        ticker symbol (e.g: AAPL)
    """
    ticker = yf.Ticker(ticker_symbol, session=session)
    information = ticker.info

    # To check if input is a valid ticker
    if "symbol" in information:
        # with open(r"database/financials.json", "r+") as r:
        #     data = json.load(r)
            # check_financial_data(ticker_symbol, ticker, data, r)

        url_ratings = "https://finance.yahoo.com/calendar/earnings?symbol={}".format(ticker_symbol)
        text_soup_ratings = BeautifulSoup(get_earnings_html(url_ratings), "lxml")

        earnings_list, financial_quarter_list = [], []
        # [[1, 0.56, 0.64], [2, 0.51, 0.65], [3, 0.7, 0.73], [4, 1.41, 1.68], [5, 0.98]]
        count = 5
        for earning in text_soup_ratings.findAll("tr"):
            tds = earning.findAll("td")
            if len(tds) > 0:
                earning_date = tds[2].text.rsplit(",", 1)[0]
                eps_est = tds[3].text
                eps_act = tds[4].text
                print(earning_date, eps_est, eps_act, ticker_symbol)
                if eps_est != "-" and eps_act != "-":
                    if eps_act != "-":
                        earnings_list.append([count, earning_date, eps_est, eps_act])
                    else:
                        earnings_list.append([count, earning_date, eps_est])
            else:
                break
        # print(earnings_list)

        #     if len(earnings_list) != 100:
        #         tds = earning.findAll("td")
        #         if len(tds) > 0:
        #             earning_date = tds[2].text.rsplit(",", 1)[0]
        #             eps_est = tds[3].text
        #             eps_act = tds[4].text
        #             print(earning_date, eps_est, eps_act, ticker_symbol)
        #
        #             if eps_act != "-":
        #                 earnings_list.append([count, eps_est, eps_act])
        #             else:
        #                 earnings_list.append([count, eps_est])
        #
        #             # Deduce financial quarter based on date of report
        #             year_num = earning_date.split()[-1]
        #             month_num = earning_date.split()[0]
        #             if month_num in ["Jan", "Feb", "Mar"]:
        #                 year_num = int(year_num) - 1
        #                 quarter = "Q4"
        #             elif month_num in ["Apr", "May", "Jun"]:
        #                 quarter = "Q1"
        #             elif month_num in ["Jul", "Aug", "Sep"]:
        #                 quarter = "Q2"
        #             else:
        #                 quarter = "Q3"
        #             financial_quarter_list.append("{} {}".format(year_num, quarter))
        #             count -= 1
        #     else:
        #         break


if __name__ == '__main__':
    for i in full_ticker_list():
        financial(i)
