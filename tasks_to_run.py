"""
Compilation of scheduled tasks to run
"""

import scheduled_tasks.create_database
import scheduled_tasks.get_reddit_trending_stocks.scrape_reddit as scrape_reddit
import scheduled_tasks.get_news_sentiment as get_news_sentiment
import scheduled_tasks.get_subreddit_count as get_subreddit_count
import scheduled_tasks.get_short_volume as get_short_volume
import scheduled_tasks.buy_trending_tickers as buy_trending_tickers
import scheduled_tasks.get_ticker_info as get_ticker_info
import scheduled_tasks.get_earnings_calendar as get_earnings_calendar
import scheduled_tasks.miscellaneous as miscellaneous

# Best to run 1 hour before market opens daily to get trending tickers and subreddit count
SCRAPE_REDDIT = True

# Update latest price of Reddit ETF. Run this WHEN MARKET OPENS to get latest price
UPDATE_REDDIT_ETF = True

# If you want to get news sentiment from Finviz
NEWS_SENTIMENT = True

# If you want to get short volume of individual tickers
SHORT_VOL = False

# If you want to update the cached ticker info for faster processing time
TICKER_INFO = False

# If you want to get tickers with low float
LOW_FLOAT = False

# If you want to get tickers with high short interest
SHORT_INT = False

# If you want to get upcoming earnings calendar
EARNINGS_CALENDAR = False

if __name__ == '__main__':
    if SCRAPE_REDDIT:
        # Uncomment this if you want to get trending tickers on Reddit
        scrape_reddit.main()

        # Uncomment this if you want to get subreddit subscribers stats
        get_subreddit_count.subreddit_count()

    if TICKER_INFO:
        for i in get_ticker_info.full_ticker_list():
            get_ticker_info.ticker_info(i)

    if NEWS_SENTIMENT:
        get_news_sentiment.news_sentiment()

    if SHORT_VOL:
        for i in get_short_volume.full_ticker_list():
            get_short_volume.short_volume(i)

    if UPDATE_REDDIT_ETF:
        buy_trending_tickers.update_bought_ticker_price()

    if LOW_FLOAT:
        miscellaneous.get_low_float()

    if SHORT_INT:
        miscellaneous.get_high_short_interest()

    if EARNINGS_CALENDAR:
        get_earnings_calendar.get_new_earnings(n_days=7)
