import locale
import yfinance.ticker as yf
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta

from scheduled_tasks.reddit.reddit_utils import *

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(json.load(open("custom_extensions/custom_words.json")))

# x base point of for a ticker that appears on a subreddit title or text body that fits the search criteria
base_points = 2

# x bonus points for each flair matching 'DD' or 'Catalyst' of for a ticker that appears on the subreddit
bonus_points = 2

# every x upvotes on the thread counts for 1 point (rounded down)
upvote_factor = 3

# every x comments on the thread counts for 1 point (rounded down)
comments_factor = 3

# x bonus points for the sentiment of ticker
positive_sentiment = 2
neutral_sentiment = 1
negative_sentiment = 0

# rocket emoji
rocket = '🚀'

# Python regex pattern for stocks codes
pattern = "(?<=\$)?\\b[A-Z]{2,5}\\b(?:\.[A-Z]{1,2})?"

# Create folder to store price chart
if not os.path.exists("static/graph_chart"):
    os.mkdir("static/graph_chart")
    os.mkdir("static/graph_chart/stocks")
    os.mkdir("static/graph_chart/crypto")


def get_sentiment(text, increment):
    vs = analyzer.polarity_scores(text)
    sentiment_score = vs['compound']
    if sentiment_score >= 0.05:
        increment += positive_sentiment
    elif sentiment_score <= -0.05:
        increment += negative_sentiment
    else:
        increment += neutral_sentiment
    return increment, sentiment_score


def get_submission_praw(n, sub, n_num):
    """
    Returns a list of results for submission in past:
    1st list: current result from n hours ago until now
    2nd list: prev result from 2n hours ago until n hours ago
    """
    mid_interval = datetime.today() - timedelta(hours=n)
    timestamp_mid = int(mid_interval.timestamp())
    timestamp_start = int((mid_interval - timedelta(hours=n)).timestamp())
    timestamp_end = int(datetime.today().timestamp())

    recent = {}
    prev = {}
    subreddit = reddit.subreddit(sub)
    all_results = []
    for post in subreddit.new(limit=n_num):
        all_results.append([post.title, post.link_flair_text, post.selftext, post.score, post.num_comments,
                            post.created_utc])

    # start --> mid --> end
    recent[sub] = [posts for posts in all_results if timestamp_mid <= posts[5] <= timestamp_end]
    prev[sub] = [posts for posts in all_results if timestamp_start <= posts[5] < timestamp_mid]
    return recent, prev


def get_submission_generators(n, sub, n_num):
    """
    Returns dictionary of current scores, previous score, total score, upvote score and comment score
    """

    recent, prev = get_submission_praw(n, sub, n_num)
    print("Searching for tickers in {}...".format(sub))

    current_scores, current_rocket_scores, current_posts_dict, current_upvotes_dict, current_comments_dict = get_ticker_scores_praw(recent)
    prev_scores, prev_rocket_scores, prev_posts_dict, prev_upvotes_dict, prev_comments_dict = get_ticker_scores_praw(prev)

    total_rocket_score = Counter(current_rocket_scores) + Counter(prev_rocket_scores)
    total_posts_score = Counter(current_posts_dict) + Counter(prev_posts_dict)
    total_upvotes_score = Counter(current_upvotes_dict) + Counter(prev_upvotes_dict)
    total_comments_score = Counter(current_comments_dict) + Counter(prev_comments_dict)

    return current_scores, prev_scores, total_rocket_score, total_posts_score, total_upvotes_score, total_comments_score


