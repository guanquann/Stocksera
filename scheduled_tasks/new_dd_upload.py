import re
from datetime import datetime
import sqlite3
import praw

import scheduled_tasks.config as cfg

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()


def upload_new_dd(url, ticker):
    reddit = praw.Reddit(client_id=cfg.API_REDDIT_CLIENT_ID,
                         client_secret=cfg.API_REDDIT_CLIENT_SECRET,
                         user_agent=cfg.API_REDDIT_USER_AGENT)
    submission = reddit.submission(url)
    title = submission.title
    print(submission.selftext)
    text = submission.selftext[:1000]
    upvotes = submission.score
    comments = submission.num_comments
    subreddit = submission.subreddit
    date_text = str(datetime.fromtimestamp(submission.created_utc)).split()[0]

    url_pattern = "((https://preview.redd.it?)((/)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
    img_url = re.findall(url_pattern, submission.selftext)
    text = re.sub(url_pattern, "", text)
    if len(img_url) > 0:
        img_url = img_url[0][0]
    else:
        img_url = ""

    db.execute("INSERT INTO top_DD VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (url, ticker, title, text, int(upvotes), int(comments), str(subreddit), date_text, img_url))
    conn.commit()


if __name__ == '__main__':
    upload_new_dd("nqxtzd", "BB")