"""
Compilation of scheduled tasks to run
"""
import scheduled_tasks.create_database as create_database

import scheduled_tasks.reddit.stocks.scrape_discussion_thread as scrape_stocks_discussion_thread
import scheduled_tasks.reddit.crypto.scrape_discussion_thread as scrape_crypto_discussion_thread
import scheduled_tasks.reddit.get_subreddit_count as get_subreddit_count

import scheduled_tasks.twitter.get_twitter_followers as get_twitter_followers
import scheduled_tasks.twitter.scrape_trending_posts as scrape_twitter_posts

import scheduled_tasks.stocks.get_short_volume as get_short_volume
import scheduled_tasks.stocks.get_failure_to_deliver as get_failure_to_deliver
import scheduled_tasks.stocks.get_borrowed_shares as get_borrowed_shares
import scheduled_tasks.stocks.get_threshold_securities as get_threshold_securities

import scheduled_tasks.discover.get_latest_insider_trading as get_latest_insider_trading
import scheduled_tasks.discover.get_stocks_summary as get_stocks_summary
import scheduled_tasks.discover.get_ipo_calendar as get_ipo_calendar
import scheduled_tasks.discover.miscellaneous as miscellaneous
import scheduled_tasks.discover.get_stocktwits_trending as get_stocktwits_trending
import scheduled_tasks.discover.get_dividends as get_dividends
import scheduled_tasks.discover.get_earnings as get_earnings
import scheduled_tasks.discover.get_stock_splits as get_stock_splits
import scheduled_tasks.discover.get_largest_companies as get_largest_companies
import scheduled_tasks.discover.get_fear_and_greed as get_fear_and_greed

import scheduled_tasks.news.get_news as get_news
import scheduled_tasks.news.get_trading_halts as get_trading_halts

import scheduled_tasks.government.get_senate_trading as get_senate_trading
import scheduled_tasks.government.get_house_trading as get_house_trading

import scheduled_tasks.economy.get_reverse_repo as get_reverse_repo
import scheduled_tasks.economy.get_inflation as get_inflation
import scheduled_tasks.economy.get_daily_treasury as get_daily_treasury
import scheduled_tasks.economy.get_retail_sales as get_retail_sales
import scheduled_tasks.economy.get_interest_rate as get_interest_rate
import scheduled_tasks.economy.get_initial_jobless_claims as get_initial_jobless_claims
import scheduled_tasks.economy.get_upcoming_events_date as get_upcoming_events_date


def task_create_db():
    create_database.database()


def task_wsb_trending():
    scrape_stocks_discussion_thread.main()


def task_crypto_trending():
    scrape_crypto_discussion_thread.main()


def task_subreddit_trending():
    get_subreddit_count.main()


def task_twitter_followers():
    get_twitter_followers.main()


def task_twitter_stock_trending():
    scrape_twitter_posts.main()


def task_stocktwits_trending():
    get_stocktwits_trending.main()


def task_short_vol():
    get_short_volume.main()


def task_low_float():
    miscellaneous.get_low_float()


def task_short_int():
    miscellaneous.get_high_short_interest()


def task_dividends():
    get_dividends.main()


def task_earning_calendar():
    get_earnings.main()


def task_stock_split():
    get_stock_splits.main()


def task_largest_companies():
    get_largest_companies.main()


def task_fear_and_greed():
    get_fear_and_greed.main()


def task_latest_news():
    get_news.main()


def task_trading_halt():
    get_trading_halts.main()


def task_ftd():
    get_failure_to_deliver.main()


def task_ctb():
    get_borrowed_shares.main()


def task_threshold_sec():
    get_threshold_securities.main()


def task_insider_trading():
    get_latest_insider_trading.main()


def task_heatmap():
    get_stocks_summary.main()


def task_govt_trading():
    get_senate_trading.senate_trades()
    get_house_trading.house_trades()


def task_ipo():
    get_ipo_calendar.main()


def task_rrp():
    get_reverse_repo.reverse_repo()


def task_inflation():
    get_inflation.main()


def task_treasury():
    get_daily_treasury.download_json()


def task_retail():
    get_retail_sales.retail_sales()


def task_interest_rate():
    get_interest_rate.interest_rate()


def task_initial_jobless_claims():
    get_initial_jobless_claims.jobless_claims()


def task_upcoming_economic_dates():
    get_upcoming_events_date.main()
