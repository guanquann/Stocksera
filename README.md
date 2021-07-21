# StocksEra


You can view the application in:
- <a href="https://stocksera.pythonanywhere.com">stocksera.pythonanywhere.com </a>

Alternatively, you can look at https://youtu.be/SEYXEcVKt38 for a live demo.

But because I'm hosting it free on pythonanywhere, speed of website can be (very) slow when traffic is high. 

![Web Traffic](./static/images/web_traffic.png)

You are encouraged to host it locally on your computer, where the speed is much faster.

### Support:
This website will be free forever! No subscription needed! But if you want to support me, please give me a star on Github or you can PayPal to <a href="https://www.paypal.me/stocksera">paypal.me/stocksera</a>

### User Guide:

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

#### /reddit_ticker_analysis/
- View ranking of popular tickers in Reddit over time and compare it with its price.
![Reddit Ranking](./static/images/reddit_ranking.png)

#### /subreddit_count/
- Look at the increase in number of redditors on popular sub-reddits such as r/wallstreetbets, r/Superstonk and r/amcstock.
- Growth in number of new redditors and percentage of active redditors.
- This page is currently very basic, open to new suggestions on how to improve this page.
![Subreddit Stats](./static/images/subreddit_stats.png)

#### /market_overview/
- Overview of the performance of the entire market.
- Data is from <a href="https://tradingview.com/">Trading View</a>
![Market Overview](./static/images/market_overview.png)

#### /short_interest/
- Identify tickers with the highest short interest level.
- Data is from <a href="https://www.highshortinterest.com">shortinterest.com</a>
![Short Interest](./static/images/short_interest.png)

#### /low_float/
- Identify tickers with low float.
- Data is from <a href="https://www.lowfloat.com">lowfloat.com</a>
![Low Float](./static/images/low_float.png)

#### /hedge_funds/
- Identify top holdings from some of the major hedge funds.
- Data is from <a href="https://whalewisdom.com/">whalewisdom</a>
![Hedge Funds](./static/images/hedge_funds.png)

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

# Create environment
py -m venv venv

# Navigate into project's folder and activate venv
cd Stockera/venv/Scripts
activate
cd .. / ..

# Install modules
pip install -r requiresments.txt

# Set up static file
py manage.py collectstatic
```

Download nltk data for sentiment analysis. Type the following in console:
```
>>> import nltk
>>> nltk.download("vader_lexicon")
```

#### Sign up credentials for Reddit API
- Register for an API in <a href="https://www.reddit.com/prefs/apps">https://www.reddit.com/prefs/apps </a> and enter credential in scheduled_tasks/config.py

#### tasks_to_run.py
- Compilation of tasks that are needed to be completed.
- Get trending tickers in Reddit, subreddit subscribers statistics, stocks with low float and high short interest.

#### Run scheduled tasks
- Please refer to [Scheduled Tasks Guide](https://github.com/spartan737/Stocksera/tree/master/scheduled_tasks) for more information on how to run scheduled tasks.

#### Setting up news sentiment
- Go to ViewStocks/urls.py and uncomment 'sub_news/' and 'latest_news/'.
- Go to templates/format.html and uncomment line 33.
- Go to templates/ticker_price.html and uncomment line 122-125.

#### Running the application
You can run run_app.bat.

Alternatively, you can run using your terminal:
```
cd venv/Scripts
activate
cd ../..
py manange.py runserver
```
You can view the application in 127.0.0.1:8000 and you are ready to explore!

### Future improvements:
- [x] Show hedge funds (Citadel, Melvin Capital etc) major holdings
- [x] Show T-35 date in FTD data
- [x] Sort hedge funds holdings
- [x] Add 30 days graph for trending reddit tickers
- [x] Show ranking of tickers in reddit and compare it with its price
- [x] Improve speed of website (although I feel that the major issue lies with pythonanywhere-the website I'm hosting instead, since it runs smoothly locally)
    - Solved by caching tickers' information when market is closed and caching financial data
- [ ] Add trending symbols on r/cryptocurrency
- [ ] Income Statement and Cash Flow for Financial data
- [ ] Show theta, delta, gamma in Options data
- [ ] Show performance of Reddit ETF vs SPY

### Review and Showcase:
In 10 hours, there were more than 10 awards and 500 upvotes.
![Review and Showcase in r/options](./static/images/reddit_review.png)

### License:
This project is under the <a href="https://github.com/spartan737/stocksera/blob/master/LICENSE">MIT</a> license.