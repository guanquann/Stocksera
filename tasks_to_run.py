"""
Compilation of scheduled tasks to run
"""

import sqlite3
import scheduled_tasks.create_database as create_database
import scheduled_tasks.get_reddit_trending_stocks.scrape_reddit as scrape_reddit
import scheduled_tasks.get_news_sentiment as get_news_sentiment
import scheduled_tasks.get_subreddit_count as get_subreddit_count
import scheduled_tasks.get_short_volume as get_short_volume
import scheduled_tasks.buy_trending_tickers as buy_trending_tickers
import scheduled_tasks.get_ticker_info as get_ticker_info
import scheduled_tasks.get_financial as get_financial
import scheduled_tasks.get_earnings_calendar as get_earnings_calendar
import scheduled_tasks.get_hedge_funds_holdings as get_hedge_funds_holdings
import scheduled_tasks.get_failure_to_deliver as get_failure_to_deliver
import scheduled_tasks.miscellaneous as miscellaneous

# Best to run 1 hour before market opens daily to get trending tickers and subreddit count
SCRAPE_REDDIT = True

# Update latest price of Reddit ETF. Run this WHEN MARKET OPENS to get latest price
UPDATE_REDDIT_ETF = False

# If you want to update the cached ticker info for faster processing time
TICKER_INFO = False

# IF you want to update the cached ticker financial data for faster processing time
TICKER_FINANCIAL = False

# If you want to get short volume of individual tickers
SHORT_VOL = False

# If you want to get news sentiment from Finviz
NEWS_SENTIMENT = True

# If you want to get tickers with low float
LOW_FLOAT = False

# If you want to get tickers with high short interest
SHORT_INT = False

# If you want to get upcoming earnings calendar
EARNINGS_CALENDAR = False

# If you want to update Failure to Deliver
FTD = False

# If you want to update hedge funds holdings
HEDGE_FUNDS = False

if __name__ == '__main__':
    # Create/update database. It is okay to run this even though you have an existing database.
    # Data will not be over-written.
    create_database.database()

    if SCRAPE_REDDIT:
        # Uncomment this if you want to get trending tickers on Reddit
        scrape_reddit.main()

        # Uncomment this if you want to get subreddit subscribers stats
        get_subreddit_count.subreddit_count()

    if UPDATE_REDDIT_ETF:
        conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
        db_date = db.fetchone()[0]
        buy_trending_tickers.buy_new_ticker(db_date)
        buy_trending_tickers.sell_ticker(db_date)
        buy_trending_tickers.update_bought_ticker_price()

    if TICKER_INFO:
        for i in get_ticker_info.full_ticker_list():
            get_ticker_info.ticker_info(i)

    if TICKER_FINANCIAL:
        for i in get_ticker_info.full_ticker_list():
            get_financial.financial(i)

    if SHORT_VOL:
        for i in get_short_volume.full_ticker_list():
            get_short_volume.short_volume(i)

    if NEWS_SENTIMENT:
        get_news_sentiment.news_sentiment()

    if LOW_FLOAT:
        miscellaneous.get_low_float()

    if SHORT_INT:
        miscellaneous.get_high_short_interest()

    if EARNINGS_CALENDAR:
        get_earnings_calendar.get_new_earnings(n_days=7)

    if FTD:
        # Uncomment this if there is not new FTD txt file from SEC
        # get_failure_to_deliver.update_all_tickers(ftd_txt_file_name="INSERT_FTD_TXT_FILE_PATH")

        for i in get_failure_to_deliver.full_ticker_list():
            get_failure_to_deliver.add_new_ticker(i)

    if HEDGE_FUNDS:
        get_hedge_funds_holdings.preprocess_hedge_funds(csv=r"C:\Users\Acer\Desktop\citadel_advisors_llc-current-2021-06-23_14_17_24.csv", fund_name="citadel")
