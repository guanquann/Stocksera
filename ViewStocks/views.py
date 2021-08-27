import math

from custom_extensions.custom_words import *
from custom_extensions.stopwords import *
from scheduled_tasks.get_popular_tickers import full_ticker_list
from email_server import *
from helpers import *

import requests_cache
import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq
from finvizfinance.quote import finvizfinance

from django.shortcuts import render
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# analyzer = SentimentIntensityAnalyzer()
# analyzer.lexicon.update(new_words)

trends = TrendReq(hl='en-US', tz=360)

pd.options.display.float_format = '{:.1f}'.format

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                'Chrome/91.0.4472.124 Safari/537.36'


def main(request):
    db.execute("SELECT * FROM stocksera_trending ORDER BY count DESC LIMIT 10")
    trending = db.fetchall()
    trending = list(map(list, trending))
    return render(request, "home.html", {"trending": trending})


def stock_price(request):
    """
    Get price and key statistics of a ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    information = check_market_hours(ticker, ticker_selected)
    symbol_list, description = get_all_tickers()
    if "symbol" in information:
        return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected,
                                                     "information": information,
                                                     "symbol_list": symbol_list,
                                                     "description": description
                                                     })
    else:
        return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected,
                                                     "error": "error_true"})


def ticker_recommendations(request):
    """
    Show upgrades/downgrades of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected, session=session)
    try:
        recommendations = ticker.recommendations
        recommendations["Action"] = recommendations["Action"].str.replace("main", "Maintain").replace("up", "Upgrade").replace("down", "Downgrade").replace("init", "Initialised").replace("reit", "Reiterate")
        recommendations.reset_index(inplace=True)
        recommendations["Date"] = recommendations["Date"].dt.date
        recommendations.sort_values(by=["Date"], ascending=False, inplace=True)
    except TypeError:
        recommendations = pd.DataFrame()
        recommendations["Date"] = ["N/A"]
        recommendations["Firm"] = ["N/A"]
        recommendations["To Grade"] = ["N/A"]
        recommendations["From Grade"] = ["N/A"]
        recommendations["Action"] = ["N/A"]
    return render(request, 'iframe_format.html', {"title": "Recommendations",
                                                  "table": recommendations[:100].to_html(index=False)})


def ticker_major_holders(request):
    """
    Show major holders of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected, session=session)
    try:
        major_holders = ticker.major_holders
        major_holders = major_holders.to_html(index=False, header=False)
    except (TypeError, AttributeError):
        major_holders = "N/A"
    return render(request, 'iframe_format.html', {"title": "Major Holders", "table": major_holders})


def ticker_institutional_holders(request):
    """
    Show institutional holders of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected, session=session)
    institutional_holders = ticker.institutional_holders
    if institutional_holders is not None:
        try:
            institutional_holders.columns = (institutional_holders.columns.str.replace("% Out", "Stake"))
            institutional_holders["Stake"] = institutional_holders["Stake"].apply(lambda x: str(f"{100 * x:.2f}") + "%")
            institutional_holders["Value"] = institutional_holders["Value"].apply(lambda x: "$" + str(x))
        except AttributeError:
            institutional_holders = pd.DataFrame()
            institutional_holders["Holder"] = ["N/A"]
            institutional_holders["Shares"] = ["N/A"]
            institutional_holders["Date Reported"] = ["N/A"]
            institutional_holders["Stake"] = ["N/A"]
            institutional_holders["Value"] = ["N/A"]
    else:
        institutional_holders = pd.DataFrame()
        institutional_holders["Holder"] = ["N/A"]
        institutional_holders["Shares"] = ["N/A"]
        institutional_holders["Date Reported"] = ["N/A"]
        institutional_holders["Stake"] = ["N/A"]
        institutional_holders["Value"] = ["N/A"]
    return render(request, 'iframe_format.html', {"title": "Institutional Holders",
                                                  "table": institutional_holders.to_html(index=False)})


