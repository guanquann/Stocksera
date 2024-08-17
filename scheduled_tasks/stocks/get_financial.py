import requests_cache
import yfinance.ticker as yf

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from scheduled_tasks.others.get_popular_tickers import full_ticker_list
from helpers import *

session = requests_cache.CachedSession("yfinance.cache")
session.headers["User-agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)


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
        with open(r"database/financials.json", "r+") as r:
            data = json.load(r)
            check_financial_data(ticker_symbol, ticker, data, r)


if __name__ == "__main__":
    for i in full_ticker_list():
        financial(i)
