import math
from collections import Counter

import praw
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt

from helpers import *
import scheduled_tasks.reddit.config as cfg

client = CoinGeckoAPI()

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

# x base point of for a ticker that appears on a subreddit title or text body that fits the search criteria
base_points = 2

# every x upvotes on the thread counts for 1 point (rounded down)
upvote_factor = 3

# every x comments on the thread counts for 1 point (rounded down)
comments_factor = 3

# rocket emoji
rocket = '🚀'


def coinbase_coins():
    # List of crypto symbols interest in
    # We use symbols from coinbase instead as it is more concise than CoinGeckoAPI, which list ALL symbols (>1000)
    r = requests.get('https://api.pro.coinbase.com/currencies')
    crypto_dict = {}
    for coin in r.json():
        if coin['details']['type'] == 'crypto':
            crypto_dict[coin['id']] = {coin['id'].upper(), coin['name'].upper()}

    # Remove unwanted symbols
    del crypto_dict['KEEP']
    del crypto_dict['RLY']
    del crypto_dict['FORTH']
    del crypto_dict['FARM']
    del crypto_dict['MASK']
    del crypto_dict['OMG']
    return crypto_dict


def get_topics():
    # in case of duplicate key in dicts
    # latest dict overwrites previous dicts
    mapping_coins = {
        'ETH': {'ETH', 'ETHEREUM'},
        'XRP': {'XRP', 'RIPPLE'},
        'NEO': {'NEO'},
        'CEL': {'CEL', 'CELSIUS'},
        'XMR': {'MONERO', 'XMR'},
        'BNB': {'BNB', 'BINANCE COIN'},
        'NEM': {'XEM', 'NEM'},
        'TRON': {'TRX', 'TRON'},
        'BTG': {'GOLD', 'BTG'},
        'EOS': {'EOS', 'EOSIO'},
        'VET': {'VET', 'VECHAIN'},
        'DAI': {'DAI', 'MAKERDAO'},
        'SHIB': {'SHIBA', 'SHIB', 'SHIBA INU'},
        'IOTA': {'IOTA', 'MIOTA'},
        'LTO': {'LTO NETWORK', 'LTO'},
        'MOON': {'MOONS', 'MOON'},
        'THETA': {'THETA'},
        'KSM': {'KUSAMA', 'KSM'},
        'CAKE': {'PANCAKESWAP', 'PANCAKE', 'CAKE'},
        'KLAY': {'KLAYTN', 'KLAY'},
        'ERG': {'ERG', 'ERGO'}
    }
    return {**coinbase_coins(), **mapping_coins}


def get_submission_praw(n, sub):
    """
    Returns a list of results for submission in past:
    1st list: current result from n hours ago until now
    2nd list: prev result from 2n hours ago until n hours ago
    """
    mid_interval = datetime.today() - timedelta(hours=n)
    timestamp_mid = int(mid_interval.timestamp())
    timestamp_start = int((mid_interval - timedelta(hours=n)).timestamp())
    timestamp_end = int(datetime.today().timestamp())
    reddit = praw.Reddit(client_id=cfg.API_REDDIT_CLIENT_ID,
                         client_secret=cfg.API_REDDIT_CLIENT_SECRET,
                         user_agent=cfg.API_REDDIT_USER_AGENT)

    recent = {}
    subreddit = reddit.subreddit(sub)
    all_results = []
    count = 0
    for post in subreddit.new(limit=1000):
        print(count, ": ", datetime.fromtimestamp(post.created_utc), post.title)
        count += 1
        all_results.append([post.title, post.link_flair_text, post.selftext, post.score, post.num_comments,
                            post.created_utc])

    recent[sub] = [posts for posts in all_results if timestamp_mid <= posts[5] <= timestamp_end]
    return recent


