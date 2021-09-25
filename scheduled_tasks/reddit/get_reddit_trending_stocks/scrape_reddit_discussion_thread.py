import re
import os
import sys
import sqlite3
import praw
import pandas as pd
from nltk.corpus import stopwords
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
import scheduled_tasks.reddit.config as cfg
from scheduled_tasks.reddit.get_reddit_trending_stocks.fast_yahoo import download_quick_stats
from custom_extensions.stopwords import stopwords_list
from custom_extensions.custom_words import new_words

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

reddit = praw.Reddit(client_id=cfg.API_REDDIT_CLIENT_ID,
                     client_secret=cfg.API_REDDIT_CLIENT_SECRET,
                     user_agent=cfg.API_REDDIT_USER_AGENT)

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

pattern = "(?<=\$)?\\b[A-Z]{1,5}\\b(?:\.[A-Z]{1,2})?"
current_datetime = datetime.utcnow()


def round_time(time_string, base=5):
    return str(base * round(int(time_string)/base))


def wsb_live():
    """
    Get real time sentiment from wsb daily discussion thread
    """
    # current_datetime_str = str(current_datetime).rsplit(":", 1)[0][:-1] + "0"
    current_datetime_str = str(current_datetime).rsplit(":", 1)[0]

    minute_hand = round_time(current_datetime_str.split(":")[1])
    current_datetime_str = current_datetime_str[:-2] + round_time(minute_hand)
    print(current_datetime_str)
    threshold_datetime = datetime.timestamp(current_datetime - timedelta(minutes=15))

    basic_stopwords_list = list(map(lambda x: re.sub(r'\W+', '', x.upper()), stopwords.words('english'))) + \
                           ["THATS", "GOT", "IM", "LIKE", "STILL", "EVER", "EVEN", "CANT", "US", "THATS", "GO", "WOULD",
                            "MUCH", "GET", "ONE", "SEE", "WAY", "NEED", "TAKE", "MAKE", "GETTING", "GOING", "GONNA",
                            "NEED", "THINK", "SAY", "SAID", "KNOW", "WAY", "TIME", "WEEK", "WELL", "WANT", "THING",
                            "LETS", "IVE"]

    subreddit = reddit.subreddit("wallstreetbets")

    all_words_dict = dict()
    tickers_dict = dict()
    sentiment_dict = dict()
    for post in subreddit.hot(limit=10):
        if post.stickied and ".jpg" not in post.url:
            print(post.url)
            submission = reddit.submission(url=post.url)

            submission.comment_sort = "new"
            submission.comments.replace_more(limit=0)

            for comment in submission.comments:
                if threshold_datetime < comment.created_utc:
                    comment_body = comment.body

                    vs = analyzer.polarity_scores(comment_body)
                    sentiment_score = float(vs['compound'])
                    print(datetime.fromtimestamp(comment.created_utc), sentiment_score, comment_body)

                    for word in comment_body.upper().split():
                        word = re.sub(r'\W+', '', word)
                        all_words_dict[word] = all_words_dict.get(word, 0) + 1

                    extracted_tickers = set(re.findall(pattern, comment_body.upper()))
                    print(extracted_tickers)
                    for ticker in extracted_tickers:
                        tickers_dict[ticker] = tickers_dict.get(ticker, 0) + 1
                        sentiment_dict[ticker] = sentiment_dict.get(ticker, 0) + sentiment_score

                    for second_level_comment in comment.replies:
                        second_level_comment = second_level_comment.body

                        vs = analyzer.polarity_scores(second_level_comment)
                        sentiment_score = float(vs['compound'])
                        # print('$$$$ Score: ', sentiment_score, "|", second_level_comment)

                        for word in second_level_comment.upper().split():
                            word = re.sub(r'\W+', '', word)
                            all_words_dict[word] = all_words_dict.get(word, 0) + 1

                        extracted_tickers = set(re.findall(pattern, second_level_comment.upper()))
                        for ticker in extracted_tickers:
                            tickers_dict[ticker] = tickers_dict.get(ticker, 0) + 1
                            sentiment_dict[ticker] = sentiment_dict.get(ticker, 0) + sentiment_score

    tickers_dict = dict(sorted(tickers_dict.items(), key=lambda item: item[1]))
    for key in list(tickers_dict.keys()):
        if key in stopwords_list:
            del tickers_dict[key]

    all_words_dict = dict(sorted(all_words_dict.items(), key=lambda item: item[1]))
    for key in list(all_words_dict.keys()):
        if key in basic_stopwords_list:
            del all_words_dict[key]

    df = pd.DataFrame(all_words_dict, index=[0])
    df = df.T
    df.reset_index(inplace=True)
    df.rename(columns={"index": "word", 0: "mentions"}, inplace=True)
    df = df[(df["mentions"] >= 3) & (df["word"].str.len() > 1)]
    df["date_updated"] = current_datetime_str
    df.to_sql("wsb_word_cloud", conn, if_exists="append", index=False)

    quick_stats = {'regularMarketPreviousClose': 'prvCls',
                   'regularMarketVolume': 'volume',
                   'regularMarketPrice': 'price',
                   'marketCap': 'mkt_cap'}
    quick_stats_df = download_quick_stats(list(tickers_dict.keys()), quick_stats, threads=True)
    quick_stats_df = quick_stats_df[quick_stats_df["volume"] != "N/A"]
    quick_stats_df.dropna(inplace=True)
    quick_stats_df = quick_stats_df[quick_stats_df["volume"] >= 500000]
    valid_ticker_list = list(quick_stats_df.index.values)

    mentions_list = list()
    sentiment_list = list()
    for ticker in valid_ticker_list:
        mentions_list.append(tickers_dict[ticker])
        sentiment_list.append(sentiment_dict[ticker])

    quick_stats_df["mentions"] = mentions_list
    quick_stats_df["sentiment"] = sentiment_list
    quick_stats_df["sentiment"] = quick_stats_df["sentiment"] / quick_stats_df["mentions"]
    quick_stats_df["sentiment"] = quick_stats_df["sentiment"].round(2)
    print(quick_stats_df)

    for index, row in quick_stats_df.iterrows():
        db.execute("INSERT INTO wsb_trending_24H VALUES (?, ?, ?, ?)",
                   (index, row[4], row[5], current_datetime_str))
        conn.commit()


