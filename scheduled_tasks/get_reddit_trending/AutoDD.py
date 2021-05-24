import sys
import os
import re
import locale
from datetime import datetime, timedelta
from psaw import PushshiftAPI
from tabulate import tabulate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3

from scheduled_tasks.get_reddit_trending.fast_yahoo import *
from custom_extensions.stopwords import stopwords_list
from custom_extensions.custom_words import new_words

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

# dictionary of possible subreddits to search in with their respective column name
subreddit_dict = {'pennystocks': 'pnnystks',
                  'RobinHoodPennyStocks': 'RHPnnyStck',
                  'Daytrading': 'daytrade',
                  'StockMarket': 'stkmrkt',
                  'stocks': 'stocks',
                  'investing': 'investing',
                  'wallstreetbets': 'WSB'}

# x base point of for a ticker that appears on a subreddit title or text body that fits the search criteria
base_points = 2

# x bonus points for each flair matching 'DD' or 'Catalyst' of for a ticker that appears on the subreddit
bonus_points = 1

# every x upvotes on the thread counts for 1 point (rounded down)
upvote_factor = 3

# x bonus points for the sentiment of ticker
positive_sentiment = 2
neutral_sentiment = 1
negative_sentiment = 0

# rocket emoji
rocket = '🚀'


def get_sentiment(text, increment):
    vs = analyzer.polarity_scores(text)
    if vs['compound'] >= 0.05:
        increment += positive_sentiment
        sentiment = "positive"
    elif vs['compound'] <= -0.05:
        increment += negative_sentiment
        sentiment = "negative"
    else:
        increment += neutral_sentiment
        sentiment = "neutral"
    return increment, sentiment


def get_submission_psaw(n, sub_dict):
    """
    Returns a list of results for submission in past:
    1st list: current result from n hours ago until now
    2nd list: prev result from 2n hours ago until n hours ago
    """
    api = PushshiftAPI()

    mid_interval = datetime.today() - timedelta(hours=n)
    timestamp_mid = int(mid_interval.timestamp())
    timestamp_start = int((mid_interval - timedelta(hours=n)).timestamp())
    timestamp_end = int(datetime.today().timestamp())
    recent = {}
    prev = {}
    for key in sub_dict:
        # results from the last n hours
        recent[key] = api.search_submissions(after=timestamp_mid,
                                             before=timestamp_end,
                                             subreddit=key,
                                             filter=['title', 'link_flair_text', 'selftext', 'score'])

        # results from the last 2n hours until n hours ago
        prev[key] = api.search_submissions(after=timestamp_start,
                                           before=timestamp_mid,
                                           subreddit=key,
                                           filter=['title', 'link_flair_text', 'selftext', 'score'])

    return recent, prev


def get_submission_generators(n, sub):
    """
    Returns two dictionaries:
    1st dictionary: current result from n hours ago until now
    2nd dictionary: prev result from 2n hours ago until n hours ago
    The two dictionaries' keys are the requested subreddit: all subreddits if allsub is True, and just "sub" otherwise
    The value paired with each subreddit key is a generator which traverses each submission
    Note that the generator for each subreddit will only perform http requests when it is traversed, such that this
    function itself does not retrieve any reddit data (merely the generators)
    """

    if sub not in subreddit_dict:
        subreddit_dict[sub] = sub

    sub_dict = {sub: subreddit_dict[sub]}

    recent, prev = get_submission_psaw(n, sub_dict)

    print("Searching for tickers in {}...".format(sub))
    current_scores, current_rocket_scores, current_positive, current_negative = get_ticker_scores_psaw(recent)
    prev_scores, prev_rocket_scores, prev_positive, prev_negative = get_ticker_scores_psaw(prev)

    return current_scores, current_rocket_scores, current_positive, current_negative, \
           prev_scores, prev_rocket_scores, prev_positive, prev_negative