def ticker_mutual_fund_holders(request):
    """
        Show mutual funds holders of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected, session=session)
    mutual_fund_holders = ticker.mutualfund_holders
    if mutual_fund_holders is not None:
        mutual_fund_holders.columns = (mutual_fund_holders.columns.str.replace("% Out", "Stake"))
        mutual_fund_holders["Stake"] = mutual_fund_holders["Stake"].apply(lambda x: str(f"{100 * x:.2f}") + "%")
        mutual_fund_holders["Value"] = mutual_fund_holders["Value"].apply(lambda x: "$" + str(x))
    else:
        mutual_fund_holders = pd.DataFrame()
        mutual_fund_holders["Holder"] = ["N/A"]
        mutual_fund_holders["Shares"] = ["N/A"]
        mutual_fund_holders["Date Reported"] = ["N/A"]
        mutual_fund_holders["Stake"] = ["N/A"]
        mutual_fund_holders["Value"] = ["N/A"]
    return render(request, 'iframe_format.html', {"title": "MutualFund Holders",
                                                  "table": mutual_fund_holders.to_html(index=False)})


def dividend_and_split(request):
    """
        Show dividend and split of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected, session=session)
    df = ticker.actions
    if df is not None:
        df["Dividends"] = "$" + df["Dividends"].astype(str)
        df.sort_values(by=["Date"], ascending=False, inplace=True)
        df = df.reset_index().to_html(index=False)
    else:
        df = "N/A"
    return render(request, 'iframe_format.html', {"title": "Dividend & Split", "table": df})


