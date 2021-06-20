# StocksEra

You can view the application in <a href="https://stocksera.pythonanywhere.com">https://stocksera.pythonanywhere.com </a>

### User Guide

#### /ticker/
- View graph/historical data of your favourite ticker.
- Gather key statistics such as EPS, beta and SMA.
- Proportion of stocks held by major holders and major institutions.
- Google trending.
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>
![Ticker Stats](./static/images/ticker_main.png)

#### /ticker/options/
- View options chain of your favourite ticker. Inspired from <a href="https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal">Gamestonk Terminal</a>
- Find out the max-pain price, OTM & ITM options and Call/Put ratio of the next few weeks.
- NOTE: Options chain and max-pain price are updated real time. Hence, there may be a slight delay in rendering this page. 
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>
![Options](./static/images/options.png)

#### /ticker/short_volume/
- View short volume and short percentage of some of the popular tickers.
- Data is from <a href="http://shortvolumes.com/">shortvolumes.com</a>
![Short Volume](./static/images/short_volume.png)

#### /ticker/failure_to_deliver/
- View failure to deliver data of some of the popular tickers.
- Data is from <a href="https://www.sec.gov/data/foiadocsfailsdatahtm">SEC.gov</a>
![Failure to Deliver](./static/images/ftd.png)

#### /earnings_calendar/
- View all tickers earnings report for the week ahead 
- Market Cap, EPS Estimate and EPS Actual
- Sortable by market cap and day
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>
![Earnings Calendar](./static/images/earnings_calendar.png)

#### /reddit_analysis/
- Find the most mentioned tickers with their sentiment level on different subreddits such as r/wallstreetbets, r/stockmarket and r/stocks. Inspired from <a href="https://github.com/kaito1410/AutoDD_Rev2/blob/main/AutoDD.py">Auto DD</a>
- Data is updated daily, around 1 hour before market open.
![Reddit Analysis](./static/images/reddit_trending.png)

#### /reddit_etf/
- Analyse the performance of trending tickers on r/wallstreetbets.
- Top 10 most mentioned tickers with the highest sentiment will be added to the "Reddit ETF" when market opens.
- Tickers that fall outside the Top 10 list will be sold.
![Reddit ETF](./static/images/etf.png)

#### /subreddit_count/
- Look at the increase in number of redditors on popular sub-reddits such as r/wallstreetbets, r/Superstonk and r/amcstock.
- Growth in number of new redditors and percentage of active redditors.
- This page is currently very basic, open to new suggestions on how to improve this page.
![Subreddit Stats](./static/images/subreddit_stats.png)

#### /due_diligence/
- Note: This page is still in development
- A compilation of top due-diligence on Reddit. 
- Data is manually sourced by Stocksera on a regular basis.

#### /top_movers/
- Identify top gainers and losers during market hours.
![Top Movers](./static/images/top_movers.png)

#### /short_interest/
- Identify tickers with the highest short interest level.
![Short Interest](./static/images/short_interest.png)

#### /low_float/
- Identify tickers with low float.
![Low Float](./static/images/low_float.png)

#### /ark_trades/
- View holdings, trades and news of all companies in ARK Fund.
- View trades and ownership of a ticker.
- Data is from <a href="https://arkfunds.io/api/">arkfunds.io/api</a>
![ARK Trades](./static/images/ark_trades.png)

#### /latest_news/
- View latest news of your favorite ticker
- Get their overall news sentiment and their sentiment level over time
- Compare the sentiment level with other popular tickers such as GME, AAPL, TSLA.
- NOTE: This feature is not available on pythonanywhere. To use this feature, you have to host the application locally. Please refer to the Developers section for more details
- Data is from <a href="https://finviz.com/">finviz</a>
![News Sentiment](./static/images/news_sentiment.png)

### For developers:
- Advantages of hosting it locally on your computer:
    - Faster rendering time
    - Customise your own ticker
    - Access to news sentiment

#### Setting up and installing dependencies
```
# Clone the project
git clone https://github.com/spartan737/Stocksera.git

# Navigate into project's folder
cd Stockera

# Install modules
pip install -r requiresments.txt
```

#### Sign up credentials for Reddit API
- Register for an API in <a href="https://www.reddit.com/prefs/apps">https://www.reddit.com/prefs/apps </a> and enter credential in scheduled_tasks/config.py


#### Setting up SQLite database (file found in scheduled_tasks folder)
```
cd scheduled_tasks
py create_database.py
```

#### Run scheduled tasks
- Please refer to [Scheduled Tasks Guide](https://github.com/spartan737/Stocksera/tree/master/scheduled_tasks) for more information on how to run scheduled tasks.

#### Setting up news sentiment
- Go to ViewStocks/urls.py and uncomment 'sub_news/' and 'latest_news/'.
- Go to templates/format.html and uncomment line 33.
- Go to templates/ticker_price.html and uncomment line 92-95.

#### Running the application
```
# Set up static file (you only need to run this the first time):
py manage.py collectstatic

# Run application (view it in 127.0.0.1:8000):
py manange.py runserver
# And you're ready to explore!
```

### License:
This project is under the <a href="https://github.com/spartan737/stocksera/blob/master/LICENSE">MIT</a> license.