import os
import sqlite3
from datetime import datetime, timedelta

from custom_extensions.custom_words import *
from helpers import *

import pandas as pd
from pytrends.request import TrendReq
from yahoo_earnings_calendar import YahooEarningsCalendar
from finvizfinance.quote import finvizfinance

from django.shortcuts import render
from nltk.sentiment.vader import SentimentIntensityAnalyzer

conn = sqlite3.connect(r"scheduled_tasks/database.db", check_same_thread=False)
db = conn.cursor()

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

trends = TrendReq(hl='en-US', tz=360)


def main(request):
    return render(request, "home.html")


def stock_price(request):
    """
    Get price, graph and key statistics of a ticker. Data from yahoo finance
    """
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote']
        try:
            ticker = yf.Ticker(ticker_selected)
            # Display graph based on what user selects. Default is 1 day
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
                price_df = ticker.history(period="5y", interval="1wk").fillna(method="ffill")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "4"
            else:
                price_df = ticker.history(period="1d", interval="2m")
                ticker_date_max = list(map(lambda x: x.split()[1].split("-")[0].rsplit(":", 1)[0],
                                       price_df.index.astype(str).to_list()))
                duration = "0"

            # If price < $1, round to 4sf, else 2sf
            if price_df["Close"][0] <= 1:
                ticker_price_max = list(map(lambda x: round(x, 4), price_df["Close"].to_list()))
            else:
                ticker_price_max = list(map(lambda x: round(x, 2), price_df["Close"].to_list()))

            information = ticker.info

            return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected,
                                                         "ticker_date_max": ticker_date_max,
                                                         "ticker_price_max": ticker_price_max,
                                                         "duration": duration,
                                                         "information": information,
                                                         })
        except (IndexError, KeyError, Exception):
            return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected, "error": "error_true"})
    return render(request, 'ticker_price.html')


def ticker_recommendations(request):
    """
    Show upgrades/downgrades of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    try:
        recommendations = ticker.recommendations
        recommendations["Action"] = recommendations["Action"].str.replace("main", "Maintain").replace("up", "Upgrade").replace("down", "Downgrade").replace("init", "Initialised").replace("reit", "Reiterate")
        recommendations = recommendations.to_html(index=False)
    except TypeError:
        recommendations = "N/A"
    return render(request, 'iframe_format.html', {"title": "Recommendations",
                                                  "table": recommendations})


def ticker_major_holders(request):
    """
    Show major holders of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    major_holders = ticker.major_holders
    major_holders = major_holders.to_html(index=False, header=False)
    return render(request, 'iframe_format.html', {"title": "Major Holders", "table": major_holders})