def ticker_earnings(request):
    """
    Show historical earnings of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected, session=session)
    past_df = ticker.earnings
    if not past_df.empty:
        past_df.reset_index(inplace=True)
        past_df.sort_values(by=["Year"], ascending=False, inplace=True)
    else:
        past_df = pd.DataFrame(columns=["Year", "Revenue", "Earnings"])
        past_df["Year"] = ["2021", "2020", "2019", "2018"]
        past_df["Revenue"] = ["N/A", "N/A", "N/A", "N/A"]
        past_df["Earnings"] = ["N/A", "N/A", "N/A", "N/A"]

    next_df = ticker.calendar
    next_df.fillna("N/A", inplace=True)
    if not next_df.empty:
        next_df.iloc[0, 0] = next_df.iloc[0, 0].date().strftime("%d/%m/%Y")
        next_df.rename(index={"Earnings Low": "EPS Low", "Earnings High": "EPS High",
                              "Earnings Average": "EPS Average"}, inplace=True)
        next_df = pd.DataFrame(next_df.iloc[:, 0]).reset_index()
        next_df.rename(columns={"index": "", 0: "Estimate"}, inplace=True)
    else:
        next_df = pd.DataFrame(columns=["Next Earning", "Estimate"])
        next_df["Next Earning"] = ["Earning Date", "EPS Average", "EPS Low", "EPS High", "Revenue Average", "Revenue Low",
                                   "Revenue High"]
        next_df["Estimate"] = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    return render(request, 'ticker_earnings.html', {"ticker_selected": ticker_selected,
                                                    "ticker_earnings": past_df.to_html(index=False),
                                                    "ticker_next_earnings": next_df.to_html(index=False)})


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
    information = check_market_hours(ticker, ticker_selected)

    # To check if input is a valid ticker
    if "symbol" in information:
        ticker_fin = finvizfinance(ticker_selected)

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
                                                       "information": information,
                                                       "news_df": news_df.to_html(index=False),
                                                       "link": link,
                                                       "ticker_sentiment": ticker_sentiment,
                                                       "latest_date": latest_date,
                                                       "avg_score": avg_score})
    else:
        included_list = ", ".join(sorted(full_ticker_list()))
        return render(request, 'news_sentiment.html', {"ticker_selected": ticker_selected,
                                                       "included_list": included_list,
                                                       "error": "error_true"})


def historical_data(request):
    """
    Allow users to filter/sort historical data of ticker
    """
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(request)
    if request.GET.get("sort"):
        sort_by = request.GET['sort'].replace("Sort By: ", "")
    else:
        sort_by = "Date"

    if request.GET.get("timeframe"):
        timeframe = request.GET['timeframe'].replace("Timeframe: ", "")
    else:
        timeframe = "1Y"

    ticker = yf.Ticker(ticker_selected)
    price_df = ticker.history(period=timeframe.lower(), interval="1d").reset_index().iloc[::-1]

    del price_df["Dividends"]
    del price_df["Stock Splits"]

    # Add % Price Change, Amplitude, % Vol Change columns
    price_df["% Price Change"] = price_df["Close"].shift(-1)
    price_df["% Price Change"] = 100 * (price_df["Close"] - price_df["% Price Change"]) / price_df["% Price Change"]

    price_df["Amplitude"] = 100 * (price_df["High"] - price_df["Low"]) / price_df["Open"]

    price_df["% Vol Change"] = price_df["Volume"].shift(-1)
    price_df["% Vol Change"] = 100 * (price_df["Volume"] - price_df["% Vol Change"]) / price_df["% Vol Change"]

    price_df["Volume / % Price Ratio"] = round(price_df["Volume"] / price_df["% Price Change"].abs())
    price_df.insert(0, 'Day', price_df["Date"].dt.day_name())

    if request.GET.get("order"):
        order = request.GET['order'].replace("Order: ", "")
    else:
        order = "Descending"

    if order == "Descending":
        price_df.sort_values(by=[sort_by], inplace=True, ascending=False)
    else:
        price_df.sort_values(by=[sort_by], inplace=True)

    price_df = price_df.round(2)
    price_df = price_df.replace([np.inf, -np.inf], np.nan)
    price_df = price_df.fillna(0)
    latest_date = price_df["Date"].astype(str).max()

    if "download_csv" in request.GET:
        file_name = "{}_historical_{}.csv".format(ticker_selected, timeframe)
        response = download_file(price_df, file_name)
        return response

    price_df.index = np.arange(1, len(price_df) + 1)
    price_df.reset_index(inplace=True)
    price_df.rename(columns={"index": "Rank"}, inplace=True)
    price_df = price_df.to_html(index=False)

    return render(request, 'historical_data.html', {"ticker_selected": ticker_selected,
                                                    "sort_by": sort_by,
                                                    "order": order,
                                                    "timeframe": timeframe,
                                                    "latest_date": latest_date,
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
    ticker = yf.Ticker(ticker_selected)

    information = check_market_hours(ticker, ticker_selected)

    # quarterly_cashflow = ticker.quarterly_cashflow
    # print(quarterly_cashflow)
    # for i in quarterly_cashflow.index.to_list():
    #     print(i)

    # To check if input is a valid ticker
    if "symbol" in information:
        current_datetime = str(datetime.utcnow().date())
        with open(r"database/financials.json", "r+") as r:
            data = json.load(r)
            if ticker_selected in data:
                to_update_date = data[ticker_selected]["next_update"]
                if current_datetime > to_update_date:
                    date_list, balance_list, balance_col_list = check_financial_data(ticker_selected, ticker, data, r)
                else:
                    date_list = data[ticker_selected]["date_list"]
                    balance_list = data[ticker_selected]["balance_list"]
                    balance_col_list = data[ticker_selected]["balance_col_list"]
            else:
                date_list, balance_list, balance_col_list = check_financial_data(ticker_selected, ticker, data, r)
        return render(request, 'financial.html', {"ticker_selected": ticker_selected,
                                                  "information": information,
                                                  "date_list": date_list,
                                                  "balance_list": balance_list,
                                                  "balance_col_list": balance_col_list})
    else:
        return render(request, 'financial.html', {"ticker_selected": ticker_selected,
                                                  "error": "error_true"})


def options(request):
    """
    Get options (Max pain, option chain, C/P ratio) of ticker.
    """
    pd.options.display.float_format = '{:.1f}'.format
    ticker_selected = default_ticker(request)
    try:
        ticker = yf.Ticker(ticker_selected)

        information = check_market_hours(ticker, ticker_selected)

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

        last_adj_close_price = float(information['previousClose'])
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

    sql_query = "SELECT * FROM short_volume WHERE ticker='{}' ORDER BY reported_date DESC".format(ticker_selected)
    db.execute(sql_query)
    short_volume_data = db.fetchall()
    if short_volume_data:
        ticker = yf.Ticker(ticker_selected)
        information = check_market_hours(ticker, ticker_selected)
        short_volume_data = list(map(list, short_volume_data))

        if "download_csv" in request.GET:
            file_name = "{}_short_volume.csv".format(ticker_selected)
            ftd_df = pd.read_sql_query(sql_query, conn)
            ftd_df.to_csv(file_name, index=False)
            response = download_file(ftd_df, file_name)
            return response

        return render(request, 'short_volume.html', {"ticker_selected": ticker_selected,
                                                     "information": information,
                                                     "short_volume_data": short_volume_data})
    else:
        included_list = ", ".join(sorted(full_ticker_list()))
        return render(request, 'short_volume.html', {"ticker_selected": ticker_selected,
                                                     "short_volume_data": short_volume_data,
                                                     "error": "error_true",
                                                     "included_list": included_list})


def failure_to_deliver(request):
    """
    Get FTD of tickers. Data from SEC
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)
    file_path = r"database/failure_to_deliver/ftd.csv"
    if os.path.isfile(file_path):
        information = check_market_hours(ticker, ticker_selected)
        ftd = pd.read_csv(file_path)
        ftd = ftd[ftd["Symbol"] == ticker_selected]
        ftd = ftd[::-1]
        ftd["Amount (FTD x $)"] = (ftd["Failure to Deliver"].astype(int) * ftd["Price"].astype(float)).astype(int)
        del ftd["Symbol"]

        if "download_csv" in request.GET:
            file_name = "{}_ftd.csv".format(ticker_selected)
            ftd.to_csv(file_name, index=False)
            response = download_file(ftd, file_name)
            return response

        return render(request, 'ftd.html', {"ticker_selected": ticker_selected,
                                            "information": information,
                                            "90th_percentile": ftd["Amount (FTD x $)"].quantile(0.90),
                                            "ftd": ftd.to_html(index=False)})
    else:
        included_list = ", ".join(sorted(full_ticker_list()))
        return render(request, 'ftd.html', {"ticker_selected": ticker_selected,
                                            "error": "error_true",
                                            "included_list": included_list})


