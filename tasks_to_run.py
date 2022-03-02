"""
Compilation of scheduled tasks to run
"""

import os
import sqlite3
from pathlib import Path

import scheduled_tasks.create_database as create_database

import scheduled_tasks.reddit.stocks.scrape_trending_posts as scrape_reddit_stocks
import scheduled_tasks.reddit.stocks.scrape_discussion_thread as scrape_stocks_discussion_thread
import scheduled_tasks.reddit.crypto.scrape_trending_posts as scrape_reddit_crypto
import scheduled_tasks.reddit.crypto.scrape_discussion_thread as scrape_crypto_discussion_thread
import scheduled_tasks.reddit.get_subreddit_count as get_subreddit_count
import scheduled_tasks.reddit.buy_trending_tickers as buy_trending_tickers

import scheduled_tasks.twitter.get_twitter_followers as get_twitter_followers
import scheduled_tasks.twitter.scrape_trending_posts as scrape_twitter_posts

import scheduled_tasks.stocks.get_short_volume as get_short_volume
import scheduled_tasks.stocks.get_financial as get_financial
import scheduled_tasks.stocks.get_failure_to_deliver as get_failure_to_deliver
import scheduled_tasks.stocks.get_borrowed_shares as get_borrowed_shares

import scheduled_tasks.discover.get_latest_insider_trading as get_latest_insider_trading
import scheduled_tasks.discover.get_stocks_summary as get_stocks_summary
import scheduled_tasks.discover.get_ipo_calendar as get_ipo_calendar
import scheduled_tasks.discover.miscellaneous as miscellaneous
import scheduled_tasks.discover.get_stocktwits_trending as get_stocktwits_trending
import scheduled_tasks.discover.get_earnings_calendar as get_earnings_calendar

import scheduled_tasks.news.get_news as get_news

import scheduled_tasks.government.get_senate_trading as get_senate_trading
import scheduled_tasks.government.get_house_trading as get_house_trading

import scheduled_tasks.economy.get_reverse_repo as get_reverse_repo
import scheduled_tasks.economy.get_inflation as get_inflation
import scheduled_tasks.economy.get_daily_treasury as get_daily_treasury
import scheduled_tasks.economy.get_retail_sales as get_retail_sales
import scheduled_tasks.economy.get_initial_jobless_claims as get_initial_jobless_claims
import scheduled_tasks.economy.get_upcoming_events_date as get_upcoming_events_date

import scheduled_tasks.others.get_ticker_info as get_ticker_info

# Get real time trending tickers from WSB
SCRAPE_LIVE_WSB = True

# Get real time trending crypto from r/cryptocurrency
SCRAPE_LIVE_CRYPTO = True

# Get trending tickers/crypto POSTS in popular subreddits
SCRAPE_REDDIT_STOCKS_POSTS = True
SCRAPE_REDDIT_CRYPTO_POSTS = True

# Get subreddit count
SCRAPE_SUBREDDIT_COUNT = True

# Update latest price of Reddit ETF.
UPDATE_REDDIT_ETF_PRICE = True

# Update number of followers of company in Twitter
UPDATE_TWITTER_FOLLOWERS = True

# Get number of symbol tweets in Twitter in the last week
SCRAPE_TWEET_COUNTS = True

# Get trending tickers in Stocktwits
SCRAPE_STOCKTWITS_TRENDING = True

# Update the cached ticker info for faster processing time
TICKER_INFO = True

# Update the cached ticker financial data for faster processing time
TICKER_FINANCIAL = True

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

# Get senate trading
SENATE_TRADING = True

# Get house trading
HOUSE_TRADING = True

# Get IPO calendar
IPO_calendar = True

# Get reverse repo data
RRP = True

# Get inflation data
INFLATION = True

# Gget daily treasury data
TREASURY = True

# Compare retail sale vs covid cases
RETAIL_SALES = True