def ticker_institutional_holders(request):
    """
    Show institutional holders of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    institutional_holders = ticker.institutional_holders
    if institutional_holders is not None:
        institutional_holders = institutional_holders.to_html(index=False)
    else:
        institutional_holders = "N/A"
    return render(request, 'iframe_format.html', {"title": "Institutional Holders", "table": institutional_holders})


def sub_news(request):
    """
    Show news and sentiment of ticker in /ticker?quote={TICKER}. Data from Finviz
    Note: News are only available if hosted locally. Read README.md for more details
    """
    ticker_selected = default_ticker(request)
    ticker_fin = finvizfinance(ticker_selected)

    news_df = ticker_fin.TickerNews()
    news_df["Date"] = news_df["Date"].dt.date
    link = news_df["Link"].to_list()
    del news_df["Link"]

    # Get sentiment of each news title and add it to a new column in news_df
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
    """
    Show news and sentiment of ticker in /latest_news?quote={TICKER}. Data from Finviz
    This is more detailed (graphs included) than sub_news()
    Note: News are only available if hosted locally. Read README.md for more details
    """
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

    db.execute("UPDATE news_sentiment SET sentiment=? WHERE ticker=? AND date_updated=?",
               (avg_score, ticker_selected, str(datetime.now()).split()[0]))
    conn.commit()

    db.execute("SELECT * FROM news_sentiment WHERE date_updated=?", (str(datetime.now()).split()[0],))
    ticker_sentiment = db.fetchall()
    days = 1
    while not ticker_sentiment:
        db.execute("SELECT * FROM news_sentiment WHERE date_updated=?", (str(datetime.now()-timedelta(days=days)).split()[0],))
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


def historical_data(request):
    """
    Allow users to filter/sort historical data of ticker
    """
    ticker_selected = default_ticker(request)

    if request.GET.get("sort"):
        sort_by = request.GET['sort'].replace("Sort By: ", "")
    else:
        sort_by = "Date"

    ticker = yf.Ticker(ticker_selected)
    price_df = ticker.history(period="1y", interval="1d").reset_index().iloc[::-1]

    del price_df["Dividends"]
    del price_df["Stock Splits"]

    # Add % Price Change, Amplitude, % Vol Change columns
    price_df["% Price Change"] = price_df["Close"].shift(-1)
    price_df["% Price Change"] = 100 * (price_df["Close"] - price_df["% Price Change"]) / price_df["% Price Change"]

    price_df["Amplitude"] = 100 * (price_df["High"] - price_df["Low"]) / price_df["Open"]

    price_df["% Vol Change"] = price_df["Volume"].shift(-1)
    price_df["% Vol Change"] = 100 * (price_df["Volume"] - price_df["% Vol Change"]) / price_df["% Vol Change"]

    if request.GET.get("order"):
        order = request.GET['order'].replace("Order: ", "")
    else:
        order = "Descending"

    if order == "Descending":
        price_df.sort_values(by=[sort_by], inplace=True, ascending=False)
    else:
        price_df.sort_values(by=[sort_by], inplace=True)

    price_df = price_df.round(2)
    price_df = price_df.fillna(0)
    price_df = price_df.to_html(index=False)

    return render(request, 'historical_data.html', {"ticker_selected": ticker_selected,
                                                    "sort_by": sort_by,
                                                    "order": order,
                                                    "price_df": price_df})


def google_trends(request):
    """
    Get trending of ticker in Google. Data is from Google
    """
    ticker_selected = default_ticker(request)

    # Remove -USD in crpyto
    if "-USD" in ticker_selected:
        ticker_selected = ticker_selected.split("-USD")[0]

    # Get timeframe of trends. Default is 12 months
    if request.GET.get("timing_selected"):
        timeframe = request.GET.get("timing_selected")
    else:
        timeframe = "today 12-m"

    # cat=7 refers to finance and investing section in Google
    trends.build_payload(kw_list=[ticker_selected], timeframe=timeframe, cat=7)
    interest_over_time = trends.interest_over_time().reset_index()

    # Sort trends by country level
    interest_by_region = trends.interest_by_region(resolution='COUNTRY', inc_low_vol=False, inc_geo_code=False).\
        reset_index().sort_values([ticker_selected], ascending=False).head(20).reset_index()
    region_list = interest_by_region["geoName"].to_list()
    region_count_list = interest_by_region[ticker_selected].to_list()

    # Map api variable to clearer format
    mapping_dict = {"now 1-H": "Past hour",
                    "now 4-H": "Past 4 hours",
                    "now 1-d": "Past day",
                    "now 7-d": "Past 7 days",
                    "today 1-m": "Past 30 days",
                    "today 3-m": "Past 90 days",
                    "today 12-m": "Past 12 months"}
    timeframe = mapping_dict[timeframe]

    return render(request, "google_trend.html", {"interest_over_time": interest_over_time.to_html(index=False),
                                                 "ticker_selected": ticker_selected,
                                                 "timing_selected": timeframe,
                                                 "region_list": region_list,
                                                 "region_count_list": region_count_list})


def financial(request):
    """
    Get balance sheet of company. Data is from yahoo finance
    """
    ticker_selected = default_ticker(request)
    balance_list = []
    ticker = yf.Ticker(ticker_selected)
    information = ticker.info

    # To check if input is a valid ticker
    if "symbol" in information:
        balance_sheet = ticker.quarterly_balance_sheet.replace(np.nan, 0)

        date_list = balance_sheet.columns.astype("str").to_list()
        balance_col_list = balance_sheet.index.tolist()

        for i in range(len(balance_sheet)):
            values = balance_sheet.iloc[i].tolist()
            balance_list.append(values)

        # Get Actual vs Est EPS of ticker
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

                    # Deduce financial quarter based on date of report
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
                                                  "information": information,
                                                  "date_list": date_list,
                                                  "balance_list": balance_list,
                                                  "balance_col_list": balance_col_list,
                                                  "earnings_list": earnings_list,
                                                  "financial_quarter_list": financial_quarter_list})
    else:
        return render(request, 'financial.html', {"ticker_selected": ticker_selected,
                                                  "error": "error_true"})


def options(request):
    """
    Get options (Max pain, option chain, C/P ratio) of ticker.
    """
    ticker_selected = default_ticker(request)
    try:
        ticker = yf.Ticker(ticker_selected)
        information = ticker.info

        options_dates = ticker.options
        if request.GET.get("date") not in ["", None]:
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

        calls["Bid"].fillna('-', inplace=True)
        calls["Ask"].fillna('-', inplace=True)
        calls["Volume"].fillna('-', inplace=True)
        calls["Open Interest"].fillna(0, inplace=True)
        calls["Implied Volatility"] = calls["Implied Volatility"].astype("float").multiply(100)

        calls["Change"] = calls["Change"].round(2)
        calls["% Change"] = calls["% Change"].round(2).fillna("-")
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

        puts["Bid"].fillna('-', inplace=True)
        puts["Ask"].fillna('-', inplace=True)
        puts["Volume"].fillna('-', inplace=True)
        puts["Open Interest"].fillna(0, inplace=True)
        puts["Implied Volatility"] = puts["Implied Volatility"].astype("float").multiply(100)

        puts["Change"] = puts["Change"].round(2)
        puts["% Change"] = puts["% Change"].round(2).fillna("-")
        puts["Implied Volatility"] = puts["Implied Volatility"].round(2)

        df_merge = pd.merge(calls, puts, on="Strike", how="outer")
        df_merge.sort_values(by=["Strike"], inplace=True)
        df_merge = df_merge[["Last Price_x", "Change_x", "% Change_x", "Volume_x", "Open Interest_x", "Strike",
                             "Last Price_y", "Change_y", "% Change_y", "Volume_y", "Open Interest_y"]]
        df_merge.columns = ["Last Price", "Change", "% Change", "Volume", "Open Interest", "Strike",
                            "Last Price", "Change", "% Change", "Volume", "Open Interest"]
        df_merge.fillna('-', inplace=True)

        df_opt = pd.merge(df_calls, df_puts, left_index=True, right_index=True)
        df_opt = df_opt[["Open Interest_x", "Open Interest_y"]].rename(
            columns={"Open Interest_x": "OI Calls", "Open Interest_y": "OI Puts"})
        max_pain, call_loss_list, put_loss_list = get_max_pain(df_opt)

        return render(request, 'options.html', {"ticker_selected": ticker_selected,
                                                "information": information,
                                                "options_dates": options_dates,
                                                "date_selected": date_selected,
                                                "max_pain": max_pain,
                                                "call_loss_list": call_loss_list,
                                                "put_loss_list": put_loss_list,
                                                "calls": calls.to_html(index=False),
                                                "puts": puts.to_html(index=False),
                                                "merge": df_merge.to_html(index=False)})
    except (IndexError, KeyError, Exception):
        return render(request, 'options.html', {"ticker_selected": ticker_selected, "error": "error_true"})


def short_volume(request):
    """
    Get short volume of tickers (only popular ones). Data from shortvolumes.com
    """
    ticker_selected = default_ticker(request)

    db.execute("SELECT * FROM short_volume WHERE ticker=? ORDER BY reported_date DESC", (ticker_selected,))
    short_volume_data = db.fetchall()
    if short_volume_data:
        ticker = yf.Ticker(ticker_selected)
        information = ticker.info
        short_volume_data = list(map(list, short_volume_data))
        return render(request, 'short_volume.html', {"ticker_selected": ticker_selected,
                                                     "information": information,
                                                     "short_volume_data": short_volume_data})
    else:
        return render(request, 'short_volume.html', {"ticker_selected": ticker_selected,
                                                     "short_volume_data": short_volume_data,
                                                     "error": "error_true"})


def failure_to_deliver(request):
    """
        Get FTD of tickers (only popular ones). Data from SEC
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    file_path = r"scheduled_tasks/failure_to_deliver/ticker/{}.csv".format(ticker_selected)
    if os.path.isfile(file_path):
        information = ticker.info
        ftd = pd.read_csv(file_path)
        ftd = ftd[::-1]
        del ftd["CUSIP"]
        del ftd["SYMBOL"]
        del ftd["DESCRIPTION"]
        return render(request, 'ftd.html', {"ticker_selected": ticker_selected,
                                            "information": information,
                                            "ftd": ftd.to_html(index=False)})
    else:
        return render(request, 'ftd.html', {"ticker_selected": ticker_selected, "error": "error_true"})