def earnings_calendar(request):
    """
    Get earnings for the upcoming week. Data from yahoo finance
    """
    db.execute("SELECT * FROM earnings_calendar ORDER BY earning_date ASC")
    calendar = db.fetchall()
    calendar = list(map(list, calendar))

    return render(request, 'earnings_calendar.html', {"earnings_calendar": calendar})


def hedge_funds(request):
    """
    Get holdings of top hedge funds in the world. Data is from whalewisdom
    """
    if request.GET.get("fund_name"):
        fund_name = request.GET.get("fund_name").replace("Hedge Fund: ", "")
    else:
        fund_name = "CITADEL ADVISORS LLC"

    if request.GET.get("sort_by"):
        selected_sort = request.GET.get("sort_by").replace("Sort By: ", "")
        page_num = int(request.GET.get("page_num"))
    else:
        selected_sort = "Rank"
        page_num = 1

    # hedge_funds_description.json remember to change the file name to the csv's file you have saved
    with open(r"database/hedge_funds_holdings/hedge_funds_description.json") as r:
        hedge_funds_holdings = json.load(r)["hedge funds"]

    ticker_selected = ""
    if request.GET.get("quote"):
        ticker_selected = request.GET.get("quote").upper()

    all_fund_names = []
    for fund in hedge_funds_holdings:
        all_fund_names.append(fund["name"])
        if fund["name"] == fund_name:
            df = pd.read_csv(r"database/hedge_funds_holdings/{}".format(fund["file_name"]))
            if ticker_selected != "":
                num_pages = 1
                df = df[df["Ticker"] == ticker_selected]
            else:
                num_pages = math.ceil(len(df) / 100)
                if len(df) > 100:
                    df = df[page_num*100-100:page_num*100]

            df = df.sort_values(by=[selected_sort])  # ascending=False
            df = df.replace(np.nan, "N/A")
            description = fund
            sort_by = df.columns

    return render(request, 'hedge_funds.html', {"df": df.to_html(index=False),
                                                "description": description,
                                                "all_fund_names": all_fund_names,
                                                "ticker_selected": ticker_selected,
                                                "sort_by": sort_by,
                                                "selected_sort": selected_sort,
                                                "page_num": page_num,
                                                "num_pages": num_pages})


