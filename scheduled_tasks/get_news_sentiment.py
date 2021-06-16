from datetime import datetime
import sqlite3

from finvizfinance.quote import finvizfinance
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from custom_extensions.custom_words import *

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

interested_tickers = ["TSLA", "GME", "AMC", "SPY", "NIO", "BB", "PLTR", "AAPL", "AMD", "VIAC", "NOK", "MVIS",
                      "OCGN", "CLOV"]
date_updated = str(datetime.now()).split()[0]


def news_sentiment():
    """
    Get the news sentiment score of popular tickers from Finviz news
    """
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

        if num_rows == 0:
            avg_score = 25
        else:
            avg_score = round((total_score / num_rows) * 100, 2)

        db.execute("INSERT INTO news_sentiment VALUES (?, ?, ?)", (ticker_selected, avg_score, date_updated))
        conn.commit()
        print("INSERT {} INTO NEWS SENTIMENT DATABASE SUCCESSFULLY!".format(ticker_selected))


if __name__ == '__main__':
    news_sentiment()
