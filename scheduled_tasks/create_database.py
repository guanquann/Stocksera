import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

subreddits = ["wallstreetbets", "stocks", "stockmarket"]
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

db.execute("CREATE table IF NOT EXISTS news_sentiment ("
           "ticker TEXT, "
           "sentiment FLOAT, "
           "date_updated TEXT )")

db.execute("CREATE table IF NOT EXISTS reddit_etf ("
           "ticker TEXT, "
           "logo_url TEXT, "
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
           "mkt_cap TEXT, "
           "eps_est TEXT, "
           "eps_act TEXT, "
           "img_url TEXT, "
           "earning_date TEXT, "
           "earning_time TEXT )")

db.execute("CREATE table IF NOT EXISTS subreddit_count ("
           "subreddit TEXT, "
           "subscribers INTEGER, "
           "active INTEGER, "
           "updated_date TEXT,"
           "percentage_active FLOAT, "
           "growth FLOAT)")

db.execute("CREATE table IF NOT EXISTS short_interest ("
           "ticker TEXT, "
           "company TEXT, "
           "exchange TEXT, "
           "short_int TEXT, "
           "float TEXT, "
           "outstanding_shares TEXT,"
           "industry TEXT)")

db.execute("CREATE table IF NOT EXISTS low_float ("
           "ticker TEXT, "
           "company TEXT, "
           "exchange TEXT, "
           "float TEXT, "
           "outstanding_shares TEXT,"
           "short_int TEXT, "
           "industry TEXT)")

db.execute("CREATE table IF NOT EXISTS short_volume ("
           "ticker TEXT, "
           "reported_date TEXT, "
           "close_price FLOAT, "
           "short_vol INTEGER, "
           "total_vol INTEGER, "
           "percent TEXT, "
           "UNIQUE('ticker', 'reported_date','short_vol','total_vol','percent'))")

db.execute("CREATE table IF NOT EXISTS contact ("
           "name TEXT, "
           "email TEXT, "
           "suggestions TEXT)")