def get_ticker_scores_praw(sub_gen_dict):
    """
    Return two dictionaries:
    --sub_scores_dict: a dictionary of dictionaries. This dictionaries' keys are the requested subreddit: all subreddits
    if args.allsub is True, and just args.sub otherwise. The value paired with each subreddit key is a dictionary of
    scores, where each key is a ticker found in the reddit submissions.
    --rocket_scores_dict: a dictionary whose keys are the tickers found in reddit submissions, and value is the number
    of rocker emojis found for each ticker.
    :param sub_gen_dict: A dictionary of generators for each subreddit, as outputted by get_submission_generators
    """

    # Dictionaries containing the summaries
    sub_scores_dict = {}

    # Dictionaries containing the rocket count
    rocket_scores_dict = {}
    num_posts_dict = {}
    num_upvotes_dict = {}
    num_comments_dict = {}

    for sub, submission_list in sub_gen_dict.items():
        sub_scores_dict[sub] = {}
        for submission in submission_list:
            # every ticker in the title will earn this base points
            increment = base_points

            # search the title for the ticker/tickers
            title = ' ' + submission[0].upper() + ' '
            title_extracted = set(re.findall(pattern, title))
            # print(submission[5], title, title_extracted)
            # flair is worth bonus points
            if submission[1] is not None:
                flair = submission[1].lower()
                if 'dd' in flair or 'catalyst' in flair or 'technical analysis' in flair:
                    increment += bonus_points

            # search the text body for the ticker/tickers and find sentiment score
            self_text_extracted = set()
            if submission[2] is not None:
                self_text = ' ' + submission[2] + ' '
                self_text_extracted = set(re.findall(pattern, self_text))
                increment, sentiment_score = get_sentiment(self_text, increment)
            else:
                increment, sentiment_score = get_sentiment(title, increment)

            # every 3 upvotes are worth 1 extra point
            if upvote_factor > 0 and submission[3] is not None:
                increment += math.ceil(submission[3] / upvote_factor)

            # every 2 comments are worth 1 extra point
            if comments_factor > 0 and submission[4] is not None:
                increment += math.ceil(submission[4] / comments_factor)

            extracted_tickers = self_text_extracted.union(title_extracted)
            extracted_tickers = {ticker.replace('.', '-') for ticker in extracted_tickers}

            count_rocket = title.count(rocket) + self_text.count(rocket)

            for ticker in extracted_tickers:
                rocket_scores_dict[ticker] = rocket_scores_dict.get(ticker, 0) + count_rocket
                num_posts_dict[ticker] = num_posts_dict.get(ticker, 0) + 1
                num_upvotes_dict[ticker] = num_upvotes_dict.get(ticker, 0) + submission[3]
                num_comments_dict[ticker] = num_comments_dict.get(ticker, 0) + submission[4]

                # title_extracted is a set, duplicate tickers from the same title counted once only
                sub_scores_dict[sub][ticker] = sub_scores_dict[sub].get(ticker, 0) + increment

    return sub_scores_dict, rocket_scores_dict, num_posts_dict, num_upvotes_dict, num_comments_dict


