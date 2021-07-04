import os
import json
import yfinance.ticker as yf
from datetime import datetime

import scheduled_tasks.get_short_volume as get_short_volume

# Time Format: HHMMSS
market_open_time = "133000"
market_close_time = "200000"


def ticker_info(ticker_selected):
    """
    Cache ticker information into a json file when market is closed to speed up rendering time
    Parameters
    ----------
    ticker_selected: str
        ticker symbol (e.g: AAPL)
    """
    ticker = yf.Ticker(ticker_selected)
    current_datetime = datetime.utcnow()
    current_utc_time = str(current_datetime).split()[1].split(".")[0].replace(":", "")
    if current_utc_time > market_close_time or current_utc_time < market_open_time or current_datetime.today().weekday() >= 5:
        with open(r"../yf_cached_api.json", "w") as r:
            data = json.load(r)
            if ticker_selected not in data:
                information = ticker.info
                data[ticker_selected] = information
                r.seek(0)
                json.dump(data, r, indent=4)
        print("Saving {} information to yf_cached_api.json".format(ticker_selected))
    else:
        os.remove(r"yf_cached_api.json")
        with open(r"yf_cached_api.json", "w") as r:
            json.dump({}, r, indent=4)


if __name__ == '__main__':
    for ticker_symbol in get_short_volume.full_ticker_list():
        ticker_info(ticker_symbol)