word_dict = {}
def get_ticker_scores_psaw(sub_gen_dict):
    """
    Return two dictionaries:
    --sub_scores_dict: a dictionary of dictionaries. This dictionaries' keys are the requested subreddit: all subreddits
    if args.allsub is True, and just args.sub otherwise. The value paired with each subreddit key is a dictionary of
    scores, where each key is a ticker found in the reddit submissions.
    --rocket_scores_dict: a dictionary whose keys are the tickers found in reddit submissions, and value is the number
    of rocker emojis found for each ticker.

    :param sub_gen_dict: A dictionary of generators for each subreddit, as outputted by get_submission_generators
    """

    # Python regex pattern for stocks codes
    pattern = '(?<=\$)?\\b[A-Z]{3,5}\\b(?:\.[A-Z]{1,2})?'

    # Dictionaries containing the summaries
    sub_scores_dict = {}

    # Dictionaries containing the rocket count
    rocket_scores_dict = {}

    # Dictionaries containing sentiment ratio
    positive_sentiment_dict = {}
    negative_sentiment_dict = {}
    sentiment = "neutral"

    for sub, submission_gen in sub_gen_dict.items():

        sub_scores_dict[sub] = {}

        # looping over each submission
        for submission in submission_gen:
            # every ticker in the title will earn this base points
            increment = base_points

            # flair is worth bonus points
            if hasattr(submission, 'link_flair_text'):
                if 'DD' in submission.link_flair_text:
                    increment += bonus_points
                elif 'Catalyst' in submission.link_flair_text:
                    increment += bonus_points
                elif 'Technical Analysis' in submission.link_flair_text:
                    increment += bonus_points

            # every 3 upvotes are worth 1 extra point
            if hasattr(submission, 'score') and upvote_factor > 0:
                increment += math.ceil(submission.score / upvote_factor)

            # search the title for the ticker/tickers
            if hasattr(submission, 'title'):
                title = ' ' + submission.title.upper() + ' '
                # print(title , submission)
                bag_of_words = [re.sub(r"[^A-Z0-9]+", '', k) for k in title.split()]
                for word in bag_of_words:
                    word_dict[word] = word_dict.get(word, 0) + 1
                title_extracted = set(re.findall(pattern, title))
                increment, sentiment = get_sentiment(title, increment)

            # search the text body for the ticker/tickers
            selftext_extracted = set()
            if hasattr(submission, 'selftext'):
                selftext = ' ' + submission.selftext.upper() + ' '
                bag_of_words = [re.sub(r"[^A-Z0-9]+", '', k) for k in title.split()]
                for word in bag_of_words:
                    word_dict[word] = word_dict.get(word, 0) + 1

                selftext_extracted = set(re.findall(pattern, selftext))
                increment, sentiment = get_sentiment(selftext, increment)

            extracted_tickers = selftext_extracted.union(title_extracted)
            extracted_tickers = {ticker.replace('.', '-') for ticker in extracted_tickers}

            count_rocket = title.count(rocket) + selftext.count(rocket)
            for ticker in extracted_tickers:
                rocket_scores_dict[ticker] = rocket_scores_dict.get(ticker, 0) + count_rocket

                # title_extracted is a set, duplicate tickers from the same title counted once only
                sub_scores_dict[sub][ticker] = sub_scores_dict[sub].get(ticker, 0) + increment

                if sentiment == "positive":
                    positive_sentiment_dict[ticker] = positive_sentiment_dict.get(ticker, 0) + 1
                if sentiment == "negative":
                    negative_sentiment_dict[ticker] = negative_sentiment_dict.get(ticker, 0) + 1

    return sub_scores_dict, rocket_scores_dict, positive_sentiment_dict, negative_sentiment_dict


