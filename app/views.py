from scheduled_tasks.reddit.get_subreddit_count import *
from helpers import *
from email_server import *

import requests_cache
import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq

from django.shortcuts import render, redirect

try:
    from admin import *
except ModuleNotFoundError:
    print("Not authorised to have access to admin functions")

try:
    trends = TrendReq(hl='en-US', tz=360)
except:
    print("Timeout for Google Trend")

pd.options.display.float_format = '{:.1f}'.format

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                'Chrome/91.0.4472.124 Safari/537.36'

BASE_URL = config_keys['STOCKSERA_BASE_URL']
HEADERS = {f'Authorization': f"Api-Key {config_keys['STOCKSERA_API']}"}


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
    ticker = yf.Ticker(ticker_selected, session=session)
    try:
        recommendations = ticker.recommendations
        recommendations["Action"] = recommendations["Action"].str \
            .replace("main", "Maintain") \
            .replace("up", "Upgrade") \
            .replace("down", "Downgrade") \
            .replace("init", "Initialised") \
            .replace("reit", "Reiterate")
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
    return render(request, 'stock/recommendations.html', {"table": recommendations[:100].to_html(index=False)})


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
        past_df["Year"] = ["2022", "2021", "2020", "2019"]
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
        next_df["Next Earning"] = ["Earning Date", "EPS Average", "EPS Low", "EPS High", "Revenue Average",
                                   "Revenue Low", "Revenue High"]
        next_df["Estimate"] = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    return render(request, 'stock/ticker_earnings.html', {"ticker_selected": ticker_selected,
                                                          "ticker_earnings": past_df.to_html(index=False),
                                                          "ticker_next_earnings": next_df.to_html(index=False)})


def sec_fillings(request):
    """
    Get SEC filling from Finnhub of ticker selected
    """
    ticker_selected = default_ticker(request)
    data = requests.get(f"{BASE_URL}/stocks/sec_fillings/{ticker_selected}", headers=HEADERS).json()
    df = pd.DataFrame(data)
    df = df.to_html(index=False)
    return render(request, 'stock/sec_fillings.html', {"sec_fillings_df": df})


def news_sentiment(request):
    """
    Show news and sentiment of ticker in /ticker?quote={TICKER}. Data from Finviz
    Note: News are only available if hosted locally. Read README.md for more details
    """
    ticker_selected = default_ticker(request)
    data = requests.get(f"{BASE_URL}/stocks/news_sentiment/{ticker_selected}", headers=HEADERS).json()
    news_df = pd.DataFrame(data)
    news_df = news_df.to_html(index=False)
    return render(request, 'stock/recent_news.html', {"title": "News", "recent_news_df": news_df})


def insider_trading(request):
    """
    Get a specific ticker's insider trading data from Finviz
    """
    ticker_selected = default_ticker(request)
    data = requests.get(f"{BASE_URL}/stocks/insider_trading/{ticker_selected}", headers=HEADERS).json()
    inside_trader_df = pd.DataFrame(data)
    if inside_trader_df.empty:
        inside_trader_df = pd.DataFrame([{"Name": "N/A", "Relationship": "N/A", "Date": "N/A"}])
    inside_trader_df = inside_trader_df.to_html(index=False)
    return render(request, 'stock/insider_trading.html', {"inside_trader_df": inside_trader_df})


def latest_insider(request):
    """
    Get latest insider trading data from Finviz and perform analysis
    """
    data = requests.get(f"{BASE_URL}/discover/latest_insider/?limit=2000", headers=HEADERS).json()
    recent_activity = pd.DataFrame(data)

    data = requests.get(f"{BASE_URL}/discover/latest_insider_summary", headers=HEADERS).json()
    insider_analysis = pd.DataFrame(data)
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

    # Remove -USD in crpyto
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