def update_hourly():
    """
    Group all mentions in the last hour together
    """
    threshold_datetime = str(current_datetime - timedelta(hours=1))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"
    print(threshold_hour, "onwards being saved to hourly database")

    db.execute("SELECT ticker, SUM(mentions), AVG(sentiment) FROM wsb_trending_24H WHERE date_updated > ? GROUP BY "
               "ticker", (threshold_datetime, ))
    x = db.fetchall()
    for row in x:
        db.execute("INSERT INTO wsb_trending_hourly VALUES (?, ?, ?, ?)", (row + (threshold_hour, )))
        conn.commit()


def wsb_change():
    """
    Find out change in mentions in last 24 hours
    """
    threshold_datetime = str(current_datetime - timedelta(hours=24))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"

    threshold_datetime2 = str(current_datetime - timedelta(hours=48))
    threshold_hour2 = threshold_datetime2.rsplit(":", 2)[0] + ":00"

    print(threshold_hour, threshold_hour2)

    db.execute("SELECT ticker AS Ticker, SUM(mentions) AS Mentions, AVG(sentiment) AS Sentiment FROM wsb_trending_24H "
               "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) DESC LIMIT 50".format(threshold_hour))
    current = db.fetchall()
    db.execute("DELETE FROM wsb_change")
    for row in current:
        ticker = row[0]
        current_mentions = row[1]
        db.execute("SELECT SUM(mentions) FROM wsb_trending_hourly WHERE date_updated < ? AND date_updated >= ? "
                   "AND ticker=?", (threshold_hour, threshold_hour2, ticker))
        previous_mentions = db.fetchone()[0]

        if previous_mentions is not None:
            percent_change = round((current_mentions - previous_mentions) / previous_mentions, 2) * 100
            if percent_change > 1000:
                percent_change = 1000
        else:
            percent_change = 1000

        db.execute("INSERT INTO wsb_change VALUES (?, ?, ?)", (ticker, current_mentions, percent_change))
        conn.commit()


def get_mkt_cap():
    threshold_datetime = str(current_datetime - timedelta(hours=24))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"
    print(threshold_hour, "onwards being saved to yf database")

    ticker_list, mentions_list = list(), list()
    db.execute("SELECT ticker, SUM(mentions) FROM wsb_trending_24H WHERE date_updated > ? GROUP BY "
               "ticker ORDER BY SUM(mentions) DESC LIMIT 50", (threshold_datetime,))
    x = db.fetchall()
    for row in x:
        ticker_list.append(row[0])
        mentions_list.append(row[1])
    quick_stats_dict = {'marketCap': 'mkt_cap',
                        'regularMarketChangePercent': 'price_change',
                        'regularMarketPrice': 'current_price',
                        'fiftyDayAverage': 'avg_price',
                        'fiftyTwoWeekHigh': '52w_high',
                        'fiftyTwoWeekLow': '52w_low'}
    quick_stats_df = download_quick_stats(ticker_list, quick_stats_dict, threads=True)
    quick_stats_df["difference_sma"] = 100 * (quick_stats_df["avg_price"] - quick_stats_df["current_price"]) / \
                                       quick_stats_df["avg_price"]
    quick_stats_df["difference_52w_high"] = 100 * (quick_stats_df["52w_high"] - quick_stats_df["current_price"]) / \
                                            quick_stats_df["52w_high"]
    quick_stats_df["difference_52w_low"] = 100 * (quick_stats_df["52w_low"] - quick_stats_df["current_price"]) / \
                                           quick_stats_df["52w_low"]
    quick_stats_df["mentions"] = mentions_list
    quick_stats_df.reset_index(inplace=True)
    quick_stats_df.rename(columns={"Symbol": "ticker"}, inplace=True)

    del quick_stats_df["current_price"]
    del quick_stats_df["avg_price"]
    del quick_stats_df["52w_high"]
    del quick_stats_df["52w_low"]

    quick_stats_df.to_sql("wsb_yf", conn, if_exists="replace", index=False)
    print(quick_stats_df)


if __name__ == '__main__':
    # wsb_live()
    # update_hourly()
    wsb_change()
    # get_mkt_cap()

    # python scheduled_tasks/reddit/get_reddit_trending_stocks/scrape_reddit_discussion_thread.py