def earnings_calendar(request):
    """
    Get earnings for the upcoming week. Data from yahoo finance
    """
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    db.execute("SELECT * FROM earnings_calendar ORDER BY earning_date ASC")
    calendar = db.fetchall()
    calendar = list(map(list, calendar))

    return render(request, 'earnings_calendar.html', {"popular_ticker_list": popular_ticker_list,
                                                      "popular_name_list": popular_name_list,
                                                      "price_list": price_list, 
                                                      "earnings_calendar": calendar})


def reddit_analysis(request):
    """
    Get trending tickers on Reddit
    """
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    if request.GET.get("subreddit"):
        subreddit = request.GET.get("subreddit").lower().replace(" ", "")
        if ":" in subreddit:
            subreddit = subreddit.split(":")[1]
    else:
        subreddit = "wallstreetbets"

    db.execute("SELECT DISTINCT(date_updated) FROM {} ORDER BY ID DESC LIMIT 30".format(subreddit,))
    all_dates = db.fetchall()
    all_dates = list(map(convert_date, all_dates))

    if request.GET.get("date_selected"):
        date_selected = request.GET.get("date_selected")
        if ":" in date_selected:
            date_selected = date_selected.replace(" ", "").split(":")[1]
    else:
        date_selected = all_dates[0]

    db.execute("SELECT * FROM {} WHERE date_updated LIKE '{}' ORDER BY total DESC LIMIT 25".format(subreddit, "%" + date_selected + "%"))
    trending_tickers = db.fetchall()
    trending_tickers = list(map(list, trending_tickers))

    database_mapping = {"wallstreetbets": "Wall Street Bets",
                        "stocks": "Stocks",
                        "stockmarket": "Stock Market"}
    subreddit = database_mapping[subreddit]

    return render(request, 'reddit_sentiment.html', {"popular_ticker_list": popular_ticker_list,
                                                     "popular_name_list": popular_name_list,
                                                     "price_list": price_list,
                                                     "all_dates": all_dates,
                                                     "date_selected": date_selected,
                                                     "trending_tickers": trending_tickers,
                                                     "subreddit_selected": subreddit})