def reddit_analysis(request):
    """
    Get trending tickers on Reddit
    """
    if request.GET.get("subreddit"):
        subreddit = request.GET.get("subreddit").lower().replace(" ", "")
        if ":" in subreddit:
            subreddit = subreddit.split(":")[1]
    else:
        subreddit = "wallstreetbets"

    db.execute("SELECT DISTINCT(date_updated) FROM {} ORDER BY ID DESC LIMIT 14".format(subreddit,))
    all_dates = db.fetchall()
    all_dates = list(map(convert_date, all_dates))

    if request.GET.get("date_selected"):
        date_selected = request.GET.get("date_selected")
        if ":" in date_selected:
            date_selected = date_selected.replace(" ", "").split(":")[1]
    else:
        date_selected = all_dates[0]

    db.execute("SELECT * FROM {} WHERE date_updated LIKE '{}' ORDER BY rank ASC LIMIT 35".format(subreddit, "%" + date_selected + "%"))
    trending_tickers = db.fetchall()
    trending_tickers = list(map(list, trending_tickers))

    if subreddit == "cryptocurrency":
        return render(request, 'cryptocurrency.html', {"date_selected": date_selected,
                                                       "all_dates": all_dates,
                                                       "trending_tickers": trending_tickers})

    database_mapping = {"wallstreetbets": "Wall Street Bets",
                        "stocks": "Stocks",
                        "stockmarket": "Stock Market",
                        "options": "Options",
                        "investing": "Investing",
                        "pennystocks": "Pennystocks"}
    subreddit = database_mapping[subreddit]

    return render(request, 'reddit_sentiment.html', {"all_dates": all_dates,
                                                     "date_selected": date_selected,
                                                     "trending_tickers": trending_tickers,
                                                     "subreddit_selected": subreddit,
                                                     "banned_words": sorted(stopwords_list)})


def reddit_ticker_analysis(request):
    """
    Get analysis of ranking of tickers in popular subreddits and compare it with its price
    """
    if request.GET.get("quote"):
        ticker_selected = request.GET.get("quote").upper()
    else:
        ticker_selected = "GME"
    if request.GET.get("subreddit"):
        subreddit = request.GET.get("subreddit").replace("Subreddit: ", "").replace(" ", "").lower()
    else:
        subreddit = "wallstreetbets"

    db.execute("SELECT rank, total, price, date_updated from {} WHERE ticker=? and rank != 0".format(subreddit),
               (ticker_selected,))
    ranking = db.fetchall()

    if subreddit != "cryptocurrency":
        ticker = yf.Ticker(ticker_selected)
        information = check_market_hours(ticker, ticker_selected)
        return render(request, 'reddit_stocks_analysis.html', {"ticker_selected": ticker_selected,
                                                               "information": information,
                                                               "ranking": ranking,
                                                               "subreddit": subreddit})
    else:
        return render(request, 'reddit_crypto_analysis.html', {"ticker_selected": ticker_selected,
                                                               "ranking": ranking})


