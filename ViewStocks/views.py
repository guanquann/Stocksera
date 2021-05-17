import os
from datetime import datetime, timedelta

from custom_extensions.custom_words import *
from helpers import *

import psycopg2

from yahoo_earnings_calendar import YahooEarningsCalendar
from finvizfinance.quote import finvizfinance
from finvizfinance.group import (overview, valuation, performance)

from django.shortcuts import render, redirect
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# If using database from Heroku
if os.environ.get('DATABASE_URL'):
    postgres_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(postgres_url, sslmode='require')
# If using local database
else:
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            database="stocks_analysis")

conn.autocommit = True
db = conn.cursor()

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)


def main(request):
    return render(request, "home.html")


def stock_price(request):
    if request.GET.get("financial"):
        ticker_selected = request.GET['financial'].upper()
        return redirect('/ticker/financial/?quote=%s' % ticker_selected)

    elif request.GET.get("options"):
        ticker_selected = request.GET['options'].upper()
        return redirect('/ticker/options/?quote=%s' % ticker_selected)

    elif request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()
        try:
            ticker = yf.Ticker(ticker_selected)
            ticker_fin = finvizfinance(ticker_selected)
            ticker_fin_fundament = ticker_fin.TickerFundament()
                            
            if "five_day" in request.GET:
                price_df = ticker.history(period="5d", interval="30m")
                ticker_date_max = list(map(lambda x: x.split(" ")[0], price_df.index.astype(str).to_list()))
                duration = "1"
            elif "one_month" in request.GET:
                price_df = ticker.history(period="1mo", interval="1d")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "2"
            elif "one_year" in request.GET:
                price_df = ticker.history(period="1y", interval="1d")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "3"
            elif "five_year" in request.GET:
                price_df = ticker.history(period="5y", interval="1wk")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "4"
            else:
                price_df = ticker.history(period="1d", interval="2m")
                ticker_date_max = list(map(lambda x: x.split()[1].split("-")[0].rsplit(":", 1)[0],
                                       price_df.index.astype(str).to_list()))
                duration = "0"

            information = ticker.info
            img = information["logo_url"]
            official_name = ticker_fin_fundament["Company"]

            # print(ticker.calendar)
            # print(ticker.financials)
            # print(ticker.earnings)
            # print(ticker.sustainability, "SUS")

            sector = ticker_fin_fundament['Sector']
            industry = ticker_fin_fundament["Industry"]
            summary = ticker_fin.TickerDescription()
            if "website" in information and information['website'] is not None:
                website = information["website"]
            else:
                website = "https://finance.yahoo.com/quote/{}".format(ticker_selected)

            return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected,
                                                         "ticker_date_max": ticker_date_max,
                                                         "ticker_price_max": list(map(lambda x: round(x, 2),
                                                                                      price_df["Close"].to_list())),
                                                         "duration": duration,
                                                         "img": img, "official_name": official_name,
                                                         "sector": sector, "industry": industry,
                                                         "website": website, "summary": summary,
                                                         "error": "error_false",
                                                         "information": information, "ticker_fin_fundament": ticker_fin_fundament})
        except (IndexError, KeyError, Exception):
            return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected, "error": "error_true"})
    return render(request, 'ticker_price.html')


def ticker_recommendations(request):
    ticker_selected = default_ticker(request)
    ticker_fin = finvizfinance(ticker_selected)
    try:
        recommendations = ticker_fin.TickerOuterRatings()
        recommendations = recommendations.to_html(index=False)
    except AttributeError:
        recommendations = "N/A"
    return render(request, 'iframe_format.html', {"title": "Recommendations", "table": recommendations})


def ticker_major_holders(request):
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    major_holders = ticker.major_holders
    major_holders = major_holders.to_html(index=False, header=False)
    return render(request, 'iframe_format.html', {"title": "Major Holders", "table": major_holders})


