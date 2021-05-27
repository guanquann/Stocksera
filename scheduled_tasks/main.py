import sqlite3
import scheduled_tasks.get_reddit_trending_stocks.scrape_reddit as scrape_reddit
import scheduled_tasks.get_news_sentiment as get_news_sentiment
import scheduled_tasks.get_subreddit_count as get_subreddit_count
import scheduled_tasks.buy_trending_tickers as buy_trending_tickers
import scheduled_tasks.miscellaneous as miscellaneous

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

if __name__ == '__main__':
    # get_subreddit_count.subreddit_count()
    # get_news_sentiment.news_sentiment()
    # miscellaneous.get_low_float()
    # miscellaneous.get_high_short_interest()

    scrape_reddit.main()
    # db.execute("SELECT date_updated FROM wallstreetbets ORDER BY ID DESC LIMIT 1")
    # db_date = db.fetchone()[0]
    # buy_trending_tickers.buy_new_ticker(db_date)
    # buy_trending_tickers.sell_ticker(db_date)