def populate_df(current_scores_dict, prev_scores_dict, interval):
    """
    Combine two score dictionaries, one from the current time interval, and one from the past time interval
    :returns: the populated dataframe
    """
    dict_result = {}
    total_sub_scores = {}
    # print(dict(sorted(word_dict.items(), key=lambda item: item[1])))
    for sub, current_sub_scores_dict in current_scores_dict.items():
        total_sub_scores[sub] = {}
        for symbol, current_score in current_sub_scores_dict.items():
            if symbol in dict_result.keys():
                dict_result[symbol][0] += current_score
                dict_result[symbol][1] += current_score
                # dict_result[symbol][3] = current_score
            else:
                dict_result[symbol] = [current_score, current_score, 0, 0]
            total_sub_scores[sub][symbol] = total_sub_scores[sub].get(symbol, 0) + current_score

    for sub, prev_sub_scores_dict in prev_scores_dict.items():
        for symbol, prev_score in prev_sub_scores_dict.items():
            if symbol in dict_result.keys():

                dict_result[symbol][0] += prev_score
                dict_result[symbol][2] += prev_score
                dict_result[symbol][3] = ((dict_result[symbol][1] - dict_result[symbol][2]) / dict_result[symbol][2]) * 100
                # dict_result[symbol][3] -= prev_score
            else:
                dict_result[symbol] = [prev_score, 0, prev_score, 0]  # [prev_score, 0, prev_score, -prev_score]
            total_sub_scores[sub][symbol] = total_sub_scores[sub].get(symbol, 0) + prev_score

    columns = ['one_day_score', 'recent', 'previous', 'change']  # change
    df = pd.DataFrame.from_dict(dict_result, orient='index', columns=columns)

    if len(current_scores_dict) > 1:
        dtype_dict = {}
        for sub, total_score_dict in total_sub_scores.items():
            # add each total score dict as new column of df
            df[sub] = pd.Series(total_score_dict)
            dtype_dict[sub] = 'int32'
        df = df.fillna(value=0).astype(dtype_dict)

    return df


def filter_df(df, min_val):
    """
    Filter the score dataframe
    :param dataframe df: the dataframe to be filtered
    :param int min_val: the minimum total score
    :returns: the filtered dataframe
    """
    filtered_words = stopwords_list

    # compares the first column, which is the total score to the min val
    df = df[df.iloc[:, 0] >= min_val]
    drop_index = pd.Index(filtered_words).intersection(df.index)
    df = df.drop(index=drop_index)
    return df


def get_financial_stats(results_df, min_vol, min_mkt_cap, threads=True):
    # dictionary of ticker summary profile information to get from yahoo
    summary_profile_measures = {'industry': 'industry'}

    # dictionary of ticker financial information to get from yahoo
    financial_measures = {'targetMeanPrice': 'target', 'recommendationKey': 'recommend'}

    # dictionary of ticker summary information to get from yahoo
    summary_measures = {'previousClose': 'prev_close', 'open': 'open', 'dayLow': 'day_low', 'dayHigh': 'day_high'}

    # dictionary of ticker key stats summary
    key_stats_measures = {'shortPercentOfFloat': 'short_per_float'}

    # mapping of yahoo module names to dictionaries containing data we want to retrieve
    module_name_map = {'defaultKeyStatistics': key_stats_measures, 'summaryProfile': summary_profile_measures,
                       'summaryDetail': summary_measures, 'financialData': financial_measures}

    # check for valid symbols and get quick stats
    ticker_list = list(results_df.index.values)
    quick_stats_df = get_quick_stats(ticker_list, min_vol, min_mkt_cap, threads)
    valid_ticker_list = list(quick_stats_df.index.values)

    summary_stats_df = download_advanced_stats(valid_ticker_list, module_name_map, threads)
    results_df_valid = results_df.loc[valid_ticker_list]

    results_df = pd.concat([results_df_valid, quick_stats_df, summary_stats_df], axis=1)
    results_df.index.name = 'ticker'

    return results_df