def ticker_institutional_holders(request):
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    institutional_holders = ticker.institutional_holders
    if institutional_holders is not None:
        institutional_holders = institutional_holders.to_html(index=False)
    else:
        institutional_holders = "N/A"
    return render(request, 'iframe_format.html', {"title": "Institutional Holders", "table": institutional_holders})


def sub_news(request):
    ticker_selected = default_ticker(request)
    ticker_fin = finvizfinance(ticker_selected)

    news_df = ticker_fin.TickerNews()
    news_df["Date"] = news_df["Date"].dt.date
    link = news_df["Link"].to_list()
    del news_df["Link"]

    sentiment_list = list()
    all_titles = news_df['Title'].tolist()
    for title in all_titles:
        vs = analyzer.polarity_scores(title)
        sentiment_score = vs['compound']
        if sentiment_score > 0.25:
            sentiment = "Bullish"
        elif sentiment_score < -0.25:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"
        sentiment_list.append(sentiment)

    news_df["Sentiment"] = sentiment_list
    news_df = news_df.to_html(index=False)
    return render(request, 'iframe_format.html', {"title": "News", "table": news_df, "link": link,
                                                  "class": "ticker_news"})


def latest_news(request):
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    ticker_fin = finvizfinance(ticker_selected)
    ticker_fin_fundament = ticker_fin.TickerFundament()

    information = ticker.info
    img = information["logo_url"]
    official_name = ticker_fin_fundament["Company"]

    sector = ticker_fin_fundament['Sector']
    industry = ticker_fin_fundament["Industry"]

    news_df = ticker_fin.TickerNews()
    news_df["Date"] = news_df["Date"].dt.date
    link = news_df["Link"].to_list()
    del news_df["Link"]

    sentiment_list = list()
    all_news = news_df['Title'].tolist()
    for title in all_news:
        vs = analyzer.polarity_scores(title)
        sentiment_score = vs['compound']
        if sentiment_score > 0.25:
            sentiment = "Bullish"
        elif sentiment_score < -0.25:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"
        sentiment_list.append(sentiment)

    news_df["Sentiment"] = sentiment_list

    num_rows = 0
    total_score = 0
    latest_date = news_df["Date"].unique()[0]
    today_news = news_df[news_df['Date'] == latest_date]['Title'].tolist()
    for title in today_news:
        vs = analyzer.polarity_scores(title)
        sentiment_score = vs['compound']
        if sentiment_score != 0:
            num_rows += 1
            total_score += sentiment_score

    if num_rows == 0:
        avg_score = 25
    else:
        avg_score = round((total_score / num_rows) * 100, 2)

    db.execute("SELECT * FROM news_sentiment WHERE date_updated=%s", (str(datetime.now()).split()[0],))
    ticker_sentiment = db.fetchall()
    days = 1
    while not ticker_sentiment:
        db.execute("SELECT * FROM news_sentiment WHERE date_updated=%s", (str(datetime.now()-timedelta(days=days)).split()[0],))
        ticker_sentiment = db.fetchall()
        days += 1
    ticker_sentiment = list(map(list, ticker_sentiment))

    return render(request, 'news_sentiment.html', {"ticker_selected": ticker_selected,
                                                   "news_df": news_df.to_html(index=False),
                                                   "link": link,
                                                   "official_name": official_name,
                                                   "img": img,
                                                   "industry": industry,
                                                   "sector": sector,
                                                   "ticker_sentiment": ticker_sentiment,
                                                   "latest_date": latest_date,
                                                   "avg_score": avg_score})


