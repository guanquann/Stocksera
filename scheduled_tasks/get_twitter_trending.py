import os
from datetime import datetime

import psycopg2
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from custom_extensions.custom_words import *

# Insert your twitter API key here
ckey = ""
csecret = ""
atoken = ""
asecret = ""

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

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

# Create a database for storing twitter data
mycursor.execute("CREATE DATABASE IF NOT EXISTS twitter_data")

mycursor.execute("""CREATE TABLE IF NOT EXISTS twitter_data.twitter_data_sentiment
                (date_time DATETIME,
                author VARCHAR(500),
                tweet VARCHAR(2000),
                sentiment DECIMAL(5,4)
                )
                """)

sqlFormula = "INSERT INTO twitter_data.twitter_data_sentiment (date_time, author, tweet, sentiment) VALUES (%s, %s, %s, %s)"


class listener(StreamListener):
    def on_data(self,data):
        all_data = json.loads(data)
        current_time = datetime.datetime.now()
        author = str(all_data['user']['screen_name'])
        tweet = str(all_data["text"])
        vs = analyzer.polarity_scores(unidecode(tweet))
        sentiment = vs['compound']
        db = (current_time, author, tweet,sentiment)
        mycursor.execute(sqlFormula, db)
        mydb.commit()
    def on_error(self,status):
        print(status)

## Connecting to twitter and establishing a live stream
while True:
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["$"]) #this tracks any tweet with a $ symbol. Unlike Reddit, a large proportion of twitter users use $ before the stock tickers
    except Exception as e:
        print(str(e))
        time.sleep(10)