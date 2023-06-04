# Stocksera Developers Guide

There are 2 ways to run the tasks:
- Go to http://localhost:8000/tasks and click on the buttons
  - ![Tasks](../static/images/github/tasks.png)
- Through command prompt
  - <b>You should run all commands from the main parent directory</b>
  - Ensure that you run scheduled_tasks/create_database.py first.
      ```
      # Example of how you should run all the scheduled tasks
      example: (venv) C:\Users\Acer\Stocksera>py scheduled_tasks/economy/get_inflation.py
      ```
 
Before continuing, register for an API in the links shown below and add them in http://localhost:8000/tasks or in config.yaml.

| API Source       | URL                                                |
|------------------|----------------------------------------------------|
| Reddit           | https://www.reddit.com/prefs/apps                  |
| Twitter          | https://developer.twitter.com/en/portal/dashboard  |
| Finnhub          | https://finnhub.io/                                |
| Polygon          | https://polygon.io/                                |
| Gmail -optional  | https://realpython.com/python-send-email/          |

## Frequency to run tasks
- Do note that the frequency to run the files are for guidance only. You do not need to follow them strictly. Change according to your preference.

| Script Name                                               | Functions                               | Frequency   |
|-----------------------------------------------------------|-----------------------------------------|-------------|
| scheduled_tasks/reddit/stocks/scrape_trending_posts.py    | main()                                  | Daily (PM)  |
| scheduled_tasks/reddit/stocks/scrape_discussion_thread.py | wsb_live(), wsb_change(), get_mkt_cap() | 10 Mins     |
| scheduled_tasks/reddit/stocks/scrape_discussion_thread.py | update_hourly()                         | Hourly      |
| scheduled_tasks/reddit/crypto/scrape_trending_posts.py    | main()                                  | Daily (PM)  |
| scheduled_tasks/reddit/crypto/scrape_discussion_thread.py | crypto_live(), crypto_change()          | 10 Mins     |
| scheduled_tasks/reddit/crypto/scrape_discussion_thread.py | update_hourly()                         | Hourly      |
| scheduled_tasks/reddit/get_subreddit_count.py             | main()                                  | Daily (MH)  |
| scheduled_tasks/twitter/get_twitter_followers.py          | main()                                  | Daily       |
| scheduled_tasks/twitter/scrape_trending_posts.py          | main()                                  | Daily (MH)  |
| scheduled_tasks/economy/get_reverse_repo.py               | reverse_repo()                          | 1.30PM      |
| scheduled_tasks/economy/get_daily_treasury.py             | download_json()                         | 4.00PM      |
| scheduled_tasks/economy/get_inflation.py                  | inflation()                             | Monthly     |
| scheduled_tasks/economy/get_retail_sales.py               | retail_sales()                          | Monthly     |
| scheduled_tasks/economy/get_interest_rate.py              | interest_rate()                         | Monthly     |
| scheduled_tasks/economy/get_initial_jobless_claims.py     | jobless_claims()                        | Weekly      |
| scheduled_tasks/economy/get_upcoming_events_date.py       | main()                                  | 6.00PM      |
| scheduled_tasks/stocks/get_failure_to_deliver.py          | main()                                  | 2 Weeks     |
| scheduled_tasks/stocks/get_short_volume.py                | main()                                  | 6.00PM      | 
| scheduled_tasks/stocks/get_borrowed_shares.py             | main()                                  | 10 Mins     |
| scheduled_tasks/discover/miscellaneous.py                 | main()                                  | Daily (AH)  |
| scheduled_tasks/discover/get_earnings.py                  | main()                                  | Daily (AH)  |
| scheduled_tasks/discover/get_latest_insider_trading.py    | main()                                  | 2 Hours     |
| scheduled_tasks/discover/get_stocks_summary.py            | main()                                  | 10 Mins     |
| scheduled_tasks/discover/get_stocktwits_summary.py        | main()                                  | Hourly      |
| scheduled_tasks/discover/get_ipo_calendar.py              | main()                                  | Daily (AH)  |
| scheduled_tasks/discover/get_stock_splits.py              | main()                                  | Daily (AH)  |
| scheduled_tasks/discover/get_dividends.py                 | main()                                  | Daily (AH)  |
| scheduled_tasks/government/get_senate_trading.py          | main()                                  | Daily (AH)  |
| scheduled_tasks/government/get_house_trading.py           | main()                                  | Daily (AH)  |
| scheduled_tasks/news/get_news.py                          | main()                                  | 10 Mins     |
| scheduled_tasks/reset/reset_stocksera_trending.py         | reset_trending_db()                     | 30 Mins     |
