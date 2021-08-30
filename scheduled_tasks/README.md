# StocksEra Developers Guide

### Scheduled Tasks to run 

<b>You should run all commands from the main parent directory</b>
```
# Example of how you should run all the scheduled tasks
example: (venv) C:\Users\Acer\Stocksera>py tasks_to_run.py
example: (venv) C:\Users\Acer\Stocksera>py scheduled_tasks/get_financial.py
```

Alternatively, you can refer to Stocksera/tasks_to_run.py to run everything at once.

Ensure that you run scheduled_tasks/create_database.py first.
 
Before continuing, register for an API in the links shown below.

| API Source     | URL                                                 | Directory                                |
| -------------- |---------------------------------------------------- | ---------------------------------------- |
| Reddit         | https://www.reddit.com/prefs/apps                   | scheduled_tasks/reddit/config.py         |
| Twitter        | https://developer.twitter.com/en/portal/dashboard   | scheduled_tasks/get_twitter_followers.py |

You can view a sample of the database in <a href="https://drive.google.com/drive/folders/1qR7ssxnNzOUuvYCWR-kEajyoRoGKjbcT?usp=sharing">this</a> Google Drive link.
- Transfer graph_chart folder to static directory
- Transfer database folder to the main parent directory

#### scheduled_tasks/reddit/get_reddit_trending_stocks/scrape_reddit.py
- Script to scrape trending tickers in Reddit (r/wallstreetbets, r/StockMarket, r/stocks, r/options, r/pennystocks, r/investing).
- Additional information (beta, volume, industry, recommendation etc) of the ticker will be extracted from yahoo finance too.
- Edit your config in scheduled_tasks/config.py. Make sure you have you PRAW API key first.
- Extension of [https://github.com/kaito1410/AutoDD_Rev2](https://github.com/kaito1410/AutoDD_Rev2)

#### scheduled_tasks/reddit/get_reddit_trending_crypto.py
- Script to scrape trending crypto in Reddit (r/CryptoCurrenncy)
- Additional information (circulating supply, max suply etc) will be extracted from CoinGeckoAPI

#### scheduled_tasks/reddit/get_subreddit_count.py
- Script to get total number of users and active users in popular subreddits on Reddit.
- Shows the growth in new users over time and proportion active users.

#### scheduled_tasks/reddit/buy_trending_ticker.py
- Script that buys/sells tickers based on r/wallstreetbets sentiment.
- Update prices of tickers in custom ETF.
- Best to run this script the moment market opens.

#### scheduled_tasks/get_twitter_followers.py
- Get number of followers of business accounts in Twitter.

#### scheduled_tasks/get_popular_tickers.py
- To add a new ticker, add it to list_of_tickers list in full_ticker_list().

#### scheduled_tasks/get_ticker_info.py
- Get ticker information to cache data in order to speed up rendering time

#### scheduled_tasks/get_short_volume.py
- Get short volume of tickers you are interested in.
- Best to run this daily to identify the trending of short volume over time.

#### scheduled_tasks/get_news_sentiment.py
- Get news sentiment of ticker you are interested in.
- Best to run this daily to identify the trending of news sentiment over time.

#### scheduled_tasks/government/get_reverse_repo.py
- Get reverse repo transaction

#### scheduled_tasks/government/get_daily_treasury.py
- Get daily treasury

#### scheduled_tasks/government/get_inflation.py
- Get monthly inflation

#### scheduled_tasks/government/get_retail_sales.py
- Get monthly retail sales and compare it with the number of Covid-19 cases

#### scheduled_tasks/get_financial.py
- Get financial data for companies.

#### scheduled_tasks/miscellaneous.py
- Get stocks with low float and high short interest.

#### scheduled_tasks/get_failure_to_deliver.py
- Get Failure to Deliver data from [SEC](https://www.sec.gov/data/foiadocsfailsdatahtm).
- Download the txt file. You do not need to convert it to csv. The script automatically does it for you.
- Run this script once every few weeks.

#### scheduled_tasks/get_hedge_funds_holdings.py
- Get holdings of major hedge funds
- Download csv from [whalewisdom](https://whalewisdom.com/). You need to sign up a free account to access the csv files. Data is updated quarterly.
![Get hedge funds instructions](../static/images/github/get_hedge_funds_instructions.png)