def reddit_etf(request):
    """
    Get ETF of r/wallstreetbets
    Top 10 tickers before market open will be purchased daily
    """
    db.execute("SELECT * FROM reddit_etf WHERE status='Open' ORDER BY open_date DESC")
    open_trade = db.fetchall()

    db.execute("select sum(PnL) from reddit_etf WHERE status='Open'")
    unrealized_PnL = round(db.fetchone()[0], 2)

    db.execute("SELECT * FROM reddit_etf WHERE status='Close' ORDER BY close_date DESC")
    close_trade = db.fetchall()

    db.execute("select sum(PnL) from reddit_etf WHERE status='Close'")
    realized_PnL = round(db.fetchone()[0], 2)

    return render(request, 'reddit_etf.html', {"open_trade": open_trade,
                                               "close_trade": close_trade,
                                               "unrealized_PnL": unrealized_PnL,
                                               "realized_PnL": realized_PnL})


def subreddit_count(request):
    """
    Get subreddit user count, growth, active users over time.
    """
    db.execute("SELECT * FROM subreddit_count WHERE subreddit in ('wallstreetbets', 'StockMarket', 'stocks', "
               "'investing', 'amcstock', 'Superstonk', 'GME', 'options','pennystocks', 'cryptocurrency')")
    subscribers = db.fetchall()
    subscribers = list(map(list, subscribers))
    return render(request, 'subreddit_count.html', {"subscribers": subscribers})


def market_overview(request):
    """
    Get top movers of ticker. Data is from yahoo finance. Data is cached every 5 minutes to prevent excessive API usage.
    """
    return render(request, 'market_overview.html')


def reverse_repo(request):
    """
    Get reverse repo. Data is from https://apps.newyorkfed.org/markets/autorates/tomo-results-display?SHOWMORE=TRUE&startDate=01/01/2000&enddate=01/01/2000
    """
    pd.options.display.float_format = '{:.2f}'.format
    reverse_repo_stats = pd.read_sql_query("SELECT * FROM reverse_repo", conn)
    reverse_repo_stats.rename(columns={"record_date": "Date", "amount": "Amount", "parties": "Num Parties",
                                       "average": "Average"}, inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'reverse_repo.html', {"reverse_repo_stats": reverse_repo_stats[::-1].to_html(index=False),
                                                 "next_date": data})


def daily_treasury(request):
    """
    Get daily treasury. Data is from https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/operating-cash-balance
    """
    pd.options.display.float_format = '{:.2f}'.format
    daily_treasury_stats = pd.read_sql_query("SELECT * FROM daily_treasury", conn)
    daily_treasury_stats.rename(columns={"record_date": "Date", "close_today_bal": "Close Balance",
                                         "open_today_bal": "Open Balance", "amount_change": "Amount Change",
                                         "percent_change": "Percent Change"},
                                inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'daily_treasury.html', {"daily_treasury_stats":
                                                       daily_treasury_stats[::-1].to_html(index=False),
                                                   "next_date": data})


def inflation(request):
    """
    Get inflation. Data is from https://www.usinflationcalculator.com/inflation/current-inflation-rates/
    """
    pd.options.display.float_format = '{:.1f}'.format
    inflation_stats = pd.read_sql_query("SELECT * FROM inflation", conn).to_html(index=False)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'inflation.html', {"inflation_stats": inflation_stats, "next_date": data})


def retail_sales(request):
    """
    Get retail sales. Data is from https://ycharts.com/indicators/us_retail_and_food_services_sales
    """
    pd.options.display.float_format = '{:.2f}'.format
    retail_stats = pd.read_sql_query("SELECT * FROM retail_sales", conn)
    retail_stats.rename(columns={"record_date": "Date", "value": "Amount", "percent_change": "Percent Change",
                                 "covid_monthly_avg": "Covid Monthly Average Cases"}, inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'retail_sales.html', {"retail_stats": retail_stats[::-1].to_html(index=False),
                                                 "next_date": data})


def short_interest(request):
    """
    Get short interest of ticker. Data if from highshortinterest.com
    """
    pd.options.display.float_format = '{:.2f}'.format
    df_high_short_interest = pd.read_sql("SELECT * FROM short_interest", con=conn)
    df_high_short_interest.reset_index(inplace=True)
    df_high_short_interest.rename(columns={"index": "Rank"}, inplace=True)
    df_high_short_interest["Rank"] = df_high_short_interest["Rank"] + 1
    return render(request, 'short_interest.html', {"df_high_short_interest": df_high_short_interest.to_html(index=False)})