def financial(request):
    """
    Get balance sheet of company. Data is from yahoo finance
    """
    ticker_selected = default_ticker(request)
    ticker = yf.Ticker(ticker_selected)

    information, related_tickers = check_market_hours(ticker_selected)

    # quarterly_cashflow = ticker.quarterly_cashflow
    # print(quarterly_cashflow)
    # for i in quarterly_cashflow.index.to_list():
    #     print(i)

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        current_datetime = str(datetime.utcnow().date())
        with open(r"database/financials.json", "r+") as r:
            data = check_json(r)
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
        return render(request, 'stock/financial.html', {"ticker_selected": ticker_selected,
                                                        "information": information,
                                                        "related_tickers": related_tickers,
                                                        "date_list": date_list,
                                                        "balance_list": balance_list,
                                                        "balance_col_list": balance_col_list})
    else:
        return render(request, 'stock/financial.html', {"ticker_selected": ticker_selected,
                                                        "error": "error_true"})


def options(request):
    """
    Get options chain from TD Ameritrade
    """
    ticker_selected = default_ticker(request)
    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        options_data = get_options_data(ticker_selected)
        return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                      "information": information,
                                                      "related_tickers": related_tickers,
                                                      "options_data": options_data
                                                      })
    else:
        return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                      "options_data": {},
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
        data = requests.get(f"{BASE_URL}/stocks/top_short_volume", headers=HEADERS).json()
        highest_short_vol = pd.DataFrame(data)
        return render(request, 'stock/top_short_volume.html',
                      {"highest_short_vol": highest_short_vol.to_html(index=False)})

    information, related_tickers = check_market_hours(ticker_selected)

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        data = requests.get(f"{BASE_URL}/stocks/short_volume/{ticker_selected}/", headers=HEADERS).json()
        short_volume_data = pd.DataFrame(data)
        print(short_volume_data)

        if "download_csv" in request.GET:
            file_name = "{}_short_volume.csv".format(ticker_selected)
            short_volume_data.to_csv(file_name, index=False)
            response = download_file(short_volume_data, file_name)
            return response

        data = requests.get(f"{BASE_URL}/stocks/top_short_volume", headers=HEADERS).json()
        highest_short_vol = pd.DataFrame(data)["Ticker"].tolist()[:20]

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

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        data = requests.get(f"{BASE_URL}/stocks/borrowed_shares/{ticker_selected}", headers=HEADERS).json()
        df = pd.DataFrame(data)
        del df["ticker"]
        df.columns = ["Fee", "Available", "Updated"]
        return render(request, 'stock/borrowed_shares.html', {"ticker_selected": ticker_selected,
                                                              "information": information,
                                                              "related_tickers": related_tickers,
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
        data = requests.get(f"{BASE_URL}/stocks/top_failure_to_deliver", headers=HEADERS).json()
        top_ftd = pd.DataFrame(data)
        return render(request, 'stock/top_ftd.html', {"top_ftd": top_ftd.to_html(index=False)})

    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        data = requests.get(f"{BASE_URL}/stocks/failure_to_deliver/{ticker_selected}", headers=HEADERS).json()
        ftd = pd.DataFrame(data)
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


def earnings_calendar(request):
    """
    Get earnings for the upcoming weeks
    """
    df = pd.read_sql("SELECT * FROM earnings ORDER by `date` ASC, CAST(mkt_cap AS UNSIGNED) DESC", cnx)
    df["FY"] = "Q" + df["quarter"] + "/" + df["year"]
    del df["quarter"]
    del df["year"]
    df.columns = ["Date", "Time", "Ticker", "EPS Est", "EPS Act", "Rev Est", "Rev Act", "Mkt Cap", "FY"]
    return render(request, 'market_summary/earnings.html', {"df": df.to_html(index=False)})


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

    cur.execute("SELECT DISTINCT(date_updated) FROM {} ORDER BY ID DESC".format(subreddit, ))
    latest_date = cur.fetchone()[0]

    cur.execute("SELECT * FROM {} WHERE date_updated=%s ORDER BY `rank` ASC "
                "LIMIT 35".format(subreddit), (latest_date,))
    trending_tickers = cur.fetchall()
    trending_tickers = list(map(list, trending_tickers))

    if subreddit == "cryptocurrency":
        return render(request, 'reddit/cryptocurrency.html', {"trending_tickers": trending_tickers})

    database_mapping = {"wallstreetbets": "Wall Street Bets",
                        "stocks": "Stocks",
                        "shortsqueeze": "Shortsqueeze",
                        "options": "Options",
                        "spacs": "SPACs",
                        "pennystocks": "Pennystocks"}
    subreddit = database_mapping[subreddit]

    return render(request, 'reddit/reddit_sentiment.html', {"trending_tickers": trending_tickers,
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

    cur.execute("SELECT `rank`, total, price, date_updated from {} WHERE ticker=%s".format(subreddit),
                (ticker_selected,))
    ranking = cur.fetchall()

    if subreddit != "cryptocurrency":
        information, related_tickers = check_market_hours(ticker_selected)
        return render(request, 'reddit/reddit_stocks_analysis.html', {"ticker_selected": ticker_selected,
                                                                      "information": information,
                                                                      "related_tickers": related_tickers,
                                                                      "ranking": ranking,
                                                                      "subreddit": subreddit})
    else:
        return render(request, 'reddit/reddit_crypto_analysis.html', {"ticker_selected": ticker_selected,
                                                                      "ranking": ranking})


def reddit_etf(request):
    """
    Get ETF of r/wallstreetbets
    Top 10 tickers before market open will be purchased daily
    """
    cur.execute("SELECT * FROM reddit_etf WHERE status='Open' ORDER BY open_date DESC")
    open_trade = cur.fetchall()

    cur.execute("select sum(PnL) from reddit_etf WHERE status='Open'")
    unrealized_PnL = round(cur.fetchone()[0], 2)

    cur.execute("SELECT * FROM reddit_etf WHERE status='Close' ORDER BY close_date DESC")
    close_trade = cur.fetchall()

    cur.execute("select sum(PnL) from reddit_etf WHERE status='Close'")
    realized_PnL = round(cur.fetchone()[0], 2)

    return render(request, 'reddit/reddit_etf.html', {"open_trade": open_trade,
                                                      "close_trade": close_trade,
                                                      "unrealized_PnL": unrealized_PnL,
                                                      "realized_PnL": realized_PnL})


def subreddit_count(request):
    """
    Get subreddit user count, growth, active users over time.
    """
    ticker_selected = request.GET.get("quote")

    if request.POST.get("new_subreddit_name"):
        send_email_to_self("Subreddit Alert", "",
                           f"Ticker Name: {request.POST.get('quote')}, "
                           f"Subreddit: r/{request.POST.get('new_subreddit_name')}")

    all_subreddits = sorted(interested_stocks_subreddits)
    if ticker_selected and ticker_selected.upper() != "SUMMARY":
        ticker_selected = ticker_selected.upper().replace(" ", "")
        data = requests.get(f"{BASE_URL}/reddit/subreddit_count/{ticker_selected}/?days=1000", headers=HEADERS).json()
        stats = pd.DataFrame(data)
        information, related_tickers = check_market_hours(ticker_selected)
        try:
            print(stats)
            subreddit = stats.iloc[0][1]
            print(subreddit, "#############")
            del stats["subreddit"]
        except (TypeError, IndexError):
            subreddit = "N/A"
        return render(request, 'reddit/subreddit_count_individual.html', {"ticker_selected": ticker_selected,
                                                                          "information": information,
                                                                          "subreddit": subreddit,
                                                                          "stats": stats[::-1].to_html(index=False),
                                                                          "interested_subreddits": all_subreddits})
    else:
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

    # Get trending tickers in the past 24H
    date_threshold = str(datetime.utcnow() - timedelta(hours=24))

    data = requests.get(f"{BASE_URL}/reddit/wsb/?days=1", headers=HEADERS).json()
    mentions_df = pd.DataFrame(data)

    # Get word cloud
    cur.execute("SELECT word, SUM(mentions) FROM wsb_word_cloud WHERE date_updated >= %s GROUP BY word ORDER BY "
                "SUM(mentions) DESC LIMIT 50", (date_threshold,))
    wsb_word_cloud = cur.fetchall()
    wsb_word_cloud = list(map(list, wsb_word_cloud))

    # Get trending tickers in the past 7 days
    data = requests.get(f"{BASE_URL}/reddit/wsb/?days=7", headers=HEADERS).json()
    mentions_7d_df = pd.DataFrame(data)

    # Get calls/puts mentions
    data = requests.get(f"{BASE_URL}/reddit/wsb_options/?days=1000", headers=HEADERS).json()
    trending_options = pd.DataFrame(data)

    # Get change in mentions
    change_df = pd.read_sql_query("SELECT * FROM wsb_change", cnx)

    # Get yahoo financial comparison
    wsb_yf = pd.read_sql_query("SELECT * FROM wsb_yf", cnx)

    return render(request, 'reddit/wsb_live.html', {
        "wsb_word_cloud": wsb_word_cloud,
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

    data = requests.get(f"{BASE_URL}/reddit/wsb/{ticker_selected}/?days=1000", headers=HEADERS).json()
    df = pd.DataFrame(data)

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

    posts_df = pd.read_sql_query("SELECT text_body, sentiment, date_posted FROM wsb_discussions WHERE ticker='{}' "
                                 "LIMIT 200".format(ticker_selected), cnx)

    return render(request, 'reddit/wsb_live_ticker.html', {"ticker_selected": ticker_selected,
                                                           "information": information,
                                                           "mentions_df": df.to_html(index=False),
                                                           "sentiment_df": sentiment_df.to_html(index=False),
                                                           "posts_df": posts_df.to_html(index=False),
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

    # Get trending tickers in the past 24H
    date_threshold = str(datetime.utcnow() - timedelta(hours=24))

    data = requests.get(f"{BASE_URL}/reddit/crypto/?days=1", headers=HEADERS).json()
    mentions_df = pd.DataFrame(data)

    # Get word cloud
    cur.execute("SELECT word, SUM(mentions) FROM crypto_word_cloud WHERE date_updated >= %s GROUP BY word ORDER BY "
                "SUM(mentions) DESC LIMIT 50", (date_threshold,))
    crypto_word_cloud = cur.fetchall()
    crypto_word_cloud = list(map(list, crypto_word_cloud))

    # Get trending tickers in the past 7 days
    data = requests.get(f"{BASE_URL}/reddit/crypto/?days=7", headers=HEADERS).json()
    mentions_7d_df = pd.DataFrame(data)

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

    data = requests.get(f"{BASE_URL}/reddit/crypto/{ticker_selected}/?days=1000", headers=HEADERS).json()
    df = pd.DataFrame(data)

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


def reverse_repo(request):
    """
    Get reverse repo. Data is from https://apps.newyorkfed.org/
    """
    data = requests.get(f"{BASE_URL}/economy/reverse_repo/?days=1000", headers=HEADERS).json()
    reverse_repo_stats = pd.DataFrame(data)

    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)

    return render(request, 'economy/reverse_repo.html',
                  {"reverse_repo_stats": reverse_repo_stats[::-1].to_html(index=False),
                   "next_date": data})


def daily_treasury(request):
    """
    Get daily treasury.
    Data is from https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/operating-cash-balance
    """
    data = requests.get(f"{BASE_URL}/economy/daily_treasury/?days=1000", headers=HEADERS).json()
    daily_treasury_stats = pd.DataFrame(data)

    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/daily_treasury.html',
                  {"daily_treasury_stats": daily_treasury_stats[::-1].to_html(index=False),
                   "next_date": data})


def inflation(request):
    """
    Get inflation. Data is from https://www.usinflationcalculator.com/inflation/current-inflation-rates/
    """
    data = requests.get(f"{BASE_URL}/economy/inflation/usa", headers=HEADERS).json()
    inflation_stats = pd.DataFrame(data).T
    inflation_stats.reset_index(inplace=True)
    inflation_stats.rename(columns={"index": "Year"}, inplace=True)

    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/inflation.html', {"inflation_stats": inflation_stats.to_html(index=False),
                                                      "next_date": data})


def world_inflation(request):
    """
    Get world inflation.
    """
    pd.options.display.float_format = '{:.2f}'.format
    data = requests.get(f"{BASE_URL}/economy/inflation/world", headers=HEADERS).json()
    inflation_stats = pd.DataFrame(data)
    return render(request, 'economy/world_inflation.html', {"inflation_stats": inflation_stats.to_html(index=False)})


def retail_sales(request):
    """
    Get retail sales. Data is from https://ycharts.com/indicators/us_retail_and_food_services_sales
    """
    data = requests.get(f"{BASE_URL}/economy/retail_sales/?days=1000", headers=HEADERS).json()
    retail_stats = pd.DataFrame(data)

    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/retail_sales.html',
                  {"retail_stats": retail_stats[::-1].to_html(index=False),
                   "next_date": data})


def initial_jobless_claims(request):
    data = requests.get(f"{BASE_URL}/economy/initial_jobless_claims/?days=1000", headers=HEADERS).json()
    jobless_claims = pd.DataFrame(data)

    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/initial_jobless_claims.html',
                  {"jobless_claims": jobless_claims[::-1].to_html(index=False),
                   "next_date": data})


def short_interest(request):
    """
    Get short interest of ticker. Data from https://www.stockgrid.io/shortinterest
    """
    data = requests.get(f"{BASE_URL}/discover/short_interest", headers=HEADERS).json()
    df_high_short_interest = pd.DataFrame(data)

    return render(request, 'discover/short_interest.html',
                  {"df_high_short_interest": df_high_short_interest.to_html(index=False)})


def low_float(request):
    """
    Get short interest of ticker. Data if from lowfloat.com
    """
    data = requests.get(f"{BASE_URL}/discover/low_float", headers=HEADERS).json()
    df_low_float = pd.DataFrame(data)

    return render(request, 'discover/low_float.html',
                  {"df_low_float": df_low_float.to_html(index=False)})


def ark_trades(request):
    """
    Get trades/positions of ARK Funds. Data from https://arkfunds.io/api
    """
    return render(request, 'discover/ark_trade.html')


def amd_xlnx_ratio(request):
    """
    Get latest ratio of AMD-XLNX (1.7234 if merger is successful)
    """
    pd.options.display.float_format = '{:.4f}'.format
    combined_df = pd.DataFrame()
    amd_df = yf.Ticker("AMD").history(interval="1d", period="1y")
    xlnx_df = yf.Ticker("XLNX").history(interval="1d", period="1y")

    combined_df["AMD $"] = amd_df["Close"].round(2)
    combined_df["XLNX $"] = xlnx_df["Close"].round(2)
    combined_df["XLNX % Upside"] = 100 * ((1.7234 * combined_df["AMD $"]) / combined_df["XLNX $"] - 1)
    combined_df["Ratio"] = combined_df["XLNX $"] / combined_df["AMD $"]
    combined_df["Ratio"] = combined_df["Ratio"].round(4)
    combined_df.reset_index(inplace=True)
    combined_df.rename(columns={"index": "Date"}, inplace=True)
    return render(request, 'discover/amd_xlnx_ratio.html', {"combined_df": combined_df[::-1].to_html(index=False)})


def ipo_calendar(request):
    data = requests.get(f"{BASE_URL}/discover/ipo_calendar", headers=HEADERS).json()
    df = pd.DataFrame(data)
    return render(request, 'discover/ipo_calendar.html', {"ipo_df": df.to_html(index=False)})


def correlation(request):
    pd.options.display.float_format = '{:.3f}'.format
    if request.GET.get("quotes"):
        symbols_list = request.GET['quotes'].upper().replace(" ", "")
    else:
        symbols_list = "AAPL, TSLA, SPY, AMC, GME, NVDA, XOM"
    # start = datetime(2017, 1, 1)
    try:
        df = yf.Tickers(symbols_list).history(period="1y")
    except KeyError:
        df = yf.Tickers("AAPL, TSLA, SPY, AMC, GME, NVDA, XOM").history(period="1y")
    df = df["Close"].corr(method='pearson')
    df.replace(1, "-", inplace=True)
    return render(request, 'discover/correlation.html', {"df": df.to_html(),
                                                         "symbols_list": symbols_list})


def stock_split(request):
    pd.options.display.float_format = '{:.3f}'.format
    data = requests.get(f"{BASE_URL}/discover/stock_split", headers=HEADERS).json()
    df = pd.DataFrame(data)
    return render(request, 'discover/stock_split.html', {"df": df.to_html(index=False)})


def dividend_history(request):
    pd.options.display.float_format = '{:.3f}'.format
    data = requests.get(f"{BASE_URL}/discover/dividend_history", headers=HEADERS).json()
    df = pd.DataFrame(data)

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

    data = requests.get(f"{BASE_URL}/stocktwits/{ticker_selected}", headers=HEADERS).json()
    ticker_df = pd.DataFrame(data)

    data = requests.get(f"{BASE_URL}/stocktwits", headers=HEADERS).json()
    trending_df = pd.DataFrame(data)

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

        data = requests.get(f"{BASE_URL}/discover/jim_cramer/{ticker_selected}", headers=HEADERS).json()
        ticker_df = pd.DataFrame(data)
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
        data = requests.get(f"{BASE_URL}/discover/jim_cramer", headers=HEADERS).json()
        df = pd.DataFrame(data)[:500]
        return render(request, 'discover/jim_cramer.html', {"df": df.to_html(index=False)})


def news(request):
    data = requests.get(f"{BASE_URL}/news/market_news", headers=HEADERS).json()
    df = pd.DataFrame(data)
    df.rename(columns={"Date": "Date [UTC]"}, inplace=True)
    return render(request, 'news/news.html', {"df": df.to_html(index=False)})


def twitter_feed(request):
    return render(request, 'news/twitter_feed.html')


def trading_halts(request):
    data = requests.get(f"{BASE_URL}/news/trading_halts", headers=HEADERS).json()
    df = pd.DataFrame(data)
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


def covid_beta(request):
    """
    Compare performance of ticker with covid cases
    """
    pd.options.display.float_format = '{:.3f}'.format
    return render(request, 'discover/beta_covid.html')


def about(request):
    """
    About section of the website and contact me if there's any issues/suggestions
    """
    if request.POST.get("name"):
        name = request.POST.get("name")
        email = request.POST.get("email")
        suggestions = request.POST.get("suggestions")
        send_email_to_self(name, email, suggestions)
    return render(request, 'about.html')


def loading_spinner(request):
    """
    Spinner display for iframe
    """
    return render(request, 'loading_spinner.html')


def subscribe_to_wsb_notifications(request):
    """
    Subscribe to Stocksera
    """
    if request.POST.get("name"):
        name = request.POST.get("name")
        email = request.POST.get("email")
        freq = request.POST.get("frequency")
        register_user(name, email, freq)
    return render(request, "admin/subscription.html")


def mailing_preference(request):
    """
    Change mailing preference
    """
    if request.POST.get("id"):
        edit_mailing_pref(request.POST.get("frequency"), request.POST.get("id"))
    if request.GET.get("id"):
        stats = get_user_id(request.GET.get("id"))
        if stats is not None:
            name, email, freq, user_id = stats
            return render(request, "admin/mailing_preference.html", {"name": name, "email": email,
                                                                     "freq": freq, "user_id": user_id})

    return redirect("/subscribe")


def unsubscribe(request):
    """
    Unsubscribe from Stocksera
    """
    if request.POST.get("id"):
        delete_user(request.POST.get("id"))
    if request.GET.get("id"):
        stats = get_user_id(request.GET.get("id"))
        if stats is not None:
            name, email, freq, user_id = stats
            return render(request, "admin/unsubscribe.html", {"name": name, "email": email, "user_id": user_id})
    return redirect("/subscribe")


def sample_email(request):
    return render(request, "admin/sample_email.html")


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})
