import os
from datetime import datetime

import psycopg2
from finvizfinance.quote import finvizfinance
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from custom_extensions.custom_words import *

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

interested_tickers = ["TSLA", "GME", "AMC", "SPY", "NIO", "BB", "PLTR", "AAPL", "AMD", "VIAC", "NOK", "MVIS",
                      "OCGN", "CLOV"]
date_updated = str(datetime.now()).split()[0]

# db.execute("DELETE FROM news_sentiment")

for ticker_selected in interested_tickers:
    ticker_fin = finvizfinance(ticker_selected)

    news_df = ticker_fin.TickerNews()
    news_df["Date"] = news_df["Date"].dt.date
    del news_df["Link"]

    all_titles = news_df[news_df['Date'] == news_df["Date"].unique()[0]]['Title'].tolist()

    num_rows = 0
    total_score = 0
    for title in all_titles:
        vs = analyzer.polarity_scores(title)
        sentiment_score = vs['compound']
        if sentiment_score != 0:
            num_rows += 1
            total_score += sentiment_score
        # print(vs, title)
    if num_rows == 0:
        avg_score = 25
    else:
        avg_score = round((total_score / num_rows) * 100, 2)

    db.execute("INSERT INTO news_sentiment VALUES (%s, %s, %s)", (ticker_selected, avg_score, date_updated))
    print("INSERT {} INTO DATABASE SUCCESSFULLY!".format(ticker_selected))