def subreddit_count(request):
    """
    Get subreddit user count, growth, active users over time.
    """
    db.execute("SELECT * FROM subreddit_count")
    subscribers = db.fetchall()
    subscribers = list(map(list, subscribers))
    return render(request, 'subreddit_count.html', {"subscribers": subscribers})


def top_movers(request):
    """
    Get top movers of ticker. Data is from yahoo finance
    """
    popular_ticker_list, popular_name_list, price_list = ticker_bar()

    top_gainers = pd.read_html("https://finance.yahoo.com/screener/predefined/day_gainers")[0]
    top_gainers["PE Ratio (TTM)"] = top_gainers["PE Ratio (TTM)"].replace(np.nan, "N/A")

    top_losers = pd.read_html("https://finance.yahoo.com/screener/predefined/day_losers")[0]
    top_losers["PE Ratio (TTM)"] = top_gainers["PE Ratio (TTM)"].replace(np.nan, "N/A")
    top_losers = top_losers.iloc[::-1]

    top_movers_combine = top_gainers.append(top_losers, ignore_index=True)
    del top_movers_combine["52 Week Range"]

    return render(request, 'top_movers.html', {"popular_ticker_list": popular_ticker_list,
                                               "popular_name_list": popular_name_list,
                                               "price_list": price_list,
                                               "top_movers_combine": top_movers_combine.to_html(index=False)})