def financial(request):
    ticker_selected = default_ticker(request)
    balance_list = []
    ticker = yf.Ticker(ticker_selected)

    official_name, img, sector, industry = get_ticker_basic(ticker)

    balance_sheet = ticker.quarterly_balance_sheet.replace(np.nan, 0)
    # print(balance_sheet)

    date_list = balance_sheet.columns.astype("str").to_list()
    balance_col_list = balance_sheet.index.tolist()

    for i in range(len(balance_sheet)):
        values = balance_sheet.iloc[i].tolist()
        balance_list.append(values)

    yec = YahooEarningsCalendar(0)
    earnings = yec.get_earnings_of(ticker_selected)

    earnings_list, financial_quarter_list = [], []
    # [[1, 0.56, 0.64], [2, 0.51, 0.65], [3, 0.7, 0.73], [4, 1.41, 1.68], [5, 0.98]]
    count = 5
    for earning in earnings:
        if len(earnings_list) != 5:
            if earning["epsestimate"] is not None:
                if earning["epsactual"] is not None:
                    earnings_list.append([count, earning["epsestimate"], earning["epsactual"]])
                else:
                    earnings_list.append([count, earning["epsestimate"]])
                year_num = earning["startdatetime"].split("T")[0].split("-")[0]
                month_num = int(earning["startdatetime"].split("T")[0].split("-")[1])
                if month_num in [1, 2, 3]:
                    year_num = int(year_num) - 1
                    quarter = "Q4"
                elif month_num in [4, 5, 6]:
                    quarter = "Q1"
                elif month_num in [7, 8, 9]:
                    quarter = "Q2"
                else:
                    quarter = "Q3"
                financial_quarter_list.append("{} {}".format(year_num, quarter))
            count -= 1
        else:
            break
    return render(request, 'financial.html', {"ticker_selected": ticker_selected,
                                              "official_name": official_name,
                                              "img": img,
                                              "industry": industry,
                                              "sector": sector,
                                              "date_list": date_list,
                                              "balance_list": balance_list,
                                              "balance_col_list": balance_col_list,
                                              "earnings_list": earnings_list,
                                              "financial_quarter_list": financial_quarter_list, })


