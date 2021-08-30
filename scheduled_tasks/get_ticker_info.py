import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scheduled_tasks.get_popular_tickers import full_ticker_list
from fast_yahoo import *


def ticker_info(ticker_list):
    """
    Cache ticker information into a json file to speed up rendering time
    Parameters
    ----------
    ticker_list: list
        list of tickers (e.g: ['AAPL', 'NIO', 'BB'])
    """
    with open(r"database/yf_cached_api.json", "w") as r:
        information = download_advanced_stats(ticker_list)
        json.dump(information, r, indent=4)
    print("All data saved to database/yf_cached_api.json")


if __name__ == '__main__':
    ticker_info(full_ticker_list())
