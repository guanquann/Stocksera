import re
import os
import sys
import sqlite3
import praw
import pandas as pd
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

pattern = "(?<=\$)?\\b[A-Z]{2,5}\\b(?:\.[A-Z]{1,2})?"


def wsb_live():
    """
    Get real time sentiment from wsb daily discussion thread
    THIS IS STILL IN DEVELOPMENT. DO NOT ASK ME TO FIX ANY BUG FIXES YET
    """
    current_datetime = datetime.now()
    threshold_datetime = datetime.timestamp(current_datetime - timedelta(minutes=60))
    print(threshold_datetime)
    # stopwords_list = list(map(lambda word: re.sub(r'\W+', '', word.upper()), stopwords.words('english')))

    subreddit = reddit.subreddit("wallstreetbets")

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
                    # print(datetime.fromtimestamp(comment.created_utc), sentiment_score, comment_body)

                    extracted_tickers = set(re.findall(pattern, comment_body.upper()))
                    for ticker in extracted_tickers:
                        tickers_dict[ticker] = tickers_dict.get(ticker, 0) + 1
                        sentiment_dict[ticker] = sentiment_dict.get(ticker, 0) + sentiment_score

                    for second_level_comment in comment.replies:
                        second_level_comment = second_level_comment.body

                        vs = analyzer.polarity_scores(second_level_comment)
                        sentiment_score = float(vs['compound'])
                        # print('$$$$ Score: ', sentiment_score, "|", second_level_comment)

                        extracted_tickers = set(re.findall(pattern, second_level_comment.upper()))
                        for ticker in extracted_tickers:
                            tickers_dict[ticker] = tickers_dict.get(ticker, 0) + 1
                            sentiment_dict[ticker] = sentiment_dict.get(ticker, 0) + sentiment_score

    tickers_dict = dict(sorted(tickers_dict.items(), key=lambda item: item[1]))
    for key in list(tickers_dict.keys()):
        if key in stopwords_list:
            del tickers_dict[key]

    quick_stats = {'regularMarketPreviousClose': 'prvCls',
                   'regularMarketVolume': 'volume',
                   'regularMarketPrice': 'price',
                   'marketCap': 'mkt_cap'}

    quick_stats_df = download_quick_stats(list(tickers_dict.keys()), quick_stats, threads=True)
    quick_stats_df = quick_stats_df[quick_stats_df["mkt_cap"] != "N/A"]
    quick_stats_df = quick_stats_df[quick_stats_df["mkt_cap"] >= 1000000000]
    quick_stats_df = quick_stats_df[quick_stats_df["volume"] >= 500000]
    valid_ticker_list = list(quick_stats_df.index.values)

    mentions_list = list()
    sentiment_list = list()
    for ticker in valid_ticker_list:
        mentions_list.append(tickers_dict[ticker])
        sentiment_list.append(sentiment_dict[ticker])

    quick_stats_df["mentions"] = mentions_list
    quick_stats_df["total_sentiment"] = sentiment_list

    print(quick_stats_df)

    for index, row in quick_stats_df.iterrows():
        db.execute("INSERT INTO wsb_trending_24H VALUES (?, ?, ?)", (index, row[4], str(current_datetime).rsplit(":", 1)[0]))
        conn.commit()


if __name__ == '__main__':
    wsb_live()
