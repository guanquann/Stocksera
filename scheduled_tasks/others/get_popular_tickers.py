import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


def full_ticker_list():
    """
    List of all the popular tickers identified. Add more to the list if you wish to
    """
    return json.load(open("custom_extensions/ticker_list.json"))["list_of_tickers"]


if __name__ == "__main__":
    full_ticker_list()
