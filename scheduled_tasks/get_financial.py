import json
import numpy as np
import requests_cache
import yfinance.ticker as yf
from yahoo_earnings_calendar import YahooEarningsCalendar

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scheduled_tasks.get_popular_tickers import full_ticker_list

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


def financial(ticker_symbol):
    """
    Get balance sheet of company and save it to json file. Data is from yahoo finance
    Parameters
    ----------
    ticker_symbol: str
        ticker symbol (e.g: AAPL)
    """
    balance_list = []
    ticker = yf.Ticker(ticker_symbol, session=session)
    information = ticker.info

    # To check if input is a valid ticker
    if "symbol" in information:
        balance_sheet = ticker.quarterly_balance_sheet.replace(np.nan, 0)
        print(balance_sheet)

        date_list = balance_sheet.columns.astype("str").to_list()
        balance_col_list = balance_sheet.index.tolist()
        print(date_list)
        print(balance_col_list)
        for i in range(len(balance_sheet)):
            values = balance_sheet.iloc[i].tolist()
            balance_list.append(values)

        # Get Actual vs Est EPS of ticker
        yec = YahooEarningsCalendar(0)
        earnings = yec.get_earnings_of(ticker_symbol)
        earnings_list, financial_quarter_list = [], []
        # [[1, 0.56, 0.64], [2, 0.51, 0.65], [3, 0.7, 0.73], [4, 1.41, 1.68], [5, 0.98]]
        count = 5
        for earning in earnings:
            if len(earnings_list) != 5:
                if earning["epsestimate"] is not None:
                    if earning["epsactual"] is not None:
                        earnings_list.append([count, earning["epsestimate"], earning["epsactual"]])
                    else:
                        earnings_list.append([count, earning["epsestimate"]])

                    # Deduce financial quarter based on date of report
                    year_num = earning["startdatetime"].split("T")[0].split("-")[0]
                    month_num = int(earning["startdatetime"].split("T")[0].split("-")[1])
                    if month_num in [1, 2, 3]:
                        year_num = int(year_num) - 1
                        quarter = "Q4"
                    elif month_num in [4, 5, 6]:
                        quarter = "Q1"
                    elif month_num in [7, 8, 9]:
                        quarter = "Q2"
                    else:
                        quarter = "Q3"
                    financial_quarter_list.append("{} {}".format(year_num, quarter))
                count -= 1
            else:
                break

        with open(r"database/financials.json", "r+") as r:
            data = json.load(r)
            data[ticker_symbol] = {
                "date_list": date_list,
                "balance_list": balance_list,
                "balance_col_list": balance_col_list,
                "earnings_list": earnings_list,
                "financial_quarter_list": financial_quarter_list,
            }
            r.seek(0)  # reset file position to the beginning.
            json.dump(data, r, indent=4)
            print("Financial Data for {} completed".format(ticker_symbol))


if __name__ == '__main__':
    for i in full_ticker_list():
        financial(i)
