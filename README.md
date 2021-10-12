# StocksEra

![Stocksera](./static/images/logo.png)

You can view the application in <a href="https://stocksera.pythonanywhere.com" target="_blank">stocksera.pythonanywhere.com</a>.

<a href="https://stocksera.pythonanywhere.com/subscribe/" target="_blank">![Subscribe](./static/images/github/subscribe.png)</a>

Live demo is available at https://youtu.be/jkAZu7DvhvY.

### Support:
This website is free for everyone. But if you want to support me, please give me a star on Github or you can PayPal to <a href="https://www.paypal.me/stocksera">paypal.me/stocksera</a>. Patreon is also available <a href="https://www.patreon.com/stocksera" target="_blank">here</a>.

### User Guide:

#### /ticker/
- View graph of your favourite ticker.
- Gather key statistics such as EPS, beta and SMA.
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>
![Ticker Stats](./static/images/github/ticker_main.png)


- Sort historical data based on % price change, volume, day and so on.
![Sort Historical Data](./static/images/github/ticker_main1.png)


- Get recent insider trading of a stock.
![Insider Trading](./static/images/github/ticker_main2.png)


- Get recent news and sentiment of a stock.
![News Sentiment](./static/images/github/ticker_main3.png)


- Google trend of a stock and compare it with it's closing price.
![Google Trend](./static/images/github/ticker_main4.png)


- Upgrades & Downgrades of a stock.
![Recommendations](./static/images/github/ticker_main5.png)


- Links to other social media platforms for discussion.
- Stocktwits API.
![Discussion](./static/images/github/ticker_main6.png)

#### /ticker/options/
- View options chain of your favourite ticker. Inspired from <a href="https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal">Gamestonk Terminal</a>.
- Find out the max-pain price, OTM & ITM options and Call/Put ratio of the next few weeks.
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>.
![Options](./static/images/github/options.png)
![Option Chain](./static/images/github/options_chain.png)

#### /ticker/short_volume/
- View short volume and short percentage of some of the popular tickers.
- Data is from <a href="https://cdn.finra.org/">Finra</a>.
![Short Volume](./static/images/github/short_volume.png)

#### /ticker/failure_to_deliver/
- View failure to deliver data of some of the popular tickers.
- Data is from <a href="https://www.sec.gov/data/foiadocsfailsdatahtm">SEC.gov</a>.
![Failure to Deliver](./static/images/github/ftd.png)

#### /earnings_calendar/
- View all tickers earnings report for the week ahead.
- Market Cap, EPS Estimate and EPS Actual.
- Sortable by market cap and day.
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>.
![Earnings Calendar](./static/images/github/earnings_calendar.png)

#### /reddit_analysis/
- Find the most popular tickers with their sentiment level on different subreddits such as r/wallstreetbets, r/stockmarket and r/stocks. Inspired from <a href="https://github.com/kaito1410/AutoDD_Rev2/blob/main/AutoDD.py">Auto DD</a>.
- Trending cryptocurrencies are also analysed in r/Cryptocurrency.
- This only reads the post of the subreddit. The comments are not taken into account. 
- Data is updated daily, around 1 hour before market open.
![Reddit Analysis Stocks](./static/images/github/reddit_trending.png)
![Reddit Analysis Crypto](./static/images/github/reddit_cryptocurrency.png)

#### /wsb_live/
- Tracks trending tickers and their sentiment level on r/wallstreetbets realtime.
- STILL IN PROGRESS

#### /reddit_etf/
- Analyse the performance of trending tickers on r/wallstreetbets.
- Top 10 most mentioned tickers with the highest sentiment will be added to the "Reddit ETF" when market opens.
- Tickers that fall outside the Top 10 list will be sold.
![Reddit ETF](./static/images/github/etf.png)

#### /reddit_ticker_analysis/
- View ranking of popular tickers in Reddit over time and compare it with its price.
![Reddit Ranking Stocks](./static/images/github/reddit_ranking.png)

