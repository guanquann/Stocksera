"""
Compilation of scheduled tasks to run
"""

import os
from pathlib import Path

import scheduled_tasks.create_database as create_database

import scheduled_tasks.reddit.stocks.scrape_trending_posts as scrape_reddit_stocks
import scheduled_tasks.reddit.stocks.scrape_discussion_thread as scrape_stocks_discussion_thread
import scheduled_tasks.reddit.crypto.scrape_trending_posts as scrape_reddit_crypto
import scheduled_tasks.reddit.crypto.scrape_discussion_thread as scrape_crypto_discussion_thread
import scheduled_tasks.reddit.get_subreddit_count as get_subreddit_count

import scheduled_tasks.twitter.get_twitter_followers as get_twitter_followers
import scheduled_tasks.twitter.scrape_trending_posts as scrape_twitter_posts

import scheduled_tasks.stocks.get_short_volume as get_short_volume
import scheduled_tasks.stocks.get_failure_to_deliver as get_failure_to_deliver
import scheduled_tasks.stocks.get_borrowed_shares as get_borrowed_shares

import scheduled_tasks.discover.get_latest_insider_trading as get_latest_insider_trading
import scheduled_tasks.discover.get_stocks_summary as get_stocks_summary
import scheduled_tasks.discover.get_ipo_calendar as get_ipo_calendar
import scheduled_tasks.discover.miscellaneous as miscellaneous
import scheduled_tasks.discover.get_stocktwits_trending as get_stocktwits_trending
import scheduled_tasks.discover.get_earnings as get_earnings

import scheduled_tasks.news.get_news as get_news

import scheduled_tasks.government.get_senate_trading as get_senate_trading
import scheduled_tasks.government.get_house_trading as get_house_trading

import scheduled_tasks.economy.get_reverse_repo as get_reverse_repo
import scheduled_tasks.economy.get_inflation as get_inflation
import scheduled_tasks.economy.get_daily_treasury as get_daily_treasury
import scheduled_tasks.economy.get_retail_sales as get_retail_sales
import scheduled_tasks.economy.get_interest_rate as get_interest_rate
import scheduled_tasks.economy.get_initial_jobless_claims as get_initial_jobless_claims
import scheduled_tasks.economy.get_upcoming_events_date as get_upcoming_events_date

# Get real time trending tickers from WSB
SCRAPE_LIVE_WSB = True

# Get real time trending crypto from r/cryptocurrency
SCRAPE_LIVE_CRYPTO = True

# Get trending tickers/crypto POSTS in popular subreddits
SCRAPE_REDDIT_POSTS = True

# Get subreddit count
SCRAPE_SUBREDDIT_COUNT = True

# Update number of followers of company in Twitter
UPDATE_TWITTER_FOLLOWERS = True

# Get number of symbol tweets in Twitter in the last week
SCRAPE_TWEET_COUNTS = True

# Get trending tickers in Stocktwits
SCRAPE_STOCKTWITS_TRENDING = True

# Get short volume of individual tickers
SHORT_VOL = True

# If you want to get tickers with low float
LOW_FLOAT = True

# Get tickers with high short interest
SHORT_INT = True

# Get upcoming earnings calendar
EARNINGS_CALENDAR = True

# Get breaking, crypto, forex, merger news
LATEST_NEWS = True

# Update Failure to Deliver
FTD = True

# Get borrowed shares
BORROWED_SHARES = True

# Get latest insider trading from Finviz
LATEST_INSIDER_TRADING = True

# Get stocks summary (heat map)
STOCKS_HEATMAP = True

# Get senate and house trading
GOVT_TRADING = True

# Get IPO calendar
IPO_calendar = True

# Get reverse repo data
RRP = True

# Get inflation data
INFLATION = True

# Get daily treasury data
TREASURY = True

# Compare retail sale vs covid cases
RETAIL_SALES = True

# FED Reserve Interest rate
INTEREST_RATE = True

