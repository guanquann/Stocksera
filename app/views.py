from helpers import *
from tasks_to_run import *
from scheduled_tasks.reddit.get_subreddit_count import *

import requests
import requests_cache
import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq

from django.shortcuts import render

try:
    session = requests.Session()
    session.get('https://trends.google.com')
    cookies_map = session.cookies.get_dict()
    nid_cookie = cookies_map['NID']
    trends = TrendReq(hl='en-US', tz=360, retries=3, requests_args={'headers': {'Cookie': f'NID={nid_cookie}'}})
except:
    print("Timeout for Google Trend")

pd.options.display.float_format = '{:.1f}'.format

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = header['User-Agent']

stopwords_list = json.load(open("custom_extensions/stopwords.json"))["stopwords_list"]


def main(request):
    trending = []
    data = requests.get(f"{BASE_URL}/stocksera_trending", headers=HEADERS).json()[:10]
    for i in data:
        trending.append([i["ticker"], i["name"]])

    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper().replace(" ", "")
        information, related_tickers = check_market_hours(ticker_selected)
        if "longName" in information and information["regularMarketPrice"] != "N/A":
            return render(request, 'stock/ticker_price.html', {"ticker_selected": ticker_selected,
                                                               "information": information,
                                                               "related_tickers": related_tickers,
                                                               })
    return render(request, "home/home.html", {"trending": trending})