def short_interest(request):
    """
    Get short interest of ticker. Data if from highshortinterest.com
    """
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    df_high_short_interest = pd.read_sql("SELECT * FROM short_interest", con=conn)
    return render(request, 'short_interest.html', {
                                                   "popular_ticker_list": popular_ticker_list,
                                                   "popular_name_list": popular_name_list,
                                                   "price_list": price_list,
                                                   "df_high_short_interest": df_high_short_interest.to_html(index=False)})


def low_float(request):
    """
    Get short interest of ticker. Data if from lowfloat.com
    """
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    df_low_float = pd.read_sql("SELECT * FROM low_float", con=conn)
    return render(request, 'low_float.html', {"popular_ticker_list": popular_ticker_list,
                                              "popular_name_list": popular_name_list,
                                              "price_list": price_list,
                                              "df_low_float": df_low_float.to_html(index=False)})


def ark_trades(request):
    """
    Get trades/positions of ARK Funds. Data from https://arkfunds.io/api
    """
    return render(request, 'ark_trade.html')


def reddit_etf(request):
    """
    Get ETF of r/wallstreetbets
    Top 10 tickers before market open will be purchased daily
    """
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    db.execute("SELECT * FROM reddit_etf WHERE status='Open' ORDER BY open_date DESC")
    open_trade = db.fetchall()

    db.execute("select sum(PnL) from reddit_etf WHERE status='Open'")
    unrealized_PnL = round(db.fetchone()[0], 2)

    db.execute("SELECT * FROM reddit_etf WHERE status='Close' ORDER BY close_date DESC")
    close_trade = db.fetchall()

    db.execute("select sum(PnL) from reddit_etf WHERE status='Close'")
    realized_PnL = round(db.fetchone()[0], 2)

    return render(request, 'reddit_etf.html', {"popular_ticker_list": popular_ticker_list,
                                               "popular_name_list": popular_name_list,
                                               "price_list": price_list,
                                               "open_trade": open_trade,
                                               "close_trade": close_trade,
                                               "unrealized_PnL": unrealized_PnL,
                                               "realized_PnL": realized_PnL})


def due_diligence(request):
    """
    Get a list of due diligence from different subreddits on Reddit. Data is sourced manually by me
    """
    db.execute("SELECT * FROM top_DD")
    dd = db.fetchall()
    dd = list(map(list, dd))
    return render(request, 'top_DD.html', {"due_diligence": dd})


def opinion(request):
    return render(request, 'opinion.html')


def about(request):
    """
    About section of the website and contact me if there's any issues/suggestions
    """
    if request.POST.get("name"):
        name = request.POST.get("name")
        email = request.POST.get("email")
        suggestions = request.POST.get("suggestions")
        db.execute("INSERT INTO contact VALUES (?, ?, ?)", (name, email, suggestions))
        conn.commit()
    return render(request, 'about.html')
