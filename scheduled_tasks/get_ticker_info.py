import os
import sys
import json
import yfinance.ticker as yf
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scheduled_tasks.get_popular_tickers import full_ticker_list

# import os
# print(os.path.basename(os.getcwd()))

# Time Format: HHMMSS
market_open_time = "133000"
market_close_time = "200000"


def ticker_info(ticker_selected):
    """
    Cache ticker information into a json file to speed up rendering time
    Parameters
    ----------
    ticker_selected: str
        ticker symbol (e.g: AAPL)
    """
    ticker = yf.Ticker(ticker_selected)
    current_datetime = datetime.utcnow()
    next_update_time = str(current_datetime + timedelta(seconds=600))
    with open(r"database/yf_cached_api.json", "r+") as r:
        data = json.load(r)
        information = ticker.info
        data[ticker_selected] = information
        data[ticker_selected]["next_update"] = next_update_time
        r.seek(0)
        r.truncate()
        json.dump(data, r, indent=4)
    print("Saving {} information to yf_cached_api.json".format(ticker_selected))


if __name__ == '__main__':
    for ticker_symbol in full_ticker_list():
        ticker_info(ticker_symbol)
