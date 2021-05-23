from datetime import datetime
import sqlite3
import praw

from scheduled_tasks.config import *

CLIENT_ID = API_REDDIT_CLIENT_ID
CLIENT_SECRET = API_REDDIT_CLIENT_SECRET
USER_AGENT = API_REDDIT_USER_AGENT
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

interested_subreddit = ["wallstreetbets", "stocks", "StockMarket", "GME", "Superstonk", "amcstock"]
date_updated = str(datetime.now()).split()[0]


def subreddit_count():
    for subreddit_name in interested_subreddit:
        subreddit = reddit.subreddit(subreddit_name)
        print("Looking at {} now.".format(subreddit))
        subscribers = subreddit.subscribers
        active = subreddit.accounts_active
        db.execute("INSERT INTO subreddit_count VALUES (?, ?, ?, ?)", (subreddit_name, subscribers, active, date_updated))
        conn.commit()