def stock_price(request):
    """
    Get price and key statistics of a ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)
    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        return render(request, 'stock/ticker_price.html', {"ticker_selected": ticker_selected,
                                                           "information": information,
                                                           "related_tickers": related_tickers,
                                                           })
    else:
        return render(request, 'stock/ticker_price.html', {"ticker_selected": ticker_selected,
                                                           "error": "error_true"})


def ticker_recommendations(request):
    """
    Show upgrades/downgrades of ticker. Data from yahoo finance
    """
    ticker_selected = default_ticker(request)

    df = pd.DataFrame(finnhub_client.recommendation_trends(symbol=ticker_selected))
    df = df[["strongBuy", "buy", "hold", "sell", "strongSell", "period"]]
    df.columns = ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell", "Period"]
    return render(request, 'stock/recommendations.html', {"table": df.to_html(index=False)})


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
    return render(request, 'stock/shareholders.html', {"title": "Institutional Holders",
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
    else:
        mutual_fund_holders = pd.DataFrame()
        mutual_fund_holders["Holder"] = ["N/A"]
        mutual_fund_holders["Shares"] = ["N/A"]
        mutual_fund_holders["Date Reported"] = ["N/A"]
        mutual_fund_holders["Stake"] = ["N/A"]
        mutual_fund_holders["Value"] = ["N/A"]
    return render(request, 'stock/shareholders.html', {"title": "MutualFund Holders",
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
        df = df.reset_index()
    else:
        df = pd.DataFrame()
        df["Date"] = ["N/A"]
        df["Dividends"] = ["N/A"]
        df["Stock Splits"] = ["N/A"]
    return render(request, 'iframe_format.html', {"title": "Dividend & Split", "table": df.to_html(index=False)})


def tradingview(request):
    ticker_selected = default_ticker(request)
    return render(request, 'stock/tradingview.html', {"ticker_selected": ticker_selected})


def discussion(request):
    ticker_selected = default_ticker(request)
    return render(request, 'stock/discussion.html', {"ticker_selected": ticker_selected})


def sec_fillings(request):
    """
    Get SEC filling from Finnhub of ticker selected
    """
    ticker_selected = default_ticker(request)
    df = get_stocksera_request(f"stocks/sec_fillings/{ticker_selected}")
    return render(request, 'stock/sec_fillings.html', {"sec_fillings_df": df.to_html(index=False)})


def news_sentiment(request):
    """
    Show news and sentiment of ticker data from Finviz
    """
    ticker_selected = default_ticker(request)
    df = get_stocksera_request(f"stocks/news_sentiment/{ticker_selected}")
    return render(request, 'stock/recent_news.html', {"title": "News", "recent_news_df": df.to_html(index=False)})


def stock_insider_trading(request):
    """
    Get a specific ticker's insider trading data from Finviz
    """
    ticker_selected = default_ticker(request)
    df = get_stocksera_request(f"stocks/insider_trading/{ticker_selected}")
    if df.empty:
        df = pd.DataFrame([{"Name": "N/A", "Relationship": "N/A", "Date": "N/A"}])
    return render(request, 'stock/insider_trading.html', {"inside_trader_df": df.to_html(index=False)})


def latest_insider(request):
    """
    Get the latest insider trading data from Finviz and perform analysis
    """
    recent_activity = get_stocksera_request(f"discover/latest_insider/?limit=2000")
    insider_analysis = get_stocksera_request(f"discover/latest_insider_summary")
    return render(request, 'discover/latest_insider_trading.html',
                  {"insider_analysis": insider_analysis.to_html(index=False),
                   "recent_activity": recent_activity.to_html(index=False)})


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

    price_df = price_df.round(2)
    price_df = price_df.replace([np.inf, -np.inf], np.nan)
    price_df = price_df.fillna(0)
    latest_date = price_df["Date"].astype(str).max()

    if "download_csv" in request.GET:
        file_name = "{}_historical_{}.csv".format(ticker_selected, timeframe)
        response = download_file(price_df, file_name)
        return response

    summary_df = price_df.head(50).groupby(["Day"]).mean()
    summary_df.reset_index(inplace=True)
    summary_df = summary_df.groupby(['Day']).sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    summary_df.reset_index(inplace=True)
    summary_df = pd.DataFrame(summary_df[["Day", "% Price Change"]]).to_html(index=False)

    if order == "Descending":
        price_df.sort_values(by=[sort_by], inplace=True, ascending=False)
    else:
        price_df.sort_values(by=[sort_by], inplace=True)

    price_df.reset_index(inplace=True, drop=True)
    price_df.index = np.arange(1, len(price_df) + 1)
    price_df.reset_index(inplace=True)
    price_df.rename(columns={"index": "Rank"}, inplace=True)
    price_df = price_df.to_html(index=False)

    return render(request, 'stock/historical_data.html', {"ticker_selected": ticker_selected,
                                                          "sort_by": sort_by,
                                                          "order": order,
                                                          "timeframe": timeframe,
                                                          "latest_date": latest_date,
                                                          "price_df": price_df,
                                                          "summary_df": summary_df})


def google_trends(request):
    """
    Get trending of ticker in Google. Data is from Google
    """
    ticker_selected = default_ticker(request)

    # Remove -USD in crypto
    if "-USD" in ticker_selected:
        ticker_selected = ticker_selected.split("-USD")[0]

    # Get timeframe of trends. Default is 12 months
    if request.GET.get("timing_selected"):
        timeframe = request.GET.get("timing_selected")
    else:
        timeframe = "today 12-m"

    # cat=7 refers to finance and investing section in Google
    trends.build_payload(kw_list=[ticker_selected], timeframe=timeframe)
    interest_over_time = trends.interest_over_time().reset_index()

    interest_over_time = interest_over_time.rename(columns={ticker_selected: "score"})

    if interest_over_time.empty:
        interest_over_time = pd.DataFrame(columns=["date", "score"])
    if timeframe == "today 12-m":
        interval = "1wk"
        interest_over_time["date"] = interest_over_time["date"] + timedelta(days=1)
    else:
        interval = "1d"

    history_df = yf.Ticker(ticker_selected).history(period="1y", interval=interval)
    interest_over_time = pd.merge(interest_over_time, history_df, right_on=["Date"],
                                  left_on=["date"])[["date", "score", "Close"]]

    # Map api variable to clearer format
    mapping_dict = {"today 1-m": "Past 30 days",
                    "today 3-m": "Past 90 days",
                    "today 12-m": "Past 12 months"}
    timeframe = mapping_dict[timeframe]
    return render(request, "stock/google_trend.html", {"interest_over_time": interest_over_time.to_html(index=False),
                                                       "ticker_selected": ticker_selected,
                                                       "timing_selected": timeframe,
                                                       })


def options(request):
    """
    Get options chain from Swaggystock
    """
    ticker_selected = default_ticker(request)
    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        options_data = requests.get(f"https://api.swaggystocks.com/stocks/options/maxPain/"
                                    f"{ticker_selected}").json()["maxPain"]

        if not options_data:
            return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                          "information": information,
                                                          "options_data": [],
                                                          "historical_options_data": [],
                                                          "current_price": information["regularMarketPrice"],
                                                          "expiry_date": [],
                                                          "error": "error_true",
                                                          "error_msg": f"{ticker_selected} has no option data."})

        historical_options_data = requests.get(f"https://api.swaggystocks.com/stocks/options/maxPain/"
                                               f"{ticker_selected}/historical"
                                               f"?timeframe=6-months").json()["historicalMaxPainData"]

        expiry_date = sorted(list(set(map(lambda x: x["expiration_date"], options_data))))

        return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                      "information": information,
                                                      "related_tickers": related_tickers,
                                                      "options_data": options_data,
                                                      "historical_options_data": historical_options_data,
                                                      "current_price": information["regularMarketPrice"],
                                                      "expiry_date": expiry_date
                                                      })
    else:
        return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                      "information": {},
                                                      "options_data": [],
                                                      "historical_options_data": [],
                                                      "current_price": 0,
                                                      "expiry_date": [],
                                                      "error": "error_true",
                                                      "error_msg": "There is no ticker named {} found! Please enter "
                                                                   "a ticker symbol (TSLA) instead of the name "
                                                                   "(Tesla).".format(ticker_selected)})


def short_volume(request):
    """
    Get short volume of tickers (only popular ones). Data from Finra
    """
    ticker_selected = default_ticker(request)

    if ticker_selected == "TOP_SHORT_VOLUME":
        highest_short_vol = get_stocksera_request(f"stocks/top_short_volume")
        return render(request, 'stock/top_short_volume.html',
                      {"highest_short_vol": highest_short_vol.to_html(index=False)})

    information, related_tickers = check_market_hours(ticker_selected)

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        short_volume_data = get_stocksera_request(f"stocks/short_volume/{ticker_selected}")

        if "download_csv" in request.GET:
            file_name = "{}_short_volume.csv".format(ticker_selected)
            short_volume_data.to_csv(file_name, index=False)
            response = download_file(short_volume_data, file_name)
            return response

        highest_short_vol = get_stocksera_request(f"stocks/top_short_volume")["Ticker"].tolist()[:20]
        return render(request, 'stock/short_volume.html', {"ticker_selected": ticker_selected,
                                                           "information": information,
                                                           "related_tickers": related_tickers,
                                                           "highest_short_vol": highest_short_vol,
                                                           "short_volume_data": short_volume_data.to_html(index=False)})
    else:
        return render(request, 'stock/short_volume.html', {"ticker_selected": ticker_selected,
                                                           "error": "error_true"})


def borrowed_shares(request):
    pd.options.display.float_format = '{:.3f}'.format

    ticker_selected = default_ticker(request)
    information, related_tickers = check_market_hours(ticker_selected)

    if ticker_selected == "TOP_BORROWED_SHARES":
        highest_borrowed_shares = get_stocksera_request(f"stocks/top_borrowed_shares")
        highest_borrowed_shares.columns = ["Ticker", "Fee", "Available"]
        return render(request, 'stock/top_borrowed_shares.html',
                      {"highest_borrowed_shares": highest_borrowed_shares.to_html(index=False)})

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        df = get_stocksera_request(f"stocks/borrowed_shares/{ticker_selected}")
        del df["ticker"]
        df.columns = ["Fee", "Available", "Updated"]
        highest_borrowed_shares = get_stocksera_request(f"stocks/top_borrowed_shares")["ticker"].tolist()[:20]
        return render(request, 'stock/borrowed_shares.html', {"ticker_selected": ticker_selected,
                                                              "information": information,
                                                              "related_tickers": related_tickers,
                                                              "highest_borrowed_shares": highest_borrowed_shares,
                                                              "df": df.to_html(index=False)})
    else:
        return render(request, 'stock/borrowed_shares.html', {"ticker_selected": ticker_selected,
                                                              "error": "error_true"})


def failure_to_deliver(request):
    """
    Get FTD of tickers. Data from SEC
    """
    ticker_selected = default_ticker(request)

    if ticker_selected == "TOP_FTD":
        top_ftd = get_stocksera_request(f"stocks/top_failure_to_deliver")
        return render(request, 'stock/top_ftd.html', {"top_ftd": top_ftd.to_html(index=False)})

    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        ftd = get_stocksera_request(f"stocks/failure_to_deliver/{ticker_selected}")
        if ftd.empty:
            top_range = 0
        else:
            top_range = ftd["Amount (FTD x $)"].quantile(0.90)

        if "download_csv" in request.GET:
            file_name = "{}_ftd.csv".format(ticker_selected)
            ftd.to_csv(file_name, index=False)
            response = download_file(ftd, file_name)
            return response

        return render(request, 'stock/ftd.html', {"ticker_selected": ticker_selected,
                                                  "information": information,
                                                  "related_tickers": related_tickers,
                                                  "90th_percentile": top_range,
                                                  "ftd": ftd.to_html(index=False)})
    else:
        return render(request, 'stock/ftd.html', {"ticker_selected": ticker_selected,
                                                  "error": "error_true"})


def regsho(request):
    """
    Get Regulation SHO data from SEC
    """

    ticker_selected = request.GET.get("quote")

    if ticker_selected:
        ticker_selected = ticker_selected.upper()
        information, related_tickers = check_market_hours(ticker_selected)

        df = get_stocksera_request(f"stocks/regsho/{ticker_selected}")

        if "download_csv" in request.GET:
            file_name = "{}_regsho.csv".format(ticker_selected)
            df.to_csv(file_name, index=False)
            response = download_file(df, file_name)
            return response

        return render(request, 'stock/regsho.html', {"ticker_selected": ticker_selected,
                                                     "information": information,
                                                     "related_tickers": related_tickers,
                                                     "df": df.to_html(index=False)})
    else:
        df = get_stocksera_request(f"stocks/regsho")
        date_list = df["Date"].unique().tolist()

        if "download_csv" in request.GET:
            file_name = "summary_regsho.csv"
            df.to_csv(file_name, index=False)
            response = download_file(df, file_name)
            return response

        return render(request, 'stock/regsho_summary.html', {"df": df.to_html(index=False), "date_list": date_list})


def earnings_calendar(request):
    """
    Get earnings for the upcoming weeks
    """
    cnx, cur, engine = connect_mysql_database()
    df = pd.read_sql("SELECT * FROM earnings ORDER by `date` ASC, CAST(mkt_cap AS UNSIGNED) DESC", cnx)
    df["FY"] = "Q" + df["quarter"] + "/" + df["year"]
    del df["quarter"]
    del df["year"]
    df.columns = ["Date", "Time", "Ticker", "EPS Est", "EPS Act", "Rev Est", "Rev Act", "Mkt Cap", "FY"]
    return render(request, 'market_summary/earnings.html', {"df": df.to_html(index=False)})


def subreddit_count(request):
    """
    Get subreddit user count, growth, active users over time.
    """
    ticker_selected = request.GET.get("quote")
    all_subreddits = sorted(interested_stocks_subreddits)
    if ticker_selected and ticker_selected.upper() != "SUMMARY":
        ticker_selected = ticker_selected.upper().replace(" ", "")
        stats = get_stocksera_request(f"reddit/subreddit_count/{ticker_selected}/?days=1000")
        information, related_tickers = check_market_hours(ticker_selected)
        try:
            subreddit = stats.iloc[0][1]
            del stats["subreddit"]
        except (TypeError, IndexError):
            subreddit = "N/A"
        return render(request, 'reddit/subreddit_count_individual.html', {"ticker_selected": ticker_selected,
                                                                          "information": information,
                                                                          "subreddit": subreddit,
                                                                          "stats": stats[::-1].to_html(index=False),
                                                                          "interested_subreddits": all_subreddits})
    else:
        cnx, cur, engine = connect_mysql_database()
        cur.execute("SELECT * FROM subreddit_count WHERE subreddit in ('wallstreetbets', 'stocks', "
                    " 'amcstock', 'Superstonk', 'options','pennystocks', 'cryptocurrency')")
        subscribers = cur.fetchall()
        subscribers = list(map(list, subscribers))
    return render(request, 'reddit/subreddit_count.html', {"subscribers": subscribers,
                                                           "interested_subreddits": all_subreddits})


def wsb_live(request):
    """
    Get live sentiment from WSB discussion thread
    """
    pd.options.display.float_format = '{:.2f}'.format
    cnx, cur, engine = connect_mysql_database()

    mentions_df = get_stocksera_request(f"reddit/wsb/?days=1")

    # Get trending tickers in the past 7 days
    mentions_7d_df = get_stocksera_request(f"reddit/wsb/?days=7")

    # Get calls/puts mentions
    trending_options = get_stocksera_request(f"reddit/wsb_options/?days=1000")

    # Get change in mentions
    change_df = pd.read_sql_query("SELECT * FROM wsb_change", cnx)

    # Get yahoo financial comparison
    wsb_yf = pd.read_sql_query("SELECT * FROM wsb_yf", cnx)

    return render(request, 'reddit/wsb_live.html', {
        "mentions_df": mentions_df.to_html(index=False),
        "mentions_7d_df": mentions_7d_df.to_html(index=False),
        "change_df": change_df.to_html(index=False),
        "trending_options": trending_options.to_html(index=False),
        "wsb_yf_df": wsb_yf.to_html(index=False)})


def wsb_live_ticker(request):
    """
    Get mentions and sentiment of tickers in WSB
    """
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(request, "SPY")
    information, related_tickers = check_market_hours(ticker_selected)

    df = get_stocksera_request(f"reddit/wsb/{ticker_selected}/?days=1000")

    sentiment_df = pd.read_sql_query('SELECT AVG(sentiment) AS sentiment, '
                                     'date_updated FROM wsb_trending_hourly '
                                     'WHERE ticker="{}" GROUP BY DATE(date_updated)'.
                                     format(ticker_selected), cnx)

    if df.empty:
        recent_mention = 0
        previous_mention = 0
        recent_snt = 0
        previous_snt = 0
        recent_calls = 0
        previous_calls = 0
        recent_puts = 0
        previous_puts = 0
    else:
        current_time = datetime.utcnow()
        last_7D = str(current_time - timedelta(days=7))
        last_14D = str(current_time - timedelta(days=14))

        recent_mention = df[df["date_updated"] >= last_7D]["mentions"].sum()
        previous_mention = df[(df["date_updated"] >= last_14D) & (df["date_updated"] < last_7D)]["mentions"].sum()

        recent_snt = round(sentiment_df[sentiment_df["date_updated"] >= last_7D]["sentiment"].mean(), 4)
        previous_snt = round(sentiment_df[(sentiment_df["date_updated"] >= last_14D) &
                                          (sentiment_df["date_updated"] < last_7D)]["sentiment"].mean(), 4)

        recent_calls = df[df["date_updated"] >= last_7D]["calls"].sum().astype(int)
        previous_calls = df[(df["date_updated"] >= last_14D) &
                            (df["date_updated"] < last_7D)]["calls"].sum().astype(int)

        recent_puts = df[df["date_updated"] >= last_7D]["puts"].sum().astype(int)
        previous_puts = df[(df["date_updated"] >= last_14D) & (df["date_updated"] < last_7D)]["puts"].sum().astype(int)

    return render(request, 'reddit/wsb_live_ticker.html', {"ticker_selected": ticker_selected,
                                                           "information": information,
                                                           "mentions_df": df.to_html(index=False),
                                                           "sentiment_df": sentiment_df.to_html(index=False),
                                                           "recent_mention": recent_mention,
                                                           "previous_mention": previous_mention,
                                                           "recent_snt": recent_snt,
                                                           "previous_snt": previous_snt,
                                                           "recent_calls": recent_calls,
                                                           "previous_calls": previous_calls,
                                                           "recent_puts": recent_puts,
                                                           "previous_puts": previous_puts
                                                           })


def crypto_live(request):
    """
    Get live sentiment from crypto discussion thread
    """
    pd.options.display.float_format = '{:.2f}'.format
    cnx, cur, engine = connect_mysql_database()

    # Get trending tickers in the past 24H
    date_threshold = str(datetime.utcnow() - timedelta(hours=24))

    mentions_df = get_stocksera_request(f"reddit/crypto/?days=1")

    # Get word cloud
    cur.execute("SELECT word, SUM(mentions) FROM crypto_word_cloud WHERE date_updated >= %s GROUP BY word ORDER BY "
                "SUM(mentions) DESC LIMIT 50", (date_threshold,))
    crypto_word_cloud = cur.fetchall()
    crypto_word_cloud = list(map(list, crypto_word_cloud))

    # Get trending tickers in the past 7 days
    mentions_7d_df = get_stocksera_request(f"reddit/crypto/?days=7")

    # Get change in mentions
    change_df = pd.read_sql_query("SELECT * FROM crypto_change", cnx)

    return render(request, 'reddit/crypto_live.html', {"crypto_word_cloud": crypto_word_cloud,
                                                       "mentions_df": mentions_df.to_html(index=False),
                                                       "mentions_7d_df": mentions_7d_df.to_html(index=False),
                                                       "change_df": change_df.to_html(index=False),
                                                       })


def crypto_live_ticker(request):
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(request, "BTC")

    df = get_stocksera_request(f"reddit/crypto/{ticker_selected}/?days=1000")

    sentiment_df = pd.read_sql_query('SELECT AVG(sentiment) AS sentiment, '
                                     'date_updated FROM crypto_trending_hourly '
                                     'WHERE ticker="{}" GROUP BY DATE(date_updated)'.
                                     format(ticker_selected), cnx)

    if df.empty:
        recent_mention = 0
        previous_mention = 0
        recent_snt = 0
        previous_snt = 0
    else:
        current_time = datetime.utcnow()
        last_7D = str(current_time - timedelta(days=7))
        last_14D = str(current_time - timedelta(days=14))

        recent_mention = df[df["date_updated"] >= last_7D]["mentions"].sum()
        previous_mention = df[(df["date_updated"] >= last_14D) & (df["date_updated"] < last_7D)]["mentions"].sum()

        recent_snt = round(sentiment_df[sentiment_df["date_updated"] >= last_7D]["sentiment"].mean(), 4)
        previous_snt = round(sentiment_df[(sentiment_df["date_updated"] >= last_14D) &
                                          (sentiment_df["date_updated"] < last_7D)]["sentiment"].mean(), 4)

    return render(request, 'reddit/crypto_live_ticker.html', {"ticker_selected": ticker_selected,
                                                              "mentions_df": df.to_html(index=False),
                                                              "sentiment_df": sentiment_df.to_html(index=False),
                                                              "recent_mention": recent_mention,
                                                              "previous_mention": previous_mention,
                                                              "recent_snt": recent_snt,
                                                              "previous_snt": previous_snt,
                                                              })


def wsb_documentation(request):
    return render(request, "reddit/wsb_documentation.html", {"banned_words": sorted(stopwords_list)})


def market_summary(request):
    pd.options.display.float_format = '{:.2f}'.format
    if request.GET.get("type") == "crypto":
        title = "Cryptocurrency"
        return render(request, 'market_summary/market_summary.html', {"title": title})
    elif request.GET.get("type") == "wsb":
        title = "Wallstreetbets"
        summary_df = pd.read_sql_query("SELECT ticker, mentions, mkt_cap, price_change FROM wsb_yf", cnx)
        return render(request, 'market_summary/market_summary.html', {"title": title,
                                                                      "summary_df": summary_df.to_html(index=False)})

    data = requests.get(f"{BASE_URL}/news/market_summary/?type={request.GET.get('type')}", headers=HEADERS).json()
    title = list(data.keys())[0]
    data = list(data.values())[0]

    summary_df = pd.DataFrame(data)
    summary_df = summary_df.replace("N/A", np.nan)
    summary_df = summary_df[summary_df['Industry'].notna()]

    x = summary_df.copy()
    x["% Change / Mkt Cap"] = (x["% Change"] * x["Market Cap"])

    industry_df = x.groupby(["Sector", "Industry"]).agg({"Market Cap": "sum", "% Change / Mkt Cap": "sum"})
    industry_df = pd.DataFrame(industry_df)
    industry_df["% Change"] = industry_df["% Change / Mkt Cap"] / industry_df["Market Cap"]
    industry_df.reset_index(inplace=True)

    sector_df = x.groupby(["Sector"]).agg({"Market Cap": "sum", "% Change / Mkt Cap": "sum"})
    sector_df = pd.DataFrame(sector_df)
    sector_df["% Change"] = sector_df["% Change / Mkt Cap"] / sector_df["Market Cap"]
    sector_df.reset_index(inplace=True)
    return render(request, 'market_summary/market_summary.html', {"summary_df": summary_df.to_html(index=False),
                                                                  "industry_df": industry_df.to_html(index=False),
                                                                  "sector_df": sector_df.to_html(index=False),
                                                                  "title": title})


def futures(request):
    return render(request, 'market_summary/futures.html')


def senate_trades(request):
    senator = request.GET.get("person")
    ticker_selected = request.GET.get("quote")

    if senator:
        data = requests.get(f"{BASE_URL}/government/senate/?name={senator}", headers=HEADERS).json()
        senator_df = pd.DataFrame(data["senate"])
        all_senators = data["names_available"]

        return render(request, 'government/trading_individual.html',
                      {"gov_type": "senate",
                       "person_trades_df": senator_df.to_html(index=False),
                       "person_name": senator,
                       "all_person_list": all_senators})

    elif ticker_selected:
        ticker_selected = ticker_selected.upper()
        data = requests.get(f"{BASE_URL}/government/senate/?ticker={ticker_selected}", headers=HEADERS).json()
        ticker_df = pd.DataFrame(data["senate"])
        history_df = yf.Ticker(ticker_selected).history(period="5y", interval="1d")
        history_df.reset_index(inplace=True)
        history_df = history_df[["Date", "Close"]]
        all_tickers = data["tickers_available"]

        return render(request, 'government/ticker_analysis.html', {"gov_type": "senate",
                                                                   "ticker_df": ticker_df.to_html(index=False),
                                                                   "history_df": history_df.to_html(index=False),
                                                                   "ticker_selected": ticker_selected,
                                                                   "ticker_list": all_tickers})

    else:
        data = requests.get(f"{BASE_URL}/government/senate", headers=HEADERS).json()
        df = pd.DataFrame(data["senate"])
        date_selected = request.GET.get("date_selected")
        date_selected, latest_df, group_by_senator, group_by_ticker = government_daily_trades(df, date_selected,
                                                                                              "Senator")
        return render(request, 'government/trading_summary.html',
                      {"gov_type": "senate",
                       "group_by_people": group_by_senator.to_html(index=False),
                       "group_by_ticker": group_by_ticker.to_html(index=False),
                       "latest_df": latest_df.to_html(index=False),
                       "dates_available": df["Disclosure Date"].drop_duplicates().to_list(),
                       "district": [],
                       "district_count": [],
                       "date_selected": date_selected})


def house_trades(request):
    representative = request.GET.get("person")
    ticker_selected = request.GET.get("quote")
    state = request.GET.get("state")

    if representative:
        data = requests.get(f"{BASE_URL}/government/house/?name={representative}", headers=HEADERS).json()
        house_df = pd.DataFrame(data["house"])
        all_representative = data["names_available"]

        return render(request, 'government/trading_individual.html',
                      {"gov_type": "house",
                       "person_trades_df": house_df.to_html(index=False),
                       "person_name": representative,
                       "all_person_list": all_representative})

    elif ticker_selected:
        ticker_selected = ticker_selected.upper()
        data = requests.get(f"{BASE_URL}/government/house/?ticker={ticker_selected}", headers=HEADERS).json()
        ticker_df = pd.DataFrame(data["house"])
        history_df = yf.Ticker(ticker_selected).history(period="5y", interval="1d")
        history_df.reset_index(inplace=True)
        history_df = history_df[["Date", "Close"]]
        all_tickers = data["tickers_available"]

        return render(request, 'government/ticker_analysis.html', {"gov_type": "house",
                                                                   "ticker_df": ticker_df.to_html(index=False),
                                                                   "history_df": history_df.to_html(index=False),
                                                                   "ticker_selected": ticker_selected,
                                                                   "ticker_list": all_tickers})

    elif state:
        data = requests.get(f"{BASE_URL}/government/house/?state={state}", headers=HEADERS).json()
        district_df = pd.DataFrame(data["house"])
        district_list = data["districts_available"]

        return render(request, 'government/state.html', {"gov_type": "house",
                                                         "state": state,
                                                         "district_list": district_list,
                                                         "district_df": district_df.to_html(index=False)})

    else:
        date_selected = request.GET.get("date_selected")
        data = requests.get(f"{BASE_URL}/government/house", headers=HEADERS).json()
        df = pd.DataFrame(data["house"])
        date_selected, latest_df, group_by_representative, group_by_ticker = government_daily_trades(df, date_selected,
                                                                                                     "Representative")
        df["District"] = df["District"].str[:2]
        district_df = pd.DataFrame(df.groupby(["District"]).agg("count")["Ticker"])
        district_count = district_df["Ticker"].tolist()
        district = district_df.index.tolist()

        return render(request, 'government/trading_summary.html',
                      {"gov_type": "house",
                       "group_by_people": group_by_representative.to_html(index=False),
                       "group_by_ticker": group_by_ticker.to_html(index=False),
                       "latest_df": latest_df.to_html(index=False),
                       "dates_available": df["Disclosure Date"].drop_duplicates().to_list(),
                       "district": district,
                       "district_count": district_count,
                       "date_selected": date_selected})


def crypto_transactions(request):
    return render(request, 'crypto_transaction.html')


def fear_and_greed(request):
    """
    Get fear and green data. Data is from https://edition.cnn.com/markets/fear-and-greed
    """
    df = get_stocksera_request(f"discover/fear_and_greed/?days=1000")
    return render(request, 'discover/fear_and_greed.html', {"df": df[::-1].to_html(index=False)})


def reverse_repo(request):
    """
    Get reverse repo. Data is from https://apps.newyorkfed.org/
    """
    df = get_stocksera_request(f"economy/reverse_repo/?days=1000")
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/reverse_repo.html',
                  {"reverse_repo_stats": df[::-1].to_html(index=False), "next_date": data})


def daily_treasury(request):
    """
    Get daily treasury.
    Data is from https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/operating-cash-balance
    """
    df = get_stocksera_request(f"economy/daily_treasury/?days=1000")
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/daily_treasury.html',
                  {"daily_treasury_stats": df[::-1].to_html(index=False), "next_date": data})


def us_inflation(request):
    """
    Get inflation. Data is from https://www.usinflationcalculator.com/inflation/current-inflation-rates/
    """
    df = get_stocksera_request(f"economy/inflation/usa").T
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Year"}, inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/inflation.html', {"inflation_stats": df.to_html(index=False), "next_date": data})


def world_inflation(request):
    """
    Get world inflation.
    """
    pd.options.display.float_format = '{:.2f}'.format
    df = get_stocksera_request(f"economy/inflation/world")
    return render(request, 'economy/world_inflation.html', {"inflation_stats": df.to_html(index=False)})


def retail_sales(request):
    """
    Get retail sales. Data is from https://ycharts.com/indicators/us_retail_and_food_services_sales
    """
    df = get_stocksera_request(f"economy/retail_sales/?days=1000")
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/retail_sales.html',
                  {"retail_stats": df[::-1].to_html(index=False), "next_date": data})


def fed_interest_rate(request):
    """
    Get interest rate. Data is from https://fred.stlouisfed.org
    """
    df = get_stocksera_request(f"economy/interest_rate")
    return render(request, 'economy/interest_rate.html', {"df": df.to_html(index=False)})


def initial_jobless(request):
    df = get_stocksera_request(f"economy/initial_jobless_claims/?days=1000")
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/initial_jobless_claims.html',
                  {"jobless_claims": df[::-1].to_html(index=False), "next_date": data})


def short_interest(request):
    """
    Get short interest of ticker. Data from https://www.stockgrid.io/shortinterest
    """
    df = get_stocksera_request(f"discover/short_interest")
    return render(request, 'discover/short_interest.html', {"df_high_short_interest": df.to_html(index=False)})


def low_float(request):
    """
    Get short interest of ticker. Data if from lowfloat.com
    """
    df = get_stocksera_request(f"discover/low_float")
    return render(request, 'discover/low_float.html', {"df_low_float": df.to_html(index=False)})


def ark_trades(request):
    """
    Get trades/positions of ARK Funds. Data from https://arkfunds.io/api
    """
    return render(request, 'discover/ark_trade.html')


def ipo_calendar(request):
    df = get_stocksera_request(f"discover/ipo_calendar")
    return render(request, 'discover/ipo_calendar.html', {"ipo_df": df.to_html(index=False)})


def largest_companies(request):
    df = get_stocksera_request(f"discover/largest_companies")
    return render(request, 'discover/largest_companies.html', {"df": df.to_html(index=False)})


def correlation(request):
    pd.options.display.float_format = '{:.3f}'.format
    if request.GET.get("quotes"):
        symbols_list = request.GET['quotes'].upper().replace(" ", "")
    else:
        symbols_list = "AAPL, TSLA, SPY, AMC, GME, NVDA, XOM"
    try:
        df = yf.Tickers(symbols_list).history(period="1y")
    except KeyError:
        df = yf.Tickers("AAPL, TSLA, SPY, AMC, GME, NVDA, XOM").history(period="1y")
    df = df["Close"].corr(method='pearson')
    df.replace(1, "-", inplace=True)
    return render(request, 'discover/correlation.html', {"df": df.to_html(), "symbols_list": symbols_list})


def stock_split_history(request):
    pd.options.display.float_format = '{:.3f}'.format
    df = get_stocksera_request(f"discover/stock_split")
    return render(request, 'discover/stock_split.html', {"df": df.to_html(index=False)})


def dividend_history(request):
    pd.options.display.float_format = '{:.3f}'.format
    df = get_stocksera_request(f"discover/dividend_history")

    if request.GET.get("order"):
        order = request.GET['order'].replace("Order: ", "")
        if order == "asc":
            order = True
        else:
            order = False
    else:
        order = False

    if request.GET.get("sort"):
        sort_by = request.GET['sort'].replace("Sort By: ", "")
        df.sort_values(by=[sort_by], ascending=order, inplace=True)
    else:
        sort_by = "Declaration Date"

    order = "Ascending" if order is True else "Descending"

    return render(request, 'discover/dividend_history.html', {"df": df.to_html(index=False),
                                                              "sort_by": sort_by,
                                                              "order": order})


def stocktwits(request):
    ticker_selected = default_ticker(request, "TSLA")
    ticker_df = get_stocksera_request(f"stocktwits/{ticker_selected}")
    trending_df = get_stocksera_request(f"stocktwits")

    if not ticker_df.empty:
        ticker = yf.Ticker(ticker_selected)
        price_df = ticker.history(period="1y", interval="1d").reset_index().iloc[::-1]
        price_df = price_df[["Date", "Close", "Volume"]]
        price_df = price_df[price_df["Date"] >= ticker_df.iloc[0]["date_updated"].split()[0]]
    else:
        price_df = pd.DataFrame(columns=["Date", "Close", "Volume"])

    return render(request, 'social/stocktwits.html', {"ticker_selected": ticker_selected,
                                                      "ticker_df": ticker_df.to_html(index=False),
                                                      "trending_df": trending_df.to_html(index=False),
                                                      "price_df": price_df.to_html(index=False)})


def twitter_trending(request):
    ticker_selected = default_ticker(request, "TSLA")
    ticker_df = pd.read_sql_query("SELECT tweet_count, updated_date FROM twitter_trending WHERE "
                                  "ticker='{}' ".format(ticker_selected), cnx)
    return render(request, 'social/twitter_trending.html', {"ticker_selected": ticker_selected,
                                                            "ticker_df": ticker_df.to_html(index=False),
                                                            })


def jim_cramer(request):
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = request.GET.get("quote")
    if ticker_selected:
        ticker_selected = ticker_selected.upper()
        information, related_tickers = check_market_hours(ticker_selected)

        ticker_df = get_stocksera_request(f"discover/jim_cramer/{ticker_selected}")
        history_df = yf.Ticker(ticker_selected).history(period="1y", interval="1d")
        history_df.reset_index(inplace=True)
        history_df = history_df[["Date", "Close"]]
        history_df["Date"] = history_df["Date"].astype(str)

        if ticker_df.empty:
            ticker_df = pd.DataFrame([{"Date": "N/A", "Segment": "N/A", "Call": "N/A", "Close": "N/A",
                                       "Pro Cramer": "N/A", "Inverse Cramer": "N/A"}])
        else:
            del ticker_df["Ticker"]
            del ticker_df["Price"]
            latest_price = history_df.iloc[-1]["Close"]
            ticker_df = ticker_df.merge(history_df, on="Date")
            ticker_df["Pro Cramer"] = latest_price
            ticker_df["Pro Cramer"] = 100 * (ticker_df["Pro Cramer"] - ticker_df["Close"]) / ticker_df["Close"]
            ticker_df.loc[ticker_df["Call"].isin(["Negative", "Sell"]), 'Pro Cramer'] *= -1
            ticker_df["Inverse Cramer"] = ticker_df["Pro Cramer"] * -1

        return render(request, 'discover/jim_cramer_ticker_analysis.html', {"ticker_selected": ticker_selected.upper(),
                                                                            "information": information,
                                                                            "related_tickers": related_tickers,
                                                                            "ticker_df": ticker_df.to_html(index=False),
                                                                            "history_df": history_df.to_html(
                                                                                index=False)})
    else:
        df = get_stocksera_request(f"discover/jim_cramer")[:500]
        return render(request, 'discover/jim_cramer.html', {"df": df.to_html(index=False)})


def news(request):
    df = get_stocksera_request(f"news/market_news")
    df.rename(columns={"Date": "Date [UTC]"}, inplace=True)
    return render(request, 'news/news.html', {"df": df.to_html(index=False)})


def twitter_feed(request):
    return render(request, 'news/twitter_feed.html')


def trading_halts(request):
    df = get_stocksera_request(f"news/trading_halts")
    return render(request, 'news/trading_halts.html', {"df": df.to_html(index=False)})


def beta(request):
    """
    Compare beta between any 2 tickers
    """
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

    return render(request, 'discover/beta.html', {"beta": round(coef, 3),
                                                  "ticker_selected": ticker_interested,
                                                  "ticker_selected2": default,
                                                  "price_change": price_change[::-1].to_html(index=False),
                                                  "timeframe": timeframe.replace("mo", " Months").replace("y", " Year"),
                                                  "interval": interval.replace("1mo", "Monthly").replace("1d",
                                                                                                         "Daily")})


def about(request):
    """
    About section of the website and contact me if there's any issues/suggestions
    """
    return render(request, 'about.html')


def tasks(request):
    current_timing = str(datetime.utcnow()).split(".")[0]
    if not os.path.exists("database/locally_run_timings.json"):
        with open(r"database/locally_run_timings.json", "w") as r:
            json.dump(
                {"create_db": current_timing,
                 "wsb_trending": current_timing,
                 "crypto_trending": current_timing,
                 "subreddit_trending": current_timing,
                 "twitter_followers": current_timing,
                 "twitter_stock_trending": current_timing,
                 "stocktwits_trending": current_timing,
                 "short_vol": current_timing,
                 "dividends": current_timing,
                 "stock_split": current_timing,
                 "earning_calendar": current_timing,
                 "latest_news": current_timing,
                 "trading_halt": current_timing,
                 "ftd": current_timing,
                 "ctb": current_timing,
                 "threshold_sec": current_timing,
                 "insider_trading": current_timing,
                 "heatmap": current_timing,
                 "govt_trading": current_timing,
                 "ipo": current_timing,
                 "rrp": current_timing,
                 "inflation": current_timing,
                 "treasury": current_timing,
                 "retail": current_timing,
                 "interest_rate": current_timing,
                 "initial_jobless_claims": current_timing,
                 "upcoming_economic_dates": current_timing
                 }, r, indent=4)

    with open(r"database/locally_run_timings.json", "r") as r:
        data = json.load(r)

    if request.POST:
        try:
            if request.POST.get("create_db"):
                task_create_db()
                data["create_db"] = current_timing
            elif request.POST.get("wsb_trending"):
                task_wsb_trending()
                data["wsb_trending"] = current_timing
            elif request.POST.get("crypto_trending"):
                task_crypto_trending()
                data["crypto_trending"] = current_timing
            elif request.POST.get("subreddit_trending"):
                task_subreddit_trending()
                data["subreddit_trending"] = current_timing
            elif request.POST.get("twitter_followers"):
                task_twitter_followers()
                data["twitter_followers"] = current_timing
            elif request.POST.get("twitter_stock_trending"):
                task_twitter_stock_trending()
                data["twitter_stock_trending"] = current_timing
            elif request.POST.get("stocktwits_trending"):
                task_stocktwits_trending()
                data["stocktwits_trending"] = current_timing
            elif request.POST.get("short_vol"):
                task_short_vol()
                data["short_vol"] = current_timing
            elif request.POST.get("dividends"):
                task_dividends()
                data["dividends"] = current_timing
            elif request.POST.get("stock_split"):
                task_stock_split()
                data["stock_split"] = current_timing
            elif request.POST.get("earning_calendar"):
                task_earning_calendar()
                data["earning_calendar"] = current_timing
            elif request.POST.get("latest_news"):
                task_latest_news()
                data["latest_news"] = current_timing
            elif request.POST.get("trading_halt"):
                task_trading_halt()
                data["trading_halt"] = current_timing
            elif request.POST.get("ftd"):
                task_ftd()
                data["ftd"] = current_timing
            elif request.POST.get("ctb"):
                task_ctb()
                data["ctb"] = current_timing
            elif request.POST.get("threshold_sec"):
                task_threshold_sec()
                data["threshold_sec"] = current_timing
            elif request.POST.get("insider_trading"):
                task_insider_trading()
                data["insider_trading"] = current_timing
            elif request.POST.get("heatmap"):
                task_heatmap()
                data["heatmap"] = current_timing
            elif request.POST.get("govt_trading"):
                task_govt_trading()
                data["govt_trading"] = current_timing
            elif request.POST.get("ipo"):
                task_ipo()
                data["ipo"] = current_timing
            elif request.POST.get("short_int"):
                task_short_int()
                data["short_int"] = current_timing
            elif request.POST.get("low_float"):
                task_low_float()
                data["low_float"] = current_timing
            elif request.POST.get("largest_companies"):
                task_largest_companies()
                data["largest_companies"] = current_timing
            elif request.POST.get("fear_and_greed"):
                task_fear_and_greed()
                data["fear_and_greed"] = current_timing
            elif request.POST.get("rrp"):
                task_rrp()
                data["rrp"] = current_timing
            elif request.POST.get("inflation"):
                task_inflation()
                data["inflation"] = current_timing
            elif request.POST.get("treasury"):
                task_treasury()
                data["treasury"] = current_timing
            elif request.POST.get("retail"):
                task_retail()
                data["retail"] = current_timing
            elif request.POST.get("interest_rate"):
                task_interest_rate()
                data["interest_rate"] = current_timing
            elif request.POST.get("initial_jobless_claims"):
                task_initial_jobless_claims()
                data["initial_jobless_claims"] = current_timing
            elif request.POST.get("upcoming_economic_dates"):
                task_upcoming_economic_dates()
                data["upcoming_economic_dates"] = current_timing

            with open(r"database/locally_run_timings.json", "w") as r:
                json.dump(data, r, indent=4)
        except:
            pass

    return render(request, 'tasks.html', {"data": data})


def setup(request):
    if request.POST:
        if request.POST.get("locally_hosted_value") == "True":
            config_keys[request.POST.get("locally_hosted")] = True
        else:
            config_keys[request.POST.get("locally_hosted")] = False
        config_keys[request.POST.get("stocksera_base_url")] = request.POST.get("stocksera_base_url_value")
        config_keys[request.POST.get("stocksera_api")] = request.POST.get("stocksera_api_value")

        config_keys[request.POST.get("finnhub_api")] = request.POST.get("finnhub_api_value")
        config_keys[request.POST.get("fmp_api")] = request.POST.get("fmp_api_value")
        config_keys[request.POST.get("polygon_api")] = request.POST.get("polygon_api_value")
        config_keys[request.POST.get("twitter_api")] = request.POST.get("twitter_api_value")
        config_keys[request.POST.get("reddit_id_api")] = request.POST.get("reddit_id_api_value")
        config_keys[request.POST.get("reddit_sec_api")] = request.POST.get("reddit_sec_api_value")
        config_keys[request.POST.get("whalealert_api")] = request.POST.get("whalealert_api_value")

        config_keys[request.POST.get("mysql_db")] = request.POST.get("mysql_db_value")
        config_keys[request.POST.get("mysql_host")] = request.POST.get("mysql_host_value")
        config_keys[request.POST.get("mysql_pw")] = request.POST.get("mysql_pw_value")
        config_keys[request.POST.get("mysql_port")] = request.POST.get("mysql_port_value")
        config_keys[request.POST.get("mysql_user")] = request.POST.get("mysql_user_value")

        with open('config.yaml', 'w') as outfile:
            yaml.dump(config_keys, outfile, default_flow_style=False)
    return render(request, 'setup.html', {"config": config_keys})


def loading_spinner(request):
    """
    Spinner display for iframe
    """
    return render(request, 'loading_spinner.html')


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})
