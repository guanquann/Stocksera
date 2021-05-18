# StocksEra

### Instructions

#### /ticker/
- View historical data of your favourite ticker
- Gather key statistics such as EPS, beta and SMA
- Proportion of stocks held by major holders and major institutions
- Price targets set by different organisations
- Recent news articles and their sentiment level
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a> and <a href="https://finviz.com/">finviz</a>

#### /ticker/options/
- View options chain of your favourite ticker
- Find out the max-pain price of the next few weeks
- Options chain and max-pain price are updated real time. Hence, there may be a slight delay in rendering this page. 
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>

#### /ticker/short_volume/
- View short volume and percentage of your favourite ticker in the last 2 trading weeks
- Data is from <a href="http://shortvolumes.com/">shortvolumes.com</a>

#### /earnings_calendar/
- View ALL earnings report for the week ahead 
- Market Cap, EPS Estimate and EPS Actual
- Sortable by market cap and day
- Data is from <a href="https://finance.yahoo.com/">yahoo finance</a>

#### /reddit_analysis/
- Find the most mentioned tickers with their sentiment level on Reddit
- Data is updated daily, around 1 hour before market open.

#### /subreddit_count/
- Look at the increase in number of redditors on popular sub-reddits such as r/wallstreetbets, r/Superstonk and r/amcstock
- This page is currently very basic, open to new suggestions on how to improve this page

#### /reddit_etf/
- Analyse the performance of trending tickers on Reddit
- Top 10 most mentioned tickers with the highest sentiment will be added to the "Reddit ETF" when market opens
- Tickers that fall outside the Top 10 list will be sold

#### /top_movers/
- Identify top gainers and losers during market hours

#### /short_interest/
- Identify tickers with the highest short interest level

#### /low_float/
- Identify tickers with low float

#### /penny_stocks/
- View performance of penny stocks

#### /ark_trades/
- View holdings, trades and news of all companies in ARK Fund.
- View trades and ownership of a ticker
- Data is from <a href="https://arkfunds.io/api/">arkfunds.io/api</a>

#### /latest_news/
- View latest news of your favorite ticker
- Get their overall news sentiment and their sentiment level over time
- Compare the sentiment level with other popular tickers such as GME, AAPL, TSLA.
- Data is from <a href="https://finviz.com/">finviz</a>

### For developers:

#### Setting up and installing dependencies
```
# Clone the project
git clone https://github.com/spartan737/Stocksera.git

# Navigate into project's folder
cd Stockera

# Install modules
pip install -r requiresments.txt
```

#### Enter credentials
- Register for an API in <a href="https://www.reddit.com/prefs/apps">https://www.reddit.com/prefs/apps </a> and enter credential in config.py


#### Setting up database
```
py create_database.py
```

#### Running the application
```
# Run application (view it in 127.0.0.1:8000)
py manange.py runserver

# And you're ready to explore!
```

### License:
This project is under the <a href="https://github.com/spartan737/stocksera/blob/master/LICENSE">MIT</a> license.