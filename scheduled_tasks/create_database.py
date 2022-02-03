"""
Script to create database inside scheduled_tasks folder
"""
import sqlite3

conn = sqlite3.connect("database/database.db", check_same_thread=False)
db = conn.cursor()


def database():
    db.execute("CREATE table IF NOT EXISTS stocksera_trending ("
               "symbol TEXT, "
               "name TEXT, "
               "count INTEGER, "
               "UNIQUE('symbol'))")

    subreddits = ["wallstreetbets", "stocks", "options", "pennystocks", "investing", "shortsqueeze",
                  "spacs"]
    for subreddit in subreddits:
        db.execute("CREATE table IF NOT EXISTS {} ("
                   "rank INTEGER NOT NULL, "
                   "ticker VARCHAR (10), "
                   "total INTEGER NOT NULL DEFAULT 0, "
                   "recent INTEGER NOT NULL DEFAULT 0, "
                   "previous INTEGER NOT NULL DEFAULT 0, "
                   "change FLOAT, "
                   "rockets INTEGER NOT NULL DEFAULT 0, "
                   "posts INTEGER NOT NULL DEFAULT 0, "
                   "upvotes INTEGER NOT NULL DEFAULT 0, "
                   "comments INTEGER NOT NULL DEFAULT 0, "
                   "price FLOAT, "
                   "one_day_change_percent FLOAT, "
                   "fifty_day_change_percent FLOAT, "
                   "volume VARCHAR (10), "
                   "mkt_cap VARCHAR (25), "
                   "floating_shares VARCHAR (10), "
                   "beta VARCHAR (10), "
                   "short_per_float VARCHAR (10), "
                   "industry VARCHAR (100), "
                   "website VARCHAR (150), "
                   "prev_close VARCHAR (10), "
                   "open VARCHAR (10), "
                   "day_low VARCHAR (10), "
                   "day_high VARCHAR (10), "
                   "target VARCHAR (10), "
                   "recommend VARCHAR (20), "
                   "date_updated VARCHAR (20), "
                   "subreddit VARCHAR (25),"
                   "ID INTEGER PRIMARY KEY AUTOINCREMENT)".format(subreddit))

    db.execute("CREATE table IF NOT EXISTS cryptocurrency ("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT, "
               "rank INTEGER NOT NULL, "
               "ticker VARCHAR (10), "
               "total INTEGER NOT NULL DEFAULT 0, "
               "recent INTEGER NOT NULL DEFAULT 0, "
               "previous INTEGER NOT NULL DEFAULT 0, "
               "change FLOAT, "
               "rockets INTEGER NOT NULL DEFAULT 0, "
               "posts INTEGER NOT NULL DEFAULT 0, "
               "upvotes INTEGER NOT NULL DEFAULT 0, "
               "comments INTEGER NOT NULL DEFAULT 0, "
               "price FLOAT, "
               "one_day_change_percent FLOAT, "
               "thirty_day_change_percent FLOAT, "
               "volume VARCHAR (10), "
               "mkt_cap VARCHAR (25), "
               "circulating_supply VARCHAR (20),"
               "max_supply VARCHAR (20),"
               "date_updated VARCHAR(20) )")

    db.execute("CREATE table IF NOT EXISTS wsb_trending_24H ("
               "ticker TEXT, "
               "mentions INTEGER, "
               "sentiment FLOAT, "
               "calls TEXT, "
               "puts TEXT, "
               "date_updated TEXT )")

    db.execute("CREATE table IF NOT EXISTS wsb_trending_hourly ("
               "ticker TEXT, "
               "mentions INTEGER, "
               "sentiment FLOAT, "
               "calls TEXT, "
               "puts TEXT, "
               "date_updated TEXT )")

    db.execute("CREATE table IF NOT EXISTS wsb_yf ("
               "ticker TEXT, "
               "mkt_cap TEXT, "
               "price_change FLOAT, "
               "industry TEXT, "
               "sector TEXT, "
               "difference_sma FLOAT, "
               "difference_52w_high FLOAT, "
               "difference_52w_low FLOAT, "
               "mentions INTEGER )")

    db.execute("CREATE table IF NOT EXISTS crypto_trending_24H ("
               "ticker TEXT, "
               "mentions INTEGER, "
               "sentiment FLOAT, "
               "date_updated TEXT )")

    db.execute("CREATE table IF NOT EXISTS crypto_trending_hourly ("
               "ticker TEXT, "
               "mentions INTEGER, "
               "sentiment FLOAT, "
               "date_updated TEXT )")

    for i in ["wsb", "crypto"]:
        db.execute("CREATE table IF NOT EXISTS {}_change ("
                   "ticker TEXT, "
                   "mentions INTEGER, "
                   "change FLOAT) ".format(i))

        db.execute("CREATE table IF NOT EXISTS {}_word_cloud ("
                   "word TEXT, "
                   "mentions INTEGER, "
                   "date_updated TEXT )".format(i))

    db.execute("CREATE table IF NOT EXISTS reddit_etf ("
               "ticker TEXT, "
               "open_date TEXT, "
               "open_price FLOAT, "
               "num_shares INTEGER, "
               "close_date TEXT, "
               "close_price FLOAT, "
               "PnL FLOAT, "
               "percentage FLOAT, "
               "status TEXT)")

    db.execute("CREATE table IF NOT EXISTS earnings_calendar ("
               "name TEXT, "
               "symbol TEXT, "
               "mkt_cap INTEGER, "
               "eps_est TEXT, "
               "eps_act TEXT, "
               "surprise TEXT, "
               "earning_date TEXT, "
               "earning_time TEXT, "
               "UNIQUE(name, symbol) )")

    db.execute("CREATE table IF NOT EXISTS subreddit_count ("
               "ticker TEXT, "
               "subreddit TEXT, "
               "subscribers INTEGER, "
               "active INTEGER, "
               "updated_date TEXT,"
               "percentage_active FLOAT, "
               "growth FLOAT, "
               "percentage_price_change FLOAT, "
               "UNIQUE(ticker, subreddit, updated_date) )")

    db.execute("CREATE table IF NOT EXISTS twitter_followers ("
               "ticker TEXT, "
               "followers INTEGER, "
               "updated_date TEXT,"
               "UNIQUE('ticker', 'updated_date' ))")

    db.execute("CREATE table IF NOT EXISTS twitter_trending ("
               "ticker TEXT, "
               "tweet_count INTEGER, "
               "updated_date TEXT,"
               "UNIQUE('ticker', 'updated_date' ))")

    db.execute("CREATE table IF NOT EXISTS short_interest ("
               "ticker TEXT, "
               "date TEXT, "
               "short_interest INTEGER, "
               "average_vol INTEGER, "
               "days_to_cover FLOAT, "
               "percent_float_short FLOAT)")

    db.execute("CREATE table IF NOT EXISTS low_float ("
               "ticker TEXT, "
               "company TEXT, "
               "exchange TEXT, "
               "previous_close FLOAT, "
               "one_day_change FLOAT, "
               "float TEXT, "
               "outstanding_shares TEXT,"
               "short_int TEXT, "
               "market_cap INTEGER, "
               "industry TEXT )")

    db.execute("CREATE table IF NOT EXISTS reverse_repo ("
               "record_date TEXT, "
               "amount FLOAT, "
               "parties INTEGER, "
               "average FLOAT, "
               "UNIQUE ('record_date') )")

    db.execute("CREATE table IF NOT EXISTS daily_treasury ("
               "record_date TEXT, "
               "close_today_bal FLOAT, "
               "open_today_bal FLOAT, "
               "amount_change FLOAT, "
               "percent_change FLOAT, "
               "UNIQUE ('record_date') )")

    db.execute("CREATE table IF NOT EXISTS retail_sales ("
               "record_date TEXT, "
               "value FLOAT, "
               "percent_change FLOAT, "
               "covid_monthly_avg INTEGER, "
               "UNIQUE ('record_date') )")

    db.execute("CREATE table IF NOT EXISTS initial_jobless_claims (record_date TEXT, "
               "value INTEGER, "
               "percent_change FLOAT, "
               "UNIQUE ('record_date') )")

    db.execute("CREATE table IF NOT EXISTS inflation ("
               "Year TEXT, "
               "Jan FLOAT, "
               "Feb FLOAT, "
               "Mar FLOAT, "
               "Apr FLOAT, "
               "May FLOAT, "
               "Jun FLOAT, "
               "Jul FLOAT, "
               "Aug FLOAT, "
               "Sep FLOAT, "
               "Oct FLOAT, "
               "Nov FLOAT, "
               "Dec FLOAT, "
               "Avg FLOAT )")

    db.execute("CREATE table IF NOT EXISTS sec_fillings ("
               "ticker TEXT, "
               "filling TEXT, "
               "description TEXT, "
               "filling_date TEXT, "
               "report_url TEXT, "
               "filing_url) ")

    db.execute("CREATE table IF NOT EXISTS daily_ticker_news ("
               "Ticker TEXT, "
               "Date TEXT, "
               "Title TEXT, "
               "Link TEXT, "
               "Sentiment TEXT )")

    db.execute("CREATE table IF NOT EXISTS insider_trading ("
               "Ticker TEXT, "
               "Name TEXT, "
               "Relationship TEXT, "
               "TransactionDate TEXT, "
               "TransactionType TEXT, "
               "Cost FLOAT, "
               "Shares INTEGER, "
               "Value INTEGER, "
               "SharesLeft INTEGER,"
               "URL TEXT )")

    db.execute("CREATE table IF NOT EXISTS latest_insider_trading ("
               "Ticker TEXT, "
               "Name TEXT, "
               "Relationship TEXT, "
               "TransactionDate TEXT, "
               "TransactionType TEXT, "
               "Cost FLOAT, "
               "Shares INTEGER, "
               "Value INTEGER, "
               "SharesLeft INTEGER,"
               "DateFilled TEXT, "
               "URL TEXT, "
               "UNIQUE ('Ticker', 'Name', 'Relationship', 'TransactionDate', 'TransactionType', 'Cost', 'Shares', "
               "'Value', 'SharesLeft', 'DateFilled') )")

    db.execute("CREATE table IF NOT EXISTS latest_insider_trading_analysis ("
               "Symbol TEXT, "
               "Amount INTEGER, "
               "MktCap INTEGER, "
               "Proportion FLOAT) ")

    db.execute("CREATE table IF NOT EXISTS related_tickers ("
               "ticker TEXT, "
               "ticker1 TEXT, "
               "ticker2 TEXT, "
               "ticker3 TEXT, "
               "ticker4 TEXT, "
               "ticker5 TEXT, "
               "ticker6 TEXT )")

    db.execute("CREATE table IF NOT EXISTS stocktwits_trending ("
               "rank INTEGER, "
               "watchlist INTEGER, "
               "symbol TEXT, "
               "date_updated TEXT )")

    db.execute("CREATE table IF NOT EXISTS jim_cramer_trades ("
               "Symbol TEXT, "
               "Date INTEGER, "
               "Segment TEXT, "
               "Call TEXT,"
               "Price TEXT )")

    # db.execute("CREATE table IF NOT EXISTS max_pain ("
    #            "symbol TEXT, "
    #            "date_updated TEXT, "
    #            "max_pain FLOAT ,"
    #            "UNIQUE ('symbol', 'date_updated', 'max_pain') )")

    print("Successfully created/updated database")


if __name__ == '__main__':
    database()
