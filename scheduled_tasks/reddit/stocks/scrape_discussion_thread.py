import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from scheduled_tasks.reddit.reddit_utils import *
from scheduled_tasks.reddit.stocks.fast_yahoo import download_advanced_stats, download_quick_stats

current_datetime = datetime.utcnow()
mapping_stocks = get_mapping_stocks()


def extract_ticker(text, date_posted, tickers_dict, tickers_post_dict, sentiment_dict, calls_dict, calls_mentions, puts_dict,
                   puts_mentions):
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
    calls_dict: dict
        calls dict of tickers
    calls_mentions: bool
        whether or not 'call(s)' or '100C' is mentioned
    puts_dict: dict
        puts dict of tickers
    puts_mentions: bool
        whether or not 'put(s)' or '100P' is mentioned
    """
    upper_text = text.upper()
    for word in upper_text.split():
        for key, value in mapping_stocks.items():
            if word in value:
                upper_text = upper_text.replace(word, key)

    extracted_tickers = set(re.findall(pattern, upper_text))

    # Get sentiment of comment
    vs = analyzer.polarity_scores(text)
    sentiment_score = float(vs['compound'])

    for ticker in extracted_tickers:
        tickers_dict[ticker] = tickers_dict.get(ticker, 0) + 1
        sentiment_dict[ticker] = sentiment_dict.get(ticker, 0) + sentiment_score

        if ticker in tickers_post_dict:
            tickers_post_dict[ticker].append({"ticker": ticker, "text_body": text[:500], "sentiment": sentiment_score, "date_posted": date_posted})
        else:
            tickers_post_dict[ticker] = [{"ticker": ticker, "text_body": text[:500], "sentiment": sentiment_score, "date_posted": date_posted}]

        if calls_mentions:
            calls_dict[ticker] = calls_dict.get(ticker, 0) + 1
        if puts_mentions:
            puts_dict[ticker] = puts_dict.get(ticker, 0) + 1


def check_for_options(text):
    """
    Check whether or not text contains anything related to options (call, put, 100C, 100P etc)
    Parameters
    ----------
    text: str
        comment
    """
    if re.findall("CALL|\d+C", text):
        calls_mentions = True
    else:
        calls_mentions = False
    if re.findall("PUT|\d+P", text):
        puts_mentions = True
    else:
        puts_mentions = False
    return calls_mentions, puts_mentions


def wsb_live():
    """
    Get real time sentiment from wsb daily discussion thread
    """
    current_datetime_str = str(current_datetime).rsplit(":", 1)[0]

    minute_hand = round_time(current_datetime_str.split(":")[1])
    current_datetime_str = current_datetime_str[:-2] + round_time(minute_hand)
    threshold_datetime = datetime.timestamp(current_datetime - timedelta(minutes=10))

    basic_stopwords_list = words_to_remove()

    subreddit = reddit.subreddit("wallstreetbets")

    all_words_dict = dict()
    tickers_dict = dict()
    tickers_post_dict = dict()
    sentiment_dict = dict()
    calls_dict = dict()
    puts_dict = dict()
    for post in subreddit.hot(limit=10):
        # try:
        # Ensure that post is stickied and the post is not an image
        if post.stickied and ".jpg" not in post.url and ".png" not in post.url and "comments" in post.url:
            print(post.url)
            submission = reddit.submission(url=post.url)

            submission.comment_sort = "new"
            submission.comments.replace_more(limit=0)

            for comment in submission.comments:
                if threshold_datetime < comment.created_utc:
                    comment_body = comment.body
                    print(comment.created_utc)
                    date_posted = datetime.fromtimestamp(comment.created_utc)

                    # Remove number/special characters (clean up word cloud)
                    all_words_dict = insert_into_word_cloud_dict(comment_body.upper(), all_words_dict)

                    # Check if calls and puts is mentioned in comment
                    calls_mentions, puts_mentions = check_for_options(comment_body.upper())

                    # Get ticker based on pattern
                    extract_ticker(comment_body, date_posted, tickers_dict, tickers_post_dict, sentiment_dict, calls_dict,
                                   calls_mentions, puts_dict, puts_mentions)

                    # Read sub-comment
                    for second_level_comment in comment.replies:
                        second_level_comment = second_level_comment.body

                        # Insert into word cloud
                        all_words_dict = insert_into_word_cloud_dict(second_level_comment.upper(), all_words_dict)

                        # Check if calls and puts is mentioned in comment
                        calls_mentions, puts_mentions = check_for_options(second_level_comment.upper())

                        # Get ticker based on pattern
                        extract_ticker(second_level_comment, date_posted, tickers_dict, tickers_post_dict, sentiment_dict,
                                       calls_dict, calls_mentions, puts_dict, puts_mentions)
        # except:
        #     print("ERROR")
        #     pass

    # Remove ticker if it is found in stopwords_list
    tickers_dict = dict(sorted(tickers_dict.items(), key=lambda item: item[1]))
    for key in list(tickers_dict.keys()):
        if key in stopwords_list:
            del tickers_dict[key]

    # Remove word from word cloud if it is found in all_words_dict
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
    df.to_sql("wsb_word_cloud", engine, if_exists="append", index=False)

    quick_stats = {'regularMarketPreviousClose': 'prvCls',
                   'regularMarketVolume': 'volume',
                   'regularMarketPrice': 'price',
                   'marketCap': 'mkt_cap'}
    quick_stats_df = download_quick_stats(list(tickers_dict.keys()), quick_stats, threads=True)

    # Ticker must be active in order to be valid
    quick_stats_df["volume"] = pd.to_numeric(quick_stats_df["volume"], errors='coerce')
    quick_stats_df["price"] = pd.to_numeric(quick_stats_df["price"], errors='coerce')
    quick_stats_df.dropna(inplace=True)
    quick_stats_df = quick_stats_df[quick_stats_df["price"] >= 0.5]
    quick_stats_df = quick_stats_df[quick_stats_df["volume"] >= 50000]
    valid_ticker_list = list(quick_stats_df.index.values)

    # Combine into 1 df
    mentions_list = list()
    sentiment_list = list()
    calls_list = list()
    puts_list = list()
    post_list = list()

    for ticker in valid_ticker_list:
        mentions_list.append(tickers_dict[ticker])
        sentiment_list.append(sentiment_dict[ticker])
        calls_list.append(calls_dict.get(ticker, 0))
        puts_list.append(puts_dict.get(ticker, 0))
        post_list.append(tickers_post_dict[ticker])

    for ticker_post_list in post_list:
        for i in ticker_post_list:
            print(i["ticker"], i["text_body"], i["sentiment"], i["date_posted"])
            cur.execute("INSERT INTO wsb_discussions VALUES (%s, %s, %s, %s)", (i["ticker"], i["text_body"], i["sentiment"], i["date_posted"]))
            cnx.commit()

    quick_stats_df["mentions"] = mentions_list
    quick_stats_df["sentiment"] = sentiment_list
    quick_stats_df["sentiment"] = quick_stats_df["sentiment"] / quick_stats_df["mentions"]
    quick_stats_df["sentiment"] = quick_stats_df["sentiment"].round(2)
    quick_stats_df["calls"] = calls_list
    quick_stats_df["puts"] = puts_list
    print(quick_stats_df)

    for index, row in quick_stats_df.iterrows():
        cur.execute("INSERT INTO wsb_trending_24H VALUES (%s, %s, %s, %s, %s, %s)",
                    (index, row[4], row[5], row[6], row[7], current_datetime_str))
        cnx.commit()


def update_hourly():
    """
    Group all mentions in the last hour together
    """
    threshold_datetime = str(current_datetime - timedelta(hours=1))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"

    cur.execute("SELECT ticker, SUM(mentions), AVG(sentiment), SUM(calls), SUM(puts) FROM wsb_trending_24H WHERE "
                "date_updated > %s GROUP BY ticker", (threshold_datetime, ))
    x = cur.fetchall()
    for row in x:
        cur.execute("INSERT INTO wsb_trending_hourly VALUES (%s, %s, %s, %s, %s, %s)", (row + (threshold_hour, )))
        cnx.commit()


def wsb_change():
    """
    Find out change in mentions in last 24 hours
    """
    threshold_datetime = str(current_datetime - timedelta(hours=24))
    threshold_hour = threshold_datetime.rsplit(":", 2)[0] + ":00"

    threshold_datetime2 = str(current_datetime - timedelta(hours=48))
    threshold_hour2 = threshold_datetime2.rsplit(":", 2)[0] + ":00"

    cur.execute("SELECT ticker AS Ticker, SUM(mentions) AS Mentions, AVG(sentiment) AS Sentiment FROM wsb_trending_24H "
                "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) "
                "DESC LIMIT 50".format(threshold_hour))
    current = cur.fetchall()
    cur.execute("DELETE FROM wsb_change")
    for row in current:
        ticker = row[0]
        current_mentions = row[1]
        cur.execute("SELECT SUM(mentions) FROM wsb_trending_hourly WHERE date_updated < %s AND date_updated >= %s "
                    "AND ticker=%s", (threshold_hour, threshold_hour2, ticker))
        previous_mentions = cur.fetchone()[0]

        if previous_mentions is not None:
            percent_change = round((current_mentions - previous_mentions) / previous_mentions, 2) * 100
            if percent_change > 1000:
                percent_change = 1000
        else:
            percent_change = 1000

        cur.execute("INSERT INTO wsb_change VALUES (%s, %s, %s)", (ticker, current_mentions, percent_change))
        cnx.commit()


def get_mkt_cap():
    threshold_datetime = str(current_datetime - timedelta(hours=24))

    ticker_list, mentions_list = list(), list()
    cur.execute("SELECT ticker, SUM(mentions) FROM wsb_trending_24H WHERE date_updated > %s GROUP BY "
                "ticker ORDER BY SUM(mentions) DESC LIMIT 50", (threshold_datetime,))
    x = cur.fetchall()
    for row in x:
        ticker_list.append(row[0])
        mentions_list.append(row[1])

    quick_stats_dict = {'summaryDetail': {"fiftyDayAverage": "avg_price",
                                          "fiftyTwoWeekHigh": "52w_high",
                                          "fiftyTwoWeekLow": "52w_low"},
                        'price': {"marketCap": "mkt_cap",
                                  "regularMarketChangePercent": "price_change",
                                  'regularMarketPrice': 'current_price'},
                        'summaryProfile': {"industry": "industry",
                                           "sector": "sector"}}

    quick_stats_df = download_advanced_stats(ticker_list, quick_stats_dict, threads=True)
    quick_stats_df = quick_stats_df[quick_stats_df["avg_price"] != "N/A"]
    quick_stats_df = quick_stats_df[quick_stats_df["52w_high"] != "N/A"]
    quick_stats_df = quick_stats_df[quick_stats_df["52w_low"] != "N/A"]
    quick_stats_df["difference_sma"] = 100 * (quick_stats_df["avg_price"] - quick_stats_df["current_price"]) / \
                                       quick_stats_df["avg_price"]
    quick_stats_df["difference_52w_high"] = 100 * (quick_stats_df["52w_high"] - quick_stats_df["current_price"]) / \
                                            quick_stats_df["52w_high"]
    quick_stats_df["difference_52w_low"] = 100 * (quick_stats_df["52w_low"] - quick_stats_df["current_price"]) / \
                                           quick_stats_df["52w_low"]

    del quick_stats_df["current_price"]
    del quick_stats_df["avg_price"]
    del quick_stats_df["52w_high"]
    del quick_stats_df["52w_low"]

    quick_stats_df["price_change"] = quick_stats_df["price_change"].apply(lambda k: round(k*100, 2))
    quick_stats_df = quick_stats_df.reindex(ticker_list)
    quick_stats_df["mentions"] = mentions_list
    quick_stats_df.reset_index(inplace=True)
    quick_stats_df.rename(columns={"Symbol": "ticker"}, inplace=True)
    print(quick_stats_df)
    quick_stats_df.to_sql("wsb_yf", engine, if_exists="replace", index=False)


if __name__ == '__main__':
    wsb_live()
    update_hourly()
    wsb_change()
    get_mkt_cap()