def populate_df(current_scores_dict, prev_scores_dict, interval):
    """
    Combine two score dictionaries, one from the current time interval, and one from the past time interval
    :returns: the populated dataframe
    """
    dict_result = {}
    total_sub_scores = {}

    for sub, current_sub_scores_dict in current_scores_dict.items():
        total_sub_scores[sub] = {}
        for symbol, current_score in current_sub_scores_dict.items():
            if symbol in dict_result.keys():
                dict_result[symbol][0] += current_score
                dict_result[symbol][1] += current_score
            else:
                dict_result[symbol] = [current_score, current_score, 0, 0]
            total_sub_scores[sub][symbol] = total_sub_scores[sub].get(symbol, 0) + current_score

    for sub, prev_sub_scores_dict in prev_scores_dict.items():
        for symbol, prev_score in prev_sub_scores_dict.items():
            if symbol in dict_result.keys():
                # total, recent, prev, change
                dict_result[symbol][0] += prev_score
                dict_result[symbol][2] += prev_score
                dict_result[symbol][3] = ((dict_result[symbol][1] - dict_result[symbol][2]) / dict_result[symbol][2]) * 100
            else:
                dict_result[symbol] = [prev_score, 0, prev_score, 0]
            total_sub_scores[sub][symbol] = total_sub_scores[sub].get(symbol, 0) + prev_score

    columns = ['total', 'recent', 'previous', 'change']
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
    filtered_words = json.load(open("custom_extensions/stopwords.json"))["stopwords_list"]

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

        if volume != "N/A":
            if volume <= 50000:
                volume_text = volume
            elif 50000 < volume < 1000000:
                volume_text = str(round(volume / 1000, 2)) + "K"
            elif 1000000 <= volume < 1000000000:
                volume_text = str(round(volume / 1000000, 2)) + "M"
            else:
                volume_text = str(round(volume / 1000000000, 2)) + "T"
            valid = True
        else:
            volume = 0
            volume_text = ""

        if avg50day != "N/A":
            avg50day = round(avg50day, 2)

        if mkt_cap != "N/A":
            if mkt_cap < 1000000000:
                mkt_cap_text = str(round(mkt_cap / 1000000, 2)) + "M"
            elif 1000000000 <= mkt_cap < 1000000000000:
                mkt_cap_text = str(round(mkt_cap / 1000000000, 2)) + "B"
            else:
                mkt_cap_text = str(round(mkt_cap / 1000000000000, 2)) + "T"
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
            stat_list = [symbol, price, day_change, avg50day, volume_text, mkt_cap_text, stock_float, beta]
            processed_stats_table.append(stat_list)

    # construct dataframe
    columns = ['symbol', 'price', 'one_day_change_percent', 'fifty_day_change_percent', 'volume',
               'mkt_cap', 'floating_shares', 'beta']
    stats_df = pd.DataFrame(processed_stats_table, columns=columns)

    stats_df['floating_shares'] = stats_df['floating_shares'].str.replace(',', '')

    stats_df.set_index('symbol', inplace=True)

    return stats_df


def print_df(df, filename, writesql, writecsv, subreddit):
    df.reset_index(inplace=True)
    df.index += 1
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'rank'}, inplace=True)
    now = datetime.utcnow()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    df['date_updated'] = dt_string
    df['subreddit'] = subreddit

    cols_to_change = ["rank", "total", "recent", "previous", "rockets", "posts", "upvotes", "comments"]
    for col in cols_to_change:
        df[col] = df[col].fillna(0).astype(float)
    df['change'] = df['change'].apply(lambda x: round(x, 2))
    df['change'] = df['change'].replace(0, "N/A")
    df['industry'] = df['industry'].str.replace("—", "-")
    df['recommend'] = df['recommend'].str.replace("_", " ")

    # Save to sql database
    if writesql:
        cur.executemany(
            "INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(subreddit),
            df.values.tolist())
        cnx.commit()
        print("Saved to {} SQL Database successfully.".format(subreddit))

    # Write to csv
    if writecsv:
        completeName = os.path.join(sys.path[0], filename)
        completeName += '.csv'
        df.to_csv(completeName, index=False, float_format='%.2f', mode='a', encoding=locale.getpreferredencoding())
        print("Wrote to file successfully {}".format(completeName))

    # Create past 1 month chart
    print("Saving last 1 month chart now...")
    chart_path = r"static/graph_chart/stocks"
    top_35 = df[:35]
    for index, i in top_35.iterrows():
        trending_ticker = i[1]
        ticker = yf.Ticker(trending_ticker)
        price_df = ticker.history(interval="1d", period="1mo")["Close"]

        price_list = price_df.to_list()
        if price_list:
            start_price = price_list[0]
            end_price = price_list[-1]
            if start_price > end_price:
                color = "red"
            else:
                color = "green"
            days_list = [i for i in range(len(price_list))]

            plt.figure(figsize=(1, 0.5))
            plt.axis("off")
            plt.xticks([])
            plt.yticks([])

            plt.plot(days_list, price_list, color=color)
            plt.savefig(os.path.join(chart_path, r"{}.svg".format(trending_ticker)), transparent=True)
            plt.close()

    # Remove old charts
    to_delete_date = datetime.utcnow().date() - timedelta(days=15)
    for img_name in os.listdir(chart_path):
        img_last_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(chart_path, img_name))).date()
        if img_last_modified <= to_delete_date:
            os.remove(os.path.join(chart_path, img_name))