#### /subreddit_count/
- Look at the increase in number of redditors on popular subreddits such as r/wallstreetbets, r/Superstonk and r/amcstock.
- Growth in number of new redditors and percentage of active redditors.
![Subreddit Stats](./static/images/github/subreddit_stats.png)

#### /subreddit_count/?quote={{ticker}}
- Look at the increase in number of redditors/active users/percentage growth on specific subreddits and compare it with the stock price.
![Subreddit Stats Individual](./static/images/github/subreddit_stats_individual.png)

#### /market_overview/
- Overview of the performance of the entire market.
- Data is from <a href="https://tradingview.com/">Trading View</a>.
![Market Overview](./static/images/github/market_overview.png)

#### /short_interest/
- Identify tickers with the highest short interest level.
- Data is from <a href="https://www.highshortinterest.com">shortinterest.com</a>
![Short Interest](./static/images/github/short_interest.png)

#### /low_float/
- Identify tickers with low float.
- Data is from <a href="https://www.lowfloat.com">lowfloat.com</a>
![Low Float](./static/images/github/low_float.png)

#### /ark_trades/
- View holdings, trades and news of all companies in ARK Fund.
- View trades and ownership of a ticker.
- Data is from <a href="https://arkfunds.io/api/">arkfunds.io/api</a>
![ARK Trades](./static/images/github/ark_trades.png)
![ARK Trades Individual](./static/images/github/ark_trades_individual.png)

#### /reverse_repo/
- Daily reverse repo transactions (amount, number of parties, average)
- Data is from <a href="https://apps.newyorkfed.org/markets/autorates/tomo-search-page">newyorkfed</a>
![Reverse Repo](./static/images/github/reverse_repo.PNG)

#### /daily_treasury/
- Daily treasury (closing balance, opening balance)
- Data is from <a href="https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/operating-cash-balance">fiscaldata.treasury.gov</a>
![Daily Treasury](./static/images/github/daily_treasury.PNG)

#### /inflation/
- Monthly inflation rate (with heat map) from 2001
- Data is from <a href="https://www.usinflationcalculator.com/inflation/current-inflation-rates/">usinflationcalculator.com/inflation</a>
![Inflation](./static/images/github/inflation.png)

#### /retail_sales/
- Monthly retail sales and compare it with the number of covid-19 cases
- Retail sales data is from <a href="https://ycharts.com/indicators/us_retail_and_food_services_sales">ycharts.com/indicators/us_retail_and_food_services_sales</a>
- Covid-19 data is from <a href="https://covid.ourworldindata.org/data/owid-covid-data.csv">covid.ourworldindata.org/data/owid-covid-data.csv</a>
![Retail Sales](./static/images/github/retail_sales.png)

#### /beta/
- Calculate the true beta value of any stock real-time.
![Beta](./static/images/github/beta.png)

#### /amd_xlnx_ratio/
- AMD-XLNX Share Price Ratio.
- Percentage upside when buying XLNX
![AMD-XLNX Ratio](./static/images/github/amd_xlnx_ratio.PNG)

### For developers:

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
pip install -r requirements.txt

# Set up static file (if debug is set to False in settings.py)
py manage.py collectstatic
```

Download nltk data for sentiment analysis. Type the following in console:
```
>>> import nltk
>>> nltk.download("vader_lexicon")
```

#### tasks_to_run.py
- Compilation of tasks that are needed to be completed.
- Get trending tickers in Reddit, subreddit subscribers statistics, stocks with low float and high short interest.

#### Run scheduled tasks
- Please refer to [Scheduled Tasks Guide](https://github.com/spartan737/Stocksera/tree/master/scheduled_tasks) for more information on how to run scheduled tasks.

#### Running the application
You can run run_app.bat.

Alternatively, you can run using your terminal:
```
cd venv/Scripts
activate
cd ../..
py manange.py runserver
```
You can view the application in 127.0.0.1:8000.

### License:
This project is under the <a href="https://github.com/spartan737/stocksera/blob/master/LICENSE">MIT</a> license.