def low_float(request):
    """
    Get short interest of ticker. Data if from lowfloat.com
    """
    pd.options.display.float_format = '{:.2f}'.format
    df_low_float = pd.read_sql("SELECT * FROM low_float", con=conn)
    df_low_float.reset_index(inplace=True)
    df_low_float.rename(columns={"index": "Rank"}, inplace=True)
    df_low_float["Rank"] = df_low_float["Rank"] + 1
    return render(request, 'low_float.html', {"df_low_float": df_low_float.to_html(index=False)})


def ark_trades(request):
    """
    Get trades/positions of ARK Funds. Data from https://arkfunds.io/api
    """
    return render(request, 'ark_trade.html')


def amd_xlnx_ratio(request):
    pd.options.display.float_format = '{:.4f}'.format
    combined_df = pd.DataFrame()
    amd_df = yf.Ticker("AMD").history(interval="1d", period="1y")
    xlnx_df = yf.Ticker("XLNX").history(interval="1d", period="1y")

    combined_df["AMD Price (Close)"] = amd_df["Close"].round(2)
    combined_df["XLNX Price (Close)"] = xlnx_df["Close"].round(2)
    combined_df["XLNX % Upside"] = 100 * ((1.7234 * combined_df["AMD Price (Close)"]) / combined_df["XLNX Price (Close)"] - 1)
    combined_df["Ratio"] = combined_df["XLNX Price (Close)"] / combined_df["AMD Price (Close)"]
    combined_df["Ratio"] = combined_df["Ratio"].round(4)
    combined_df.reset_index(inplace=True)
    combined_df.rename(columns={"index": "Date"}, inplace=True)
    combined_df = combined_df[combined_df["Date"] >= "2020-10-30"]
    return render(request, 'amd_xlnx_ratio.html', {"combined_df": combined_df[::-1].to_html(index=False)})


def beta(request):
    pd.options.display.float_format = '{:.3f}'.format
    ticker_interested = default_ticker(request)
    if request.GET.get("quote2"):
        default = request.GET['quote2'].upper().replace(" ", "")
    else:
        default = "SPY"

    if request.GET.get("timeframe"):
        timeframe = request.GET['timeframe'].replace("Timeframe: ", "").replace(" Year", "y").replace(" Months", "mo")
    else:
        timeframe = "5y"

    if request.GET.get("interval"):
        interval = request.GET['interval'].replace("Interval: ", "").replace("Monthly", "1mo").replace("Daily", "1d")
    else:
        interval = "1mo"

    df = pd.DataFrame()
    df1 = yf.Ticker(ticker_interested).history(interval=interval, period=timeframe)
    df2 = yf.Ticker(default).history(interval=interval, period=timeframe)

    df[ticker_interested] = df1["Close"]
    df[default] = df2["Close"]

    price_change = df.pct_change()
    price_change.dropna(inplace=True)

    price_change.reset_index(inplace=True)

    coef = linear_regression(price_change[default].values, price_change[ticker_interested].values)
    price_change[ticker_interested] = price_change[ticker_interested] * 100
    price_change[default] = price_change[default] * 100

    return render(request, 'beta.html', {"beta": round(coef, 3),
                                         "ticker_selected": ticker_interested,
                                         "ticker_selected2": default,
                                         "price_change": price_change[::-1].to_html(index=False),
                                         "timeframe": timeframe.replace("mo", " Months").replace("y", " Year"),
                                         "interval": interval.replace("1mo", "Monthly").replace("1d", "Daily")})


def about(request):
    """
    About section of the website and contact me if there's any issues/suggestions
    """
    if request.POST.get("name"):
        name = request.POST.get("name")
        email = request.POST.get("email")
        suggestions = request.POST.get("suggestions")
        send_email(name, email, suggestions)
    return render(request, 'about.html')
