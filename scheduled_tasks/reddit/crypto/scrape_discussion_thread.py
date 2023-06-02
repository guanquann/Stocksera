import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from scheduled_tasks.reddit.reddit_utils import *

current_datetime = datetime.utcnow()

crypto_dict = get_mapping_coins()


def extract_ticker(text, tickers_dict, sentiment_dict, sentiment_score):
    """
    Extract tickers with correct pattern from comment and add sentiment, calls, put to previous dict
    Parameters
    ----------
    text: str
        comment
    tickers_dict: dict
        previous dict of word cloud
    sentiment_dict: dict
        sentiment dict of tickers
    sentiment_score: float
        sentiment of comment
    """
    extracted_tickers_set = set()
    for word in text.upper().split():
        for key, value in crypto_dict.items():
            word = re.sub(r'\d|\W+', '', word)
            if word in value:
                extracted_tickers_set.add(key)
    for ticker in extracted_tickers_set:
        tickers_dict[ticker] = tickers_dict.get(ticker, 0) + 1
        sentiment_dict[ticker] = sentiment_dict.get(ticker, 0) + sentiment_score
    return tickers_dict, sentiment_dict


def upload_to_database(tickers_dict, sentiment_dict, current_datetime_str):
    """
    Upload df to sql database
    """
    trending_df = pd.DataFrame()
    trending_df["ticker"] = tickers_dict.keys()
    trending_df["mentions"] = tickers_dict.values()
    trending_df["sentiment"] = sentiment_dict.values()
    trending_df["sentiment"] = trending_df["sentiment"] / trending_df["mentions"]
    trending_df["sentiment"] = trending_df["sentiment"].round(2)
    trending_df["date_updated"] = current_datetime_str
    trending_df.sort_values(by=["mentions"], ascending=False, inplace=True)
    trending_df.to_sql("crypto_trending_24H", engine, if_exists="append", index=False)


def crypto_live():
    """
    Get mentions from r/cryptocurrency discussion thread in the last 10 minutes
    """
    current_datetime_str = str(current_datetime).rsplit(":", 1)[0]

    minute_hand = round_time(current_datetime_str.split(":")[1])
    current_datetime_str = current_datetime_str[:-2] + round_time(minute_hand)
    threshold_datetime = datetime.timestamp(current_datetime - timedelta(minutes=10))

    basic_stopwords_list = words_to_remove()

    subreddit = reddit.subreddit("cryptocurrency")

    all_words_dict = dict()
    tickers_dict = dict()
    sentiment_dict = dict()

    for post in subreddit.hot(limit=10):
        # Ensure that post is stickied and the post is not an image
        if post.stickied and ".jpg" not in post.url and ".png" not in post.url and "https" in post.url and \
                "comments" in post.url:
            submission = reddit.submission(url=post.url)

            submission.comment_sort = "new"
            submission.comments.replace_more(limit=0)

            for comment in submission.comments:
                if threshold_datetime < comment.created_utc:
                    comment_body = comment.body

                    # Get sentiment of comment
                    vs = analyzer.polarity_scores(comment_body)
                    sentiment_score = float(vs['compound'])

                    # Remove number/special characters (clean up word cloud)
                    all_words_dict = insert_into_word_cloud_dict(comment_body, all_words_dict)

                    # Get ticker based on pattern
                    tickers_dict, sentiment_dict = extract_ticker(comment_body, tickers_dict, sentiment_dict, sentiment_score)

                    # Read sub-comment
                    for second_level_comment in comment.replies:
                        second_level_comment = second_level_comment.body

                        # Get sentiment of comment
                        vs = analyzer.polarity_scores(second_level_comment)
                        sentiment_score = float(vs['compound'])

                        # Insert into word cloud
                        all_words_dict = insert_into_word_cloud_dict(second_level_comment, all_words_dict)

                        # Get ticker based on pattern
                        tickers_dict, sentiment_dict = extract_ticker(second_level_comment, tickers_dict,
                                                                      sentiment_dict, sentiment_score)

    # Remove word from word cloud if it is found in stopwords_list
    all_words_dict = dict(sorted(all_words_dict.items(), key=lambda item: item[1]))
    for key in list(all_words_dict.keys()):
        if key in basic_stopwords_list:
            del all_words_dict[key]

    df = pd.DataFrame(all_words_dict, index=[0])
    df = df.T
    df.reset_index(inplace=True)
    df.rename(columns={"index": "word", 0: "mentions"}, inplace=True)

    # Criteria to insert into db
    df = df[(df["mentions"] >= 3) & (df["word"].str.len() > 1)]

    df["date_updated"] = current_datetime_str
    df.to_sql("crypto_word_cloud", engine, if_exists="append", index=False)

    upload_to_database(tickers_dict, sentiment_dict, current_datetime_str)


def update_hourly():
    """
    Group all mentions in the last hour together
    """
    threshold_datetime = str(current_datetime - timedelta(hours=1))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"

    cur.execute("SELECT ticker, SUM(mentions), AVG(sentiment) FROM crypto_trending_24H WHERE "
                "date_updated > %s GROUP BY ticker", (threshold_datetime, ))
    x = cur.fetchall()
    for row in x:
        cur.execute("INSERT INTO crypto_trending_hourly VALUES (%s, %s, %s, %s)", (row + (threshold_hour, )))
        cnx.commit()


def crypto_change():
    """
    Find out change in mentions in last 24 hours
    """
    threshold_datetime = str(current_datetime - timedelta(hours=24))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"

    threshold_datetime2 = str(current_datetime - timedelta(hours=48))
    threshold_hour2 = threshold_datetime2.rsplit(":", 2)[0] + ":00"

    cur.execute("SELECT ticker AS Ticker, SUM(mentions) AS Mentions, AVG(sentiment) AS Sentiment "
                "FROM crypto_trending_24H WHERE date_updated >= %s GROUP BY ticker ORDER BY SUM(mentions) "
                "DESC LIMIT 50", (threshold_hour, ))
    current = cur.fetchall()
    cur.execute("DELETE FROM crypto_change")
    for row in current:
        ticker = row[0]
        current_mentions = row[1]
        cur.execute("SELECT SUM(mentions) FROM crypto_trending_hourly WHERE date_updated < %s AND date_updated >= %s "
                    "AND ticker=%s", (threshold_hour, threshold_hour2, ticker))
        previous_mentions = cur.fetchone()[0]

        if previous_mentions is not None:
            percent_change = round((current_mentions - previous_mentions) / previous_mentions, 2) * 100
            if percent_change > 1000:
                percent_change = 1000
        else:
            percent_change = 1000

        cur.execute("INSERT INTO crypto_change VALUES (%s, %s, %s)", (ticker, current_mentions, percent_change))
        cnx.commit()


def main():
    print("Getting Crypto Live Thread Trending...")
    crypto_live()
    update_hourly()
    crypto_change()
    print("Crypto Live Thread Successfully Completed...\n")


if __name__ == '__main__':
    main()

