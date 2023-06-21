import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from scheduled_tasks.others.get_popular_tickers import *
from scheduled_tasks.twitter.twitter_connection import *
from scheduled_tasks.reddit.reddit_utils import *


def main():
    print("Getting Twitter Stock Trending...")
    all_symbols = list(get_mapping_coins().keys())
    all_symbols.extend(full_ticker_list())
    for symbol in all_symbols:
        # try:
        if len(symbol) > 1:
            print(symbol)
            url = f"https://api.twitter.com/2/tweets/counts/recent?query={symbol}&granularity=day"
            json_response = connect_to_endpoint(url)
            for i in json_response["data"]:
                start_date = i["start"]
                end_date = i["end"]
                if end_date.endswith("00:00:00.000Z"):
                    tweet_count = i["tweet_count"]
                    cur.execute("INSERT IGNORE INTO twitter_trending VALUES (%s, %s, %s)",
                                (symbol, tweet_count, start_date.split("T")[0]))
                    cnx.commit()
        time.sleep(1)
        # except:
        #     continue
    print("Twitter Stock Trending Successfully Completed...\n")


if __name__ == "__main__":
    main()
