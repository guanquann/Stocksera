from datetime import datetime
import os
import praw
import psycopg2

CLIENT_ID = "3RbFQX8O9UqDCA"
CLIENT_SECRET = "NalOX_ZQqGWP4eYKZv6bPlAb2aWOcA"
USER_AGENT = "subreddit_scraper"
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# If using database from Heroku
if os.environ.get('DATABASE_URL'):
    postgres_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(postgres_url, sslmode='require')
# If using local database
else:
    conn = psycopg2.connect("dbname=stocks_analysis "
                            "user=postgres "
                            "password=admin")
conn.autocommit = True
db = conn.cursor()
# db.execute("DELETE FROM subreddit_count")
interested_subreddit = ["wallstreetbets", "stocks", "StockMarket", "GME", "Superstonk", "amcstock"]
date_updated = str(datetime.now()).split()[0]

for subreddit_name in interested_subreddit:
    subreddit = reddit.subreddit(subreddit_name)
    subscribers = subreddit.subscribers
    db.execute("INSERT INTO subreddit_count VALUES (%s, %s, %s)", (subreddit_name, subscribers, date_updated))
