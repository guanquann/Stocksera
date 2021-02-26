import os
import requests
from datetime import *

from custom_words import *

import yfinance as yf
import pandas as pd
from django.shortcuts import render
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

stopwords = nltk.corpus.stopwords.words("english")
url = 'https://newsapi.org/v2/everything?'


def home(request):
    tickers_list = pd.read_csv(r"nasdaq_screener_1613136998474.csv")
    list_of_sectors = sorted(tickers_list['Sector'].astype(str).unique().tolist())[:-1]
    list_of_industries = sorted(tickers_list['Industry'].astype(str).unique().tolist())[:-1]

    popular_ticker_list = ["SPY", "GOOG", "AAPL", "AMZN", "TSLA", "MSFT", "PLTR", "NVDA", "BB", "ARKK", "ARKF"]
    popular_name_list = ["S&P500 ETF", "Alphabet", "Apple", "Amazon", "Tesla", "Microsoft", "Palantir",
                         "NVIDIA", "BlackBerry", "ARK Invest", "ARK Fintech"]

    price_list = list()
    for ticker in popular_ticker_list:
        ticker = yf.Ticker(ticker)
        price_df = ticker.history(period="3d")['Close']
        opening_price = float(price_df.iloc[1])
        closing_price = float(price_df.iloc[2])

        price_change = str(round(closing_price - opening_price, 2))

        percentage_change = round((1 - opening_price / closing_price) * 100, 2)
        if percentage_change >= 0:
            price_change = '+' + price_change
            percentage_change = '+' + str(percentage_change)

        price_list.append([round(closing_price, 2), price_change, percentage_change])

    if request.method == "GET":
        return render(request, 'home.html', {"list_of_sectors": list_of_sectors,
                                             "list_of_industries": list_of_industries,
                                             "popular_ticker_list": popular_ticker_list,
                                             "popular_name_list": popular_name_list,
                                             "price_list": price_list
                                             })


def stock_price(request):
    tickers_list = pd.read_csv(r"nasdaq_screener_1613136998474.csv")
    symbols_list = tickers_list["Symbol"]

    if request.method == "GET":
        return render(request, 'ticker_price.html', {"symbols_list": symbols_list})

    if request.method == "POST":
        ticker_selected = request.POST.get("ticker").upper()
        ticker = yf.Ticker(ticker_selected)

        # if "one_day_btn" in request.POST:
        price_df = ticker.history(period="1d", interval="1m")
        ticker_date_max = list(map(lambda x: x.split(" ")[1].split("-")[0].rsplit(":", 1)[0],
                                   price_df.index.astype(str).to_list()))
        if "five_day_btn" in request.POST:
            price_df = ticker.history(period="5d", interval="30m")
            ticker_date_max = list(map(lambda x: x.split(" ")[0], price_df.index.astype(str).to_list()))
        elif "one_month_btn" in request.POST:
            price_df = ticker.history(period="1mo", interval="1d")
            ticker_date_max = list(map(lambda x: x.rsplit(" ", 1)[0], price_df.index.astype(str).to_list()))
        elif "one_year_btn" in request.POST:
            price_df = ticker.history(period="1y")
            ticker_date_max = list(map(lambda x: x.rsplit(" ", 1)[0], price_df.index.astype(str).to_list()))
        elif "five_year_btn" in request.POST:
            price_df = ticker.history(period="5y")
            ticker_date_max = list(map(lambda x: x.rsplit(" ", 1)[0], price_df.index.astype(str).to_list()))

        price_df['Date'] = price_df.index

        information = ticker.info
        img = information["logo_url"]
        official_name = information["longName"]
        try:
            sector = information["sector"]
            industry = information["industry"]
        except KeyError:
            sector = "-"
            industry = "-"

        mkt_open = information["regularMarketOpen"]
        mkt_close = information["previousClose"]
        mkt_low = information["regularMarketDayLow"]
        mkt_high = information["dayHigh"]
        mkt_vol = information["regularMarketVolume"]
        if mkt_vol < 1000000:
            mkt_vol = str(round(mkt_vol/1000, 2)) + "K"
        elif 1000000 <= mkt_vol < 1000000000:
            mkt_vol = str(round(mkt_vol / 1000000, 2)) + "M"
        else:
            mkt_vol = str(round(mkt_vol / 1000000000, 2)) + "B"

        mkt_year_high = information["fiftyTwoWeekHigh"]
        mkt_year_low = information["fiftyTwoWeekLow"]

        website = information["website"]
        summary = information["longBusinessSummary"]
        print(official_name)

        all_news_score_list = list()
        date_list = list()

        # for date_diff in range(14):
        #     # date_from = str(datetime.now() - timedelta(days=date_diff+1)).split()[0]
        #     date_to = str(datetime.now() - timedelta(days=date_diff)).split()[0]
        #
        #     parameters = {
        #         'q': official_name.lower().replace("limited", ""),
        #         'sortBy': 'popularity',
        #         'from': date_to,
        #         'to': date_to,
        #         'language': 'en',
        #         'pageSize': 30,  # maximum is 100 for developer version
        #         'apiKey': 'bf25476268b640d0a6972e685f1c7215'
        #     }
        #
        #     response = requests.get(url, params=parameters)
        #     print(response)
        #     news_score = 0
        #
        #     for news in response.json()['articles']:
        #         # print(news['publishedAt'])
        #         # print(news['title'])
        #         # print()
        #         if news['title'] is not None:
        #             vs = analyzer.polarity_scores(news['title'])
        #             if vs["compound"] > 0.1 or vs["compound"] < -0.1:
        #                 news_score += vs["compound"]
        #                 # print(news['title'])
        #                 # print(vs["compound"])
        #                 # all_news.add([news['title'], vs["compound"]])
        #
        #         if news['description'] is not None:
        #             vs = analyzer.polarity_scores(news['description'])
        #             if vs["compound"] > 0.1 or vs["compound"] < -0.1:
        #                 news_score += vs["compound"]
        #                 # print(news['description'])
        #                 # print(str(vs["compound"]))
        #                 # all_news.add([news['description'], vs["compound"]])
        #     all_news_score_list.append(news_score)
        #     date_list.append(date_to)
        #
        #     print(news_score, "-------------", date_to)
        #
        # print(all_news_score_list.reverse())
        # print(date_list.reverse())

        return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected, "symbols_list": symbols_list,
                                             "ticker_date_max": ticker_date_max,
                                             "ticker_price_max": list(map(lambda x: round(x, 2),
                                                                          price_df["Close"].to_list())),
                                             "img": img, "official_name": official_name, "sector": sector,
                                             "industry": industry, "mkt_open": mkt_open, "mkt_close": mkt_close,
                                             "mkt_low": mkt_low, "mkt_high": mkt_high, "mkt_vol": mkt_vol,
                                             "mkt_year_high": mkt_year_high, "mkt_year_low": mkt_year_low,
                                             "website": website, "summary": summary,
                                             "news_score": all_news_score_list.reverse(),
                                             "date_list": date_list.reverse()
                                             })