def get_submission_generators(n, sub):
    """
    Returns dictionary of current scores, previous score, total score, upvote score and comment score
    """

    recent = get_submission_praw(n, sub)
    crypto_dict = get_topics()

    current_scores, current_rocket_scores, current_posts_dict, current_upvotes_dict, current_comments_dict = \
        get_ticker_scores_praw(recent, crypto_dict)

    total_rocket_score = Counter(current_rocket_scores)
    total_posts_score = Counter(current_posts_dict)
    total_upvotes_score = Counter(current_upvotes_dict)
    total_comments_score = Counter(current_comments_dict)

    return current_scores, total_rocket_score, total_posts_score, total_upvotes_score, total_comments_score


def get_ticker_scores_praw(sub_gen_dict, crypto_dict):
    # Dictionaries containing the summaries
    subreddit_scores_dict = {}

    # Dictionaries containing the rocket count
    rocket_scores_dict = {}
    num_posts_dict = {}
    num_upvotes_dict = {}
    num_comments_dict = {}

    for sub, submission_list in sub_gen_dict.items():
        subreddit_scores_dict[sub] = {}
        for submission in submission_list:
            # every ticker in the title will earn this base points
            increment = base_points

            extracted_tickers = set()
            title = submission[0]
            self_text = submission[2]
            for word in title.upper().split():
                for key, value in crypto_dict.items():
                    if word in value:
                        extracted_tickers.add(key)

            for word in self_text.upper().split():
                for key, value in crypto_dict.items():
                    if word in value:
                        extracted_tickers.add(key)

            # every 3 upvotes are worth 1 extra point
            if upvote_factor > 0 and submission[3] is not None:
                increment += math.ceil(submission[3] / upvote_factor)

            # every 2 comments are worth 1 extra point
            if comments_factor > 0 and submission[4] is not None:
                increment += math.ceil(submission[4] / comments_factor)

            count_rocket = title.count(rocket) + self_text.count(rocket)

            for ticker in extracted_tickers:
                rocket_scores_dict[ticker] = rocket_scores_dict.get(ticker, 0) + count_rocket
                num_posts_dict[ticker] = num_posts_dict.get(ticker, 0) + 1
                num_upvotes_dict[ticker] = num_upvotes_dict.get(ticker, 0) + submission[3]
                num_comments_dict[ticker] = num_comments_dict.get(ticker, 0) + submission[4]

                subreddit_scores_dict[sub][ticker] = subreddit_scores_dict[sub].get(ticker, 0) + increment
    return subreddit_scores_dict, rocket_scores_dict, num_posts_dict, num_upvotes_dict, num_comments_dict


def populate_df(current_scores_dict):
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


def get_financial_data(stats_table, crypto_id, symbol):
    try:
        market_data = client.get_coin_by_id(crypto_id)['market_data']
    except requests.exceptions.RequestException as e:
        print(e, "error")
        time.sleep(30)
        market_data = client.get_coin_by_id(crypto_id)['market_data']

    current_price = market_data["current_price"]["usd"]
    total_volume = long_number_format(market_data["total_volume"]["usd"])
    market_cap = long_number_format(market_data["market_cap"]["usd"])
    if str(market_cap) == "0":
        market_cap = "N/A"
    if market_data["price_change_percentage_24h"] is not None:
        price_change_percentage_24h = round(market_data["price_change_percentage_24h"], 2)
    else:
        price_change_percentage_24h = 0
    if market_data["price_change_percentage_30d"] is not None:
        price_change_percentage_30d = round(market_data["price_change_percentage_30d"], 2)
    else:
        price_change_percentage_30d = 0
    circulating_supply = long_number_format(market_data["circulating_supply"])
    if str(circulating_supply) == "0":
        circulating_supply = "N/A"
    max_supply = long_number_format(market_data["total_supply"])
    if str(max_supply) == "0":
        max_supply = "N/A"
    stats_table.append([symbol, current_price,
                        price_change_percentage_24h, price_change_percentage_30d,
                        total_volume, market_cap,
                        circulating_supply, max_supply])
    return stats_table


