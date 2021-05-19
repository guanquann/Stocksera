import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

db.execute("CREATE table IF NOT EXISTS wallstreetbets ("
           "ticker VARCHAR (10), "
           "one_day_score INTEGER NOT NULL DEFAULT 0, "
           "recent INTEGER NOT NULL DEFAULT 0, "
           "previous INTEGER NOT NULL DEFAULT 0, "
           "change FLOAT, "
           "rockets INTEGER NOT NULL DEFAULT 0, "
           "positive INTEGER NOT NULL DEFAULT 0, "
           "negative INTEGER NOT NULL DEFAULT 0, "
           "price FLOAT, "
           "one_day_change_percent FLOAT, "
           "fifty_day_change_percent FLOAT, "
           "volume VARCHAR (10), "
           "mkt_cap VARCHAR (25), "
           "floating_shares VARCHAR (10), "
           "beta VARCHAR (10), "
           "short_per_float VARCHAR (10), "
           "industry VARCHAR (100), "
           "prev_close VARCHAR (10), "
           "open VARCHAR (10), "
           "day_low VARCHAR (10), "
           "day_high VARCHAR (10), "
           "target VARCHAR (10), "
           "recommend VARCHAR (20), "
           "date_updated VARCHAR (20), "
           "subreddit VARCHAR (25),"
           "ID INTEGER PRIMARY KEY AUTOINCREMENT)")

db.execute("CREATE table IF NOT EXISTS news_sentiment ("
           "ticker TEXT, "
           "sentiment FLOAT, "
           "date_updated TEXT )")

db.execute("CREATE table IF NOT EXISTS earnings_calendar ("
           "name TEXT, "
           "symbol TEXT, "
           "mkt_cap TEXT DEFAULT 0, "
           "eps_est TEXT, "
           "eps_act TEXT, "
           "img_url TEXT, "
           "earning_date TEXT, "
           "earning_time TEXT)")

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
           "updated_date TEXT )")


# db.execute("CREATE table IF NOT EXISTS dfv_stats ("
#            "author VARCHAR(100), "
#            "title VARCHAR(300), "
#            "selftext VARCHAR(3000), "
#            "link_flair_text VARCHAR(25), "
#            "score INTEGER, "
#            "upvote_ratio FLOAT, "
#            "num_comments INTEGER, "
#            "img_url VARCHAR(300), "
#            "post_link VARCHAR(300), "
#            "total_awards INTEGER, "
#            "total_coin_spent INTEGER, "
#            "total_coin_rewarded INTEGER, "
#            "total_days_premium INTEGER, "
#            "total_money_spent FLOAT, "
#            "total_awards INTEGER, "
#            ")")