def options(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()
        try:
            ticker = yf.Ticker(ticker_selected)

            official_name, img, sector, industry = get_ticker_basic(ticker)
            options_dates = ticker.options
            if request.GET.get("date") != "" and request.GET.get("date") is not None:
                date_selected = request.GET["date"]
            else:
                date_selected = options_dates[0]

            calls = ticker.option_chain(date_selected).calls

            del calls["contractSize"]
            del calls["currency"]
            calls.columns = ["Contract Name", "Last Trade Date", "Strike", "Last Price", "Bid", "Ask", "Change",
                             "% Change", "Volume", "Open Interest", "Implied Volatility", "ITM"]

            last_adj_close_price = float(ticker.info['previousClose'])
            df_calls = calls.pivot_table(
                index="Strike", values=["Volume", "Open Interest"], aggfunc="sum"
            ).reindex()
            df_calls["Strike"] = df_calls.index
            df_calls["Type"] = "calls"
            df_calls["Open Interest"] = df_calls["Open Interest"]
            df_calls["Volume"] = df_calls["Volume"]
            df_calls["oi+v"] = df_calls["Open Interest"] + df_calls["Volume"]
            df_calls["Spot"] = round(last_adj_close_price, 2)

            calls["Volume"].fillna('-', inplace=True)
            calls["Open Interest"].fillna('-', inplace=True)
            calls["Implied Volatility"] = calls["Implied Volatility"].astype("float").multiply(100)

            calls["Change"] = calls["Change"].round(2)
            calls["% Change"] = calls["% Change"].round(2)
            calls["Implied Volatility"] = calls["Implied Volatility"].round(2)

            puts = ticker.option_chain(date_selected).puts

            del puts["contractSize"]
            del puts["currency"]
            puts.columns = ["Contract Name", "Last Trade Date", "Strike", "Last Price", "Bid", "Ask", "Change",
                            "% Change", "Volume", "Open Interest", "Implied Volatility", "ITM"]

            df_puts = puts.pivot_table(
                index="Strike", values=["Volume", "Open Interest"], aggfunc="sum"
            ).reindex()
            df_puts["Strike"] = df_puts.index
            df_puts["Type"] = "puts"
            df_puts["Open Interest"] = df_puts["Open Interest"]
            df_puts["Volume"] = -df_puts["Volume"]
            df_puts["Open Interest"] = -df_puts["Open Interest"]
            df_puts["oi+v"] = df_puts["Open Interest"] + df_puts["Volume"]
            df_puts["Spot"] = round(last_adj_close_price, 2)

            puts["Volume"].fillna('-', inplace=True)
            puts["Open Interest"].fillna('-', inplace=True)
            puts["Implied Volatility"] = puts["Implied Volatility"].astype("float").multiply(100)

            puts["Change"] = puts["Change"].round(2)
            puts["% Change"] = puts["% Change"].round(2)
            puts["Implied Volatility"] = puts["Implied Volatility"].round(2)

            df_merge = pd.merge(calls, puts, on="Strike")
            df_merge = df_merge[["Last Price_x", "Change_x", "% Change_x", "Volume_x", "Open Interest_x", "Strike",
                                 "Last Price_y", "Change_y", "% Change_y", "Volume_y", "Open Interest_y"]]
            df_merge.columns = ["Last Price", "Change", "% Change", "Volume", "Open Interest", "Strike",
                                "Last Price", "Change", "% Change", "Volume", "Open Interest"]

            df_opt = pd.merge(df_calls, df_puts, left_index=True, right_index=True)
            df_opt = df_opt[["Open Interest_x", "Open Interest_y"]].rename(
                columns={"Open Interest_x": "OI Calls", "Open Interest_y": "OI Puts"})
            max_pain, call_loss_list, put_loss_list = get_max_pain(df_opt)

            return render(request, 'options.html', {"ticker_selected": ticker_selected,
                                                    "official_name": official_name,
                                                    "img": img,
                                                    "industry": industry,
                                                    "sector": sector,
                                                    "options_dates": options_dates,
                                                    "date_selected": date_selected,
                                                    "max_pain": max_pain,
                                                    "call_loss_list": call_loss_list,
                                                    "put_loss_list": put_loss_list,
                                                    "calls": calls.to_html(index=False),
                                                    "puts": puts.to_html(index=False),
                                                    "merge": df_merge.to_html(index=False),
                                                    "error": "error_false"})
        except (IndexError, KeyError, Exception):
            return render(request, 'options.html', {"ticker_selected": ticker_selected, "error": "error_true"})
    else:
        return render(request, 'options.html')


def short_volume(request):
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    official_name, img, sector, industry = get_ticker_basic(ticker)

    url = "http://shortvolumes.com/?t={}".format(ticker_selected)
    table = pd.read_html(url)
    shorted_vol_daily = table[3].loc[1:].to_html(index=False, header=False)
    shorted_vol_group = table[4].dropna().to_html(index=False, header=False)
    return render(request, 'short_volume.html', {"ticker_selected": ticker_selected,
                                                 "official_name": official_name,
                                                 "img": img,
                                                 "industry": industry,
                                                 "sector": sector,
                                                 "shorted_vol_daily": shorted_vol_daily,
                                                 "shorted_vol_group": shorted_vol_group})


def earnings_calendar(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    db.execute("SELECT * FROM earnings_calendar ORDER BY earning_date ASC")
    calendar = db.fetchall()
    calendar = list(map(list, calendar))

    return render(request, 'earnings_calendar.html', {"popular_ticker_list": popular_ticker_list,
                                                      "popular_name_list": popular_name_list,
                                                      "price_list": price_list, 
                                                      "earnings_calendar": calendar})


def reddit_analysis(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    if request.GET.get("subreddit"):
        subreddit = request.GET.get("subreddit").lower().replace(" ", "")
        if subreddit == "all":
            db.execute("SELECT * FROM reddit_trending ORDER BY score DESC")
        else:
            db.execute("SELECT * FROM {} ORDER BY recent DESC LIMIT 50".format(subreddit))
        trending_tickers = db.fetchall()
        database_mapping = {"wallstreetbets": "Wall Street Bets"}

        subreddit = database_mapping[subreddit]
        return render(request, 'reddit_sentiment.html', {"popular_ticker_list": popular_ticker_list,
                                                         "popular_name_list": popular_name_list,
                                                         "price_list": price_list,
                                                         "trending_tickers": trending_tickers,
                                                         "subreddit_selected": subreddit})
    else:
        return render(request, 'reddit_sentiment.html', {"popular_ticker_list": popular_ticker_list,
                                                         "popular_name_list": popular_name_list,
                                                         "price_list": price_list})


def subreddit_count(request):
    db.execute("SELECT * FROM subreddit_count")
    subscribers = db.fetchall()
    subscribers = list(map(list, subscribers))
    return render(request, 'subreddit_count.html', {"subscribers": subscribers})


def top_movers(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()

    top_gainers = pd.read_html("https://finance.yahoo.com/screener/predefined/day_gainers")[0]
    top_gainers["PE Ratio (TTM)"] = top_gainers["PE Ratio (TTM)"].replace(np.nan, "N/A")
    del top_gainers["52 Week Range"]

    top_losers = pd.read_html("https://finance.yahoo.com/screener/predefined/day_losers")[0]
    top_losers["PE Ratio (TTM)"] = top_gainers["PE Ratio (TTM)"].replace(np.nan, "N/A")
    del top_losers["52 Week Range"]

    return render(request, 'top_movers.html', {"popular_ticker_list": popular_ticker_list,
                                               "popular_name_list": popular_name_list,
                                               "price_list": price_list,
                                               "top_gainers": top_gainers.to_html(index=False),
                                               "top_losers": top_losers.to_html(index=False)})


def short_interest(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    df_high_short_interest = get_high_short_interest()
    return render(request, 'short_interest.html', {"popular_ticker_list": popular_ticker_list,
                                                   "popular_name_list": popular_name_list,
                                                   "price_list": price_list,
                                                   "df_high_short_interest": df_high_short_interest.to_html(index=False)})


def low_float(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    df_low_float = get_low_float()
    return render(request, 'low_float.html', {"popular_ticker_list": popular_ticker_list,
                                              "popular_name_list": popular_name_list,
                                              "price_list": price_list,
                                              "df_low_float": df_low_float.to_html(index=False)})


def penny_stocks(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    df_penny_stocks = get_penny_stocks()
    return render(request, 'penny_stocks.html', {"popular_ticker_list": popular_ticker_list,
                                                 "popular_name_list": popular_name_list,
                                                 "price_list": price_list,
                                                 "df_penny_stocks": df_penny_stocks.to_html(index=False)})


def ark_trades(request):
    return render(request, 'ark_trade.html')


def industries_analysis(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    screen = performance.Performance()
    sector = screen.ScreenerView(group="Sector")
    sector.drop(sector.columns[[7, 8, 9, 11]], axis=1, inplace=True)
    sector = sector.rename({'Change': 'Perf Day'}, axis=1)
    sector = sector[['Name', "Perf Day", "Perf Week", "Perf Month", "Perf Quart", "Perf Half", "Perf Year", "Perf YTD"]]
    wsb_df = pd.DataFrame({"Name": ["WSB"], "Perf Day": ["5%"], "Perf Week": ["5%"], "Perf Month": ["5%"], "Perf Quart": ["5%"], "Perf Half": ["5%"], "Perf Year": ["5"], "Perf YTD": ["5%"]})
    sector = wsb_df.append(sector, ignore_index=True)
    df_sector = sector.to_html(index=False)
    # df_screen = screen.ScreenerView(group="Industry")
    # print(df_screen)
    return render(request, 'industry.html', {"popular_ticker_list": popular_ticker_list,
                                             "popular_name_list": popular_name_list,
                                             "price_list": price_list,
                                             "df_sector": df_sector})


def reddit_etf(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    db.execute("SELECT * FROM wallstreetbets LIMIT 100")
    return render(request, 'reddit_etf.html', {"popular_ticker_list": popular_ticker_list,
                                               "popular_name_list": popular_name_list,
                                               "price_list": price_list})


def opinion(request):
    return render(request, 'opinion.html')


def about(request):
    return render(request, 'about.html')
