import scheduled_tasks.get_reddit_trending.scrape_reddit as scrape_reddit
import scheduled_tasks.get_news_sentiment as get_news_sentiment
import scheduled_tasks.get_subreddit_count as get_subreddit_count
import scheduled_tasks.miscellaneous as miscellaneous

if __name__ == '__main__':
    get_subreddit_count.subreddit_count()
    get_news_sentiment.news_sentiment()
    miscellaneous.get_low_float()
    miscellaneous.get_high_short_interest()
    scrape_reddit.main()
