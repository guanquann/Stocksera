import sqlite3
import scheduled_tasks.get_reddit_trending_stocks.scrape_reddit as scrape_reddit
import scheduled_tasks.get_news_sentiment as get_news_sentiment
import scheduled_tasks.get_subreddit_count as get_subreddit_count
import scheduled_tasks.get_short_volume as get_short_volume
import scheduled_tasks.buy_trending_tickers as buy_trending_tickers
import scheduled_tasks.miscellaneous as miscellaneous

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

if __name__ == '__main__':
    # Uncomment this if you want to get trending tickers on Reddit
    scrape_reddit.main()

    # Uncomment this if you want to get subreddit subscribers stats
    get_subreddit_count.subreddit_count()

    # Uncomment this if you want to get news sentiment from Finviz
    get_news_sentiment.news_sentiment()

    # Uncomment this if you want to get short volume of tickers
    # for i in get_short_volume.full_ticker_list():
    #     get_short_volume.short_volume(i)

    # Uncomment this if you want to update price of Reddit ETF
    buy_trending_tickers.update_bought_ticker_price()

    # Uncomment this if you want to get tickers with low float
    # miscellaneous.get_low_float()

    # Uncomment this if you want to get tickers with high short interest
    # miscellaneous.get_high_short_interest()
