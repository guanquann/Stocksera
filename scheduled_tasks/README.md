# StocksEra

### Scheduled Tasks

#### scheduled_tasks/main.py
- Compilation of all tasks that are needed to be completed before market open

#### scheduled_tasks/get_reddit_trending_stocks/scrape_reddit.py
- Script to scrape trending tickers in Reddit (r/wallstreetbets, r/StockMarket, r/stocks)
- Additional information (beta, volume, industry, recommendation etc) of the ticker will be extracted from yahoo finance too
- Edit your config in scheduled_tasks/config.py. Make sure you have you PRAW API key first.
- Extension of [https://github.com/kaito1410/AutoDD_Rev2](https://github.com/kaito1410/AutoDD_Rev2)

#### scheduled_tasks/get_subreddit_count.py
- Script to get total number of users and active users in popular subreddits on Reddit.
- Shows the growth in new users over time and proportion active users.

#### scheduled_tasks/get_subreddit_count.py