# Get initial jobless claims
INITIAL_JOBLESS_CLAIMS = True


if __name__ == '__main__':
    # Create/update database. It is okay to run this even though you have an existing database.
    create_database.database()

    if SCRAPE_LIVE_WSB:
        scrape_stocks_discussion_thread.wsb_live()
        scrape_stocks_discussion_thread.wsb_change()
        scrape_stocks_discussion_thread.get_mkt_cap()
        scrape_stocks_discussion_thread.update_hourly()

    if SCRAPE_LIVE_CRYPTO:
        scrape_crypto_discussion_thread.crypto_live()
        scrape_crypto_discussion_thread.crypto_change()
        scrape_crypto_discussion_thread.update_hourly()

    if SCRAPE_REDDIT_STOCKS_POSTS:
        scrape_reddit_stocks.main()

    if SCRAPE_REDDIT_CRYPTO_POSTS:
        scrape_reddit_crypto.main()

    if SCRAPE_SUBREDDIT_COUNT:
        get_subreddit_count.subreddit_count()

    if UPDATE_TWITTER_FOLLOWERS:
        get_twitter_followers.main()

    if SCRAPE_TWEET_COUNTS:
        scrape_twitter_posts.main()
    
    if SCRAPE_STOCKTWITS_TRENDING:
        get_stocktwits_trending.main()
    
    if UPDATE_REDDIT_ETF_PRICE:
        conn = sqlite3.connect(r"database/database.db", check_same_thread=True)
        db = conn.cursor()
        db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
        db_date = db.fetchone()[0]
        buy_trending_tickers.buy_new_ticker(db_date)
        buy_trending_tickers.sell_ticker(db_date)
        buy_trending_tickers.update_bought_ticker_price()

    if TICKER_INFO:
        get_ticker_info.ticker_info(get_ticker_info.full_ticker_list())

    if TICKER_FINANCIAL:
        for i in get_ticker_info.full_ticker_list():
            get_financial.financial(i)

    if SHORT_VOL:
        get_short_volume.main()

    if LOW_FLOAT:
        miscellaneous.get_low_float()

    if SHORT_INT:
        miscellaneous.get_high_short_interest()

    if EARNINGS_CALENDAR:
        get_earnings_calendar.insert_earnings_into_db(get_earnings_calendar.get_earnings(7, forward=True))
        get_earnings_calendar.update_previous_earnings(get_earnings_calendar.get_earnings(7, forward=True))
        get_earnings_calendar.delete_old_earnings(14)

    if LATEST_NEWS:
        get_news.main()
        get_news.main("crypto")
        get_news.main("forex")
        get_news.main("merger")

    if FTD:
        get_failure_to_deliver.download_ftd()
        FOLDER_PATH = r"/database/failure_to_deliver/csv"
        files_available = sorted(Path(FOLDER_PATH).iterdir(), key=os.path.getmtime)
        get_failure_to_deliver.upload_to_df(files_available)
        get_failure_to_deliver.get_top_ftd(files_available[0])

    if BORROWED_SHARES:
        get_borrowed_shares.main()

    if RRP:
        get_reverse_repo.reverse_repo()

    if LATEST_INSIDER_TRADING:
        get_latest_insider_trading.latest_insider_trading()

    if STOCKS_HEATMAP:
        get_stocks_summary.main()

    if SENATE_TRADING:
        get_senate_trading.senate_trades()

    if HOUSE_TRADING:
        get_house_trading.house_trades()

    if IPO_calendar:
        get_ipo_calendar.main()
    
    if INFLATION:
        get_inflation.usa_inflation()
        get_inflation.world_inflation()

    if TREASURY:
        get_daily_treasury.download_json()

    if RETAIL_SALES:
        get_retail_sales.retail_sales()

    if INITIAL_JOBLESS_CLAIMS:
        get_initial_jobless_claims.jobless_claims()

    get_upcoming_events_date.main()