# Get initial jobless claims
INITIAL_JOBLESS_CLAIMS = True


def wsb_trending():
    scrape_stocks_discussion_thread.wsb_live()
    scrape_stocks_discussion_thread.wsb_change()
    scrape_stocks_discussion_thread.get_mkt_cap()
    scrape_stocks_discussion_thread.update_hourly()


def crypto_trending():
    scrape_crypto_discussion_thread.crypto_live()
    scrape_crypto_discussion_thread.crypto_change()
    scrape_crypto_discussion_thread.update_hourly()


def reddit_trending():
    scrape_reddit_stocks.main()
    scrape_reddit_crypto.main()


def subreddit_trending():
    get_subreddit_count.subreddit_count()


def twitter_followers():
    get_twitter_followers.main()


def twitter_stock_trending():
    scrape_twitter_posts.main()


def stocktwits_trending():
    get_stocktwits_trending.main()


def short_vol():
    get_short_volume.main()


def low_float():
    miscellaneous.get_low_float()


def short_int():
    miscellaneous.get_high_short_interest()


def earning_calendar():
    get_earnings.main()


def latest_news():
    get_news.main()
    get_news.main("crypto")
    get_news.main("forex")
    get_news.main("merger")


def ftd():
    get_failure_to_deliver.download_ftd()
    FOLDER_PATH = r"/database/failure_to_deliver/csv"
    files_available = sorted(Path(FOLDER_PATH).iterdir(), key=os.path.getmtime)
    get_failure_to_deliver.upload_to_df(files_available)
    get_failure_to_deliver.get_top_ftd(files_available[0])


def ctb():
    get_borrowed_shares.main()


def insider_trading():
    get_latest_insider_trading.main()


def heatmap():
    get_stocks_summary.main()


def govt_trading():
    get_senate_trading.senate_trades()
    get_house_trading.house_trades()


def ipo():
    get_ipo_calendar.main()


def rrp():
    get_reverse_repo.reverse_repo()


def inflation():
    get_inflation.usa_inflation()
    get_inflation.world_inflation()


def treasury():
    get_daily_treasury.download_json()


def retail():
    get_retail_sales.retail_sales()


def interest_rate():
    get_interest_rate.interest_rate()


def initial_jobless_claims():
    get_initial_jobless_claims.jobless_claims()


def upcoming_economic_dates():
    get_upcoming_events_date.main()


if __name__ == '__main__':
    create_database.database()

    if SCRAPE_LIVE_WSB:
        wsb_trending()

    if SCRAPE_LIVE_CRYPTO:
        crypto_trending()

    if SCRAPE_REDDIT_POSTS:
        reddit_trending()

    if SCRAPE_SUBREDDIT_COUNT:
        subreddit_trending()

    if UPDATE_TWITTER_FOLLOWERS:
        twitter_followers()

    if SCRAPE_TWEET_COUNTS:
        twitter_stock_trending()

    if SCRAPE_STOCKTWITS_TRENDING:
        stocktwits_trending()

    if SHORT_VOL:
        short_vol()

    if LOW_FLOAT:
        low_float()

    if SHORT_INT:
        short_int()

    if EARNINGS_CALENDAR:
        earning_calendar()

    if LATEST_NEWS:
        latest_news()

    if FTD:
        ftd()

    if BORROWED_SHARES:
        ctb()

    if RRP:
        rrp()

    if LATEST_INSIDER_TRADING:
        insider_trading()

    if STOCKS_HEATMAP:
        heatmap()

    if GOVT_TRADING:
        govt_trading()

    if IPO_calendar:
        ipo()

    if INFLATION:
        inflation()

    if TREASURY:
        treasury()

    if RETAIL_SALES:
        retail()

    if INTEREST_RATE:
        interest_rate()

    if INITIAL_JOBLESS_CLAIMS:
        initial_jobless_claims()

    upcoming_economic_dates()