def get_graph_chart(crypto_id, symbol):
    try:
        prices = client.get_coin_market_chart_by_id(crypto_id, vs_currency="USD", days=30)
    except requests.exceptions.RequestException as e:
        print(e, "error")
        time.sleep(30)
        prices = client.get_coin_market_chart_by_id(crypto_id, vs_currency="USD", days=30)
    prices = prices["prices"]
    df = pd.DataFrame(data=prices, columns=["time", "price"]).iloc[::12, :]
    price_list = df["price"].to_list()
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
        plt.savefig(r"./static/graph_chart/crypto/{}.svg".format(symbol.upper()), transparent=True)
        plt.close()


def main():
    current_scores, total_rocket_score, total_posts_score, total_upvotes_score, total_comments_score = get_submission_generators(24, "cryptocurrency")
    results_df = populate_df(current_scores)
    results_df.insert(loc=4, column='rockets', value=pd.Series(total_rocket_score))
    results_df.insert(loc=5, column='posts', value=pd.Series(total_posts_score))
    results_df.insert(loc=6, column='upvotes', value=pd.Series(total_upvotes_score))
    results_df.insert(loc=7, column='comments', value=pd.Series(total_comments_score))

    # compares the first column, which is the total score to the min val
    results_df = results_df[results_df.iloc[:, 0] >= 10]

    ticker_list = list(results_df.index.values)
    stats_table = []

    try:
        coingecko_coin_list = client.get_coins_list()
    except requests.exceptions.RequestException as e:
        print("error", e)
        print("20 ")
        time.sleep(30)
        coingecko_coin_list = client.get_coins_list()

    print(len(ticker_list), "number of tickers")
    for index, symbol in enumerate(ticker_list):
        for i in coingecko_coin_list:
            if symbol.lower() == i["symbol"].lower():
                print(index, ": ", symbol)
                crypto_id = i['id']
                stats_table = get_financial_data(stats_table, crypto_id, symbol)

                # Only save graph for top 35 symbols
                if index < 35:
                    get_graph_chart(crypto_id, symbol)
                break

    stats_df = pd.DataFrame(stats_table, columns=["Symbol", "Price", "24H Change", "30D Change", "Volume", "Market Cap",
                                                  "Circulating Supply", "Max Supply"])
    stats_df.set_index('Symbol', inplace=True)
    results_df = pd.concat([results_df, stats_df], axis=1)

    db.execute("SELECT DISTINCT (date_updated) FROM cryptocurrency")
    dates = db.fetchall()

    db.execute("SELECT * FROM cryptocurrency WHERE date_updated LIKE '%{}%'".format(dates[-1][0].split()[0], ))
    prev = db.fetchall()

    for index, row in results_df.iterrows():
        symbol = index
        current_score = row[1]
        prev_score = 0
        for historical in prev:
            if historical[2] == symbol:
                prev_score = historical[4]
        total = current_score + prev_score
        if prev_score != 0:
            percent_change = round(((current_score / prev_score) - 1) * 100, 2)
        else:
            percent_change = 0
        results_df.at[index, 'total'] = total
        results_df.at[index, 'previous'] = prev_score
        results_df.at[index, 'change'] = percent_change

    results_df.index.name = 'ticker'
    results_df.sort_values(by=results_df.columns[0], inplace=True, ascending=False)
    results_df.reset_index(inplace=True)
    results_df.index += 1
    results_df.reset_index(inplace=True)

    results_df["change"] = results_df["change"].round(3)
    cols_to_change = ["index", "total", "recent", "previous", "change", "rockets", "posts", "upvotes", "comments"]
    for col in cols_to_change:
        results_df[col] = results_df[col].fillna(0).astype(float)
    results_df.replace(np.nan, "N/A", inplace=True)

    now = datetime.utcnow()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    results_df['date_updated'] = dt_string

    for row_num in range(len(results_df)):
        db.execute(
            "INSERT INTO cryptocurrency VALUES "
            "(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(results_df.loc[row_num].tolist()))
        conn.commit()