def get_quick_stats(ticker_list, min_vol, min_mkt_cap, threads=True):

    quick_stats = {'regularMarketPreviousClose': 'prvCls', 'fiftyDayAverage': '50DayAvg',
                   'regularMarketVolume': 'volume', 'averageDailyVolume3Month': '3MonthVolAvg',
                   'regularMarketPrice': 'price', 'regularMarketChangePercent': '1DayChange%',
                   'floatShares': 'floating_shares', 'beta': 'beta', 'marketCap': 'mkt_cap'}

    unprocessed_df = download_quick_stats(ticker_list, quick_stats, threads)

    processed_stats_table = []

    for index, row in unprocessed_df.iterrows():
        symbol = index
        prev_close = row['prvCls']
        avg50day = row['50DayAvg']
        price = row['price']
        day_change = row['1DayChange%']
        volume = row['volume']
        stock_float = row['floating_shares']
        beta = row['beta']
        mkt_cap = row['mkt_cap']

        valid = False
        if price != "N/A" and price != 0:
            valid = True

        if day_change != "N/A" and day_change != 0 or (day_change == 0 and price == prev_close):
            day_change = "{:.2f}".format(day_change)
            if day_change != 0:
                valid = True
        elif prev_close != "N/A" and prev_close != 0 and price != "N/A":
            day_change = ((float(price) - float(prev_close))/float(prev_close))*100
            day_change = "{:.2f}".format(day_change)
            if day_change != 0:
                valid = True

        change_50day = 0
        if price != "N/A" and price != 0:
            if avg50day != "N/A" and avg50day > 0:
                change_50day = ((float(price) - float(avg50day))/float(avg50day))*100
            else:
                change_50day = 0

        if change_50day != 0:
            change_50day = "{:.2f}".format(change_50day)

        if volume != "N/A":
            if volume <= 50000:
                volume_text = volume
            elif 50000 < volume < 1000000:
                volume_text = str(round(volume / 1000, 2)) + "K"
            elif 1000000 <= volume < 1000000000:
                volume_text = str(round(volume / 1000000, 2)) + "M"
            else:
                volume_text = str(round(volume / 1000000000, 2)) + "B"
            valid = True
        else:
            volume = 0
            volume_text = ""

        if mkt_cap != "N/A":
            if mkt_cap < 1000000000:
                mkt_cap_text = str(round(mkt_cap / 1000000, 2)) + "M"
            elif 1000000000 <= mkt_cap < 1000000000000:
                mkt_cap_text = str(round(mkt_cap / 1000000000, 2)) + "B"
            else:
                mkt_cap_text = str(round(mkt_cap / 1000000000000, 2)) + "B"
            valid = True
        else:
            mkt_cap = 0
            mkt_cap_text = ""

        if stock_float != "N/A":
            stock_float = stock_float
            valid = True

        if beta != "N/A":
            beta = "{:.2f}".format(beta)
            valid = True

        # if the ticker has any valid column, and mkt_cap is in the range, append
        if valid and mkt_cap >= min_mkt_cap and volume >= min_vol:
            stat_list = [symbol, price, day_change, change_50day, volume_text, mkt_cap_text, stock_float, beta]
            processed_stats_table.append(stat_list)

    # construct dataframe
    columns = ['symbol', 'price', 'one_day_change_percent', 'fifty_day_change_percent', 'volume',
               'mkt_cap', 'floating_shares', 'beta']
    stats_df = pd.DataFrame(processed_stats_table, columns=columns)

    stats_df['floating_shares'] = stats_df['floating_shares'].str.replace(',', '')

    stats_df.set_index('symbol', inplace=True)

    return stats_df


def print_df(df, filename, writecsv, subreddit):
    df.reset_index(inplace=True)

    now = datetime.utcnow()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    df['date_updated'] = dt_string
    df['subreddit'] = subreddit

    cols_to_change = ["one_day_score", "recent", "previous", "rockets", "positive", "negative"]
    for col in cols_to_change:
        df[col] = df[col].astype(float)
    df['change'] = df['change'].apply(lambda x: round(x, 2))
    df['industry'] = df['industry'].str.replace("—", "-")

    # Save to sql database
    for row_num in range(len(df)):
        db.execute(
            "INSERT INTO {} VALUES "
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)".format(subreddit),
            tuple(df.loc[row_num].tolist()))
        conn.commit()
    print("Saved to {} SQL Database successfully.".format(subreddit))

    # save the file to the same dir as the AutoDD.py script
    completeName = os.path.join(sys.path[0], filename)

    if writecsv:
        completeName += '.csv'
        df.to_csv(completeName, index=False, float_format='%.2f', mode='a', encoding=locale.getpreferredencoding())
        print(file=open(completeName, "a"))

    else:
        completeName += '.txt'
        with open(completeName, "a") as file:
            file.write("date and time now = ")
            file.write(dt_string)
            file.write('\n')
            file.write(tabulate(df, headers='keys', floatfmt='.2f', showindex=False))
            file.write('\n\n')

    print("Wrote to file successfully {}".format(completeName))
