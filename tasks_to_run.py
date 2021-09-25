"""
Compilation of scheduled tasks to run
"""

import os
import sqlite3
from pathlib import Path
import scheduled_tasks.create_database as create_database
import scheduled_tasks.reddit.get_reddit_trending_stocks.scrape_reddit as scrape_reddit_stocks
import scheduled_tasks.reddit.get_reddit_trending_crypto as scrape_reddit_crypto
import scheduled_tasks.reddit.get_subreddit_count as get_subreddit_count
import scheduled_tasks.reddit.buy_trending_tickers as buy_trending_tickers
import scheduled_tasks.get_twitter_followers as get_twitter_followers
import scheduled_tasks.get_short_volume as get_short_volume
import scheduled_tasks.get_ticker_info as get_ticker_info
import scheduled_tasks.reset_options_cache as reset_options_cache
import scheduled_tasks.get_financial as get_financial
import scheduled_tasks.get_earnings_calendar as get_earnings_calendar
import scheduled_tasks.get_failure_to_deliver as get_failure_to_deliver
import scheduled_tasks.get_latest_insider_trading as get_latest_insider_trading
import scheduled_tasks.miscellaneous as miscellaneous
import scheduled_tasks.economy.get_reverse_repo as get_reverse_repo
import scheduled_tasks.economy.get_inflation as get_inflation
import scheduled_tasks.economy.get_daily_treasury as get_daily_treasury
import scheduled_tasks.economy.get_retail_sales as get_retail_sales
import scheduled_tasks.economy.get_upcoming_events_date as get_upcoming_events_date

# Best to run 1 hour before market opens daily to get trending tickers and subreddit count
SCRAPE_REDDIT_STOCKS = True
SCRAPE_REDDIT_CRYPTO = True
SCRAPE_SUBREDDIT_STATS = True

# Update latest price of Reddit ETF. Run this WHEN MARKET OPENS to get latest price
UPDATE_REDDIT_ETF = True

# Update number of followers of company in Twitter
UPDATE_TWITTER = True

# If you want to update the cached ticker info for faster processing time
TICKER_INFO = True

# If you want to remove old dates in options data
RESET_TICKER_OPTIONS = True

# IF you want to update the cached ticker financial data for faster processing time
TICKER_FINANCIAL = False

# If you want to get short volume of individual tickers
SHORT_VOL = False

# If you want to get tickers with low float
LOW_FLOAT = True

# If you want to get tickers with high short interest
SHORT_INT = True

# If you want to get upcoming earnings calendar
EARNINGS_CALENDAR = False

# If you want to update Failure to Deliver
FTD = False

# Get latest insider trading from Finviz
LATEST_INSIDER_TRADING = False

# If you want to get reverse repo data
RRP = False

# If you want to get inflation data
INFLATION = False

# If you want to get daily treasury data
TREASURY = False

# If you want to compare retail sale vs covid cases
RETAIL_SALES = False


if __name__ == '__main__':
    # Create/update database. It is okay to run this even though you have an existing database.
    # Data will not be over-written.
    create_database.database()

    if SCRAPE_REDDIT_STOCKS:
        scrape_reddit_stocks.main()

    if SCRAPE_REDDIT_CRYPTO:
        scrape_reddit_crypto.main()

    if SCRAPE_SUBREDDIT_STATS:
        get_subreddit_count.subreddit_count()

    if UPDATE_TWITTER:
        get_twitter_followers.main()

    if UPDATE_REDDIT_ETF:
        conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
        db_date = db.fetchone()[0]
        buy_trending_tickers.buy_new_ticker(db_date)
        buy_trending_tickers.sell_ticker(db_date)
        buy_trending_tickers.update_bought_ticker_price()

    if TICKER_INFO:
        get_ticker_info.ticker_info(get_ticker_info.full_ticker_list())

    if RESET_TICKER_OPTIONS:
        reset_options_cache.reset_options()

    if TICKER_FINANCIAL:
        for i in get_ticker_info.full_ticker_list():
            get_financial.financial(i)

    if SHORT_VOL:
        get_short_volume.get_30d_data_finra()
        get_short_volume.get_daily_data_finra()

    if LOW_FLOAT:
        miscellaneous.get_low_float()

    if SHORT_INT:
        miscellaneous.get_high_short_interest()

    if EARNINGS_CALENDAR:
        get_earnings_calendar.insert_earnings_into_db(get_earnings_calendar.get_earnings(7, forward=True))

    if FTD:
        get_failure_to_deliver.download_ftd()
        FOLDER_PATH = r"C:\Users\Acer\PycharmProjects\StocksAnalysis\database\failure_to_deliver\csv"
        get_failure_to_deliver.combine_df(folder_path=FOLDER_PATH)
        get_failure_to_deliver.get_top_ftd(sorted(Path(FOLDER_PATH).iterdir(), key=os.path.getmtime)[0])

    if RRP:
        get_reverse_repo.reverse_repo()

    if LATEST_INSIDER_TRADING:
        get_latest_insider_trading.latest_insider_trading()

    if INFLATION:
        get_inflation.inflation()

    if TREASURY:
        get_daily_treasury.download_json()

    if RETAIL_SALES:
        get_retail_sales.retail_sales()

    get_upcoming_events_date.main()
