from helpers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def default_ticker(ticker):
    if not ticker:
        return "AAPL"
    return ticker.upper()


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def stocksera_trending(request):
    df = pd.read_sql_query("SELECT * FROM stocksera_trending ORDER BY count DESC LIMIT 10", conn)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def sec_fillings(request, ticker_selected="AAPL"):
    ticker_selected = default_ticker(ticker_selected)
    df = pd.read_sql_query("SELECT * FROM sec_fillings WHERE ticker='{}' ".format(ticker_selected), conn)
    if df.empty:
        df = get_sec_fillings(ticker_selected)
    else:
        del df["ticker"]
        df.rename(columns={"filling": "Filling", "description": "Description", "filling_date": "Filling Date"},
                  inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def news_sentiment(request, ticker_selected="AAPL"):
    """
    Show news and sentiment of ticker in /ticker?quote={TICKER}. Data from Finviz
    Note: News are only available if hosted locally. Read README.md for more details
    """
    ticker_selected = default_ticker(ticker_selected)
    df = pd.read_sql_query("SELECT * FROM daily_ticker_news WHERE ticker='{}' ".format(ticker_selected), conn)
    if df.empty:
        df = get_ticker_news(ticker_selected)
    else:
        del df["Ticker"]
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def insider_trading(request, ticker_selected="AAPL"):
    """
    Get a specific ticker's insider trading data from Finviz
    """
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(ticker_selected)
    df = pd.read_sql_query("SELECT * FROM insider_trading WHERE Ticker='{}' ".format(ticker_selected), conn)
    if df.empty:
        get_insider_trading(ticker_selected)
        df = pd.read_sql_query("SELECT * FROM insider_trading WHERE Ticker='{}' ".format(ticker_selected), conn)
    else:
        df.rename(columns={"TransactionDate": "Date",
                           "TransactionType": "Transaction",
                           "Value": "Value ($)",
                           "SharesLeft": "#Shares Total",
                           "URL": ""}, inplace=True)
    del df["Ticker"]
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def latest_insider_summary(request):
    """
    Get latest insider trading data from Finviz and perform analysis
    """
    pd.options.display.float_format = '{:.2f}'.format

    df = pd.read_sql_query("SELECT * FROM latest_insider_trading_analysis", conn)
    df.rename(columns={"MktCap": "Market Cap", "Proportion": "% of Mkt Cap"}, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def latest_insider(request):
    """
    Get latest insider trading data from Finviz and perform analysis
    """
    pd.options.display.float_format = '{:.2f}'.format
    try:
        n_rows = int(request.GET.get("limit", 500))
        if n_rows <= 0 or n_rows > 5000:
            n_rows = 500
    except ValueError:
        n_rows = 500

    df = pd.read_sql_query("SELECT * FROM latest_insider_trading ORDER BY DateFilled DESC LIMIT {}".format(n_rows),
                           conn)

    df.rename(columns={"TransactionDate": "Date",
                       "TransactionType": "Transaction",
                       "Value": "Value ($)",
                       "SharesLeft": "#Shares Total",
                       "URL": ""}, inplace=True)

    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def top_short_volume(request):
    pd.options.display.float_format = '{:.2f}'.format
    df = pd.read_csv(r"database/highest_short_volume.csv")
    df.fillna('', inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def short_volume(request, ticker_selected="AAPL"):
    """
    Get short volume of tickers (only popular ones). Data from Finra
    """
    pd.options.display.float_format = '{:.2f}'.format

    ticker_selected = default_ticker(ticker_selected)

    df = pd.read_csv("database/short_volume.csv")
    df = df[df["ticker"] == ticker_selected][::-1]
    history = pd.DataFrame(yf.Ticker(ticker_selected).history(interval="1d", period="1y")["Close"])
    history.reset_index(inplace=True)
    history["Date"] = history["Date"].astype(str)
    df = pd.merge(df, history, on=["Date"], how="left")
    df.rename(columns={"reported_date": "Date", "short_vol": "Short Volume",
                       "short_exempt_vol": "Short Exempt Vol", "total_vol": "Total Volume",
                       "percent": "% Shorted", "close_price": "Close Price"}, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def top_failure_to_deliver(request):
    top_ftd = pd.read_csv(r"database/failure_to_deliver/top_ftd.csv")
    top_ftd = top_ftd.replace(np.nan, "")
    df = top_ftd.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def failure_to_deliver(request, ticker_selected="AAPL"):
    """
    Get FTD of tickers. Data from SEC
    """
    ticker_selected = default_ticker(ticker_selected)

    ftd = pd.read_csv(r"database/failure_to_deliver/ftd.csv")
    ftd = ftd[ftd["Symbol"] == ticker_selected]
    ftd = ftd[::-1]
    ftd["Amount (FTD x $)"] = (ftd["Failure to Deliver"].astype(int) * ftd["Price"].astype(float)).astype(int)
    del ftd["Symbol"]
    ftd = ftd[['Date', 'Failure to Deliver', 'Price', 'Amount (FTD x $)', 'T+35 Date']]
    df = ftd.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def earnings_calendar(request):
    """
    Get earnings for the upcoming week. Data from yahoo finance
    """
    df = pd.read_sql_query("SELECT * FROM earnings_calendar ORDER BY earning_date ASC", conn)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def subreddit_count(request, ticker_selected="GME"):
    """
    Get subreddit user count, growth, active users over time.
    """
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(ticker_selected)
    df = pd.read_sql_query("SELECT * FROM subreddit_count WHERE ticker='{}'".format(ticker_selected), conn)
    del df["ticker"]
    df.rename(columns={"subscribers": "Redditors", "active": "Active", "updated_date": "Date",
                       "percentage_active": "% Active", "growth": "% Growth",
                       "percentage_price_change": "% Price Change"}, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def wsb_mentions(request, ticker_selected=None):
    if ticker_selected:
        pd.options.display.float_format = '{:.2f}'.format
        df = pd.read_sql_query("SELECT mentions, calls, puts, date_updated FROM wsb_trending_hourly WHERE "
                               "ticker='{}' ".format(ticker_selected), conn)
        df.fillna(0, inplace=True)
    else:
        try:
            num_days = int(request.GET.get("days", 1))
        except ValueError:
            num_days = 1

        date_threshold = str(datetime.utcnow() - timedelta(hours=24 * num_days))

        query = "SELECT ticker AS Ticker, SUM(mentions) AS Mentions, AVG(sentiment) AS Sentiment FROM wsb_trending_24H " \
                "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) DESC".format(date_threshold)

        df = pd.read_sql_query(query, conn)
        df.index += 1
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Rank"}, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def wsb_options(request, ticker_selected=None):
    if ticker_selected:
        df = pd.read_sql_query("SELECT AVG(sentiment) as sentiment, strftime('%Y-%m-%d', date_updated) AS "
                               "date_updated FROM wsb_trending_hourly WHERE ticker='{}' "
                               "group by strftime('%Y-%m-%d', date_updated)".format(ticker_selected), conn)
    else:
        try:
            num_days = int(request.GET.get("days", 1))
        except ValueError:
            num_days = 1

        date_threshold = str(datetime.utcnow() - timedelta(hours=24 * num_days))

        df = pd.read_sql_query("SELECT ticker as Ticker, SUM(calls) AS Calls, SUM(puts) AS Puts, "
                               "CAST(SUM(calls) AS float)/SUM(puts) as Ratio FROM wsb_trending_24H "
                               "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(puts + calls) "
                               "DESC LIMIT 30".format(date_threshold), conn)
    df.fillna(0, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def senate_trades(request):
    name = request.GET.get("name")
    ticker = request.GET.get("ticker")
    df = pd.read_csv("database/government/senate.csv")
    if name:
        df = df[df["Senator"] == name]
    if ticker:
        df = df[df["Ticker"] == ticker.upper()]
    df["Disclosure Date"] = df["Disclosure Date"].astype(str)
    df.fillna(0, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def house_trades(request):
    name = request.GET.get("name")
    ticker = request.GET.get("ticker")
    df = pd.read_csv("database/government/house.csv")
    if name:
        df = df[df["Representative"] == name]
    if ticker:
        df = df[df["Ticker"] == ticker.upper()]
    df["Disclosure Date"] = df["Disclosure Date"].astype(str)
    df.fillna(0, inplace=True)
    df = df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def reverse_repo(request):
    pd.options.display.float_format = '{:.2f}'.format
    reverse_repo_stats = pd.read_sql_query("SELECT * FROM reverse_repo", conn)
    reverse_repo_stats['Moving Avg'] = reverse_repo_stats['amount'].rolling(window=7).mean()
    reverse_repo_stats.rename(columns={"record_date": "Date", "amount": "Amount", "parties": "Num Parties",
                                       "average": "Average"}, inplace=True)
    reverse_repo_stats.fillna(0, inplace=True)
    df = reverse_repo_stats.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def daily_treasury(request):
    pd.options.display.float_format = '{:.2f}'.format
    daily_treasury_stats = pd.read_sql_query("SELECT * FROM daily_treasury", conn)
    daily_treasury_stats['Moving Avg'] = daily_treasury_stats['close_today_bal'].rolling(window=7).mean()
    daily_treasury_stats.rename(columns={"record_date": "Date", "close_today_bal": "Close Balance",
                                         "open_today_bal": "Open Balance", "amount_change": "Amount Change",
                                         "percent_change": "Percent Change"},
                                inplace=True)
    daily_treasury_stats.fillna(0, inplace=True)
    df = daily_treasury_stats.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def inflation(request):
    pd.options.display.float_format = '{:.1f}'.format
    inflation_stats = pd.read_sql_query("SELECT * FROM inflation", conn)
    inflation_stats.set_index("Year", inplace=True)
    inflation_stats.fillna(0, inplace=True)
    df = inflation_stats.to_dict(orient="index")
    return JSONResponse(df)


@csrf_exempt
def retail_sales(request):
    """
    Get retail sales. Data is from https://ycharts.com/indicators/us_retail_and_food_services_sales
    """
    pd.options.display.float_format = '{:.2f}'.format
    retail_stats = pd.read_sql_query("SELECT * FROM retail_sales", conn)
    retail_stats.rename(columns={"record_date": "Date", "value": "Amount", "percent_change": "Percent Change",
                                 "covid_monthly_avg": "Monthly Avg Cases"}, inplace=True)
    retail_stats.fillna(0, inplace=True)
    df = retail_stats.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def initial_jobless_claims(request):
    pd.options.display.float_format = '{:.2f}'.format
    jobless_claims = pd.read_sql_query("SELECT * FROM initial_jobless_claims", conn)
    jobless_claims.rename(columns={"record_date": "Date", "value": "Number", "percent_change": "Percent Change"
                                   }, inplace=True)
    jobless_claims.fillna(0, inplace=True)
    df = jobless_claims.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def short_interest(request):
    """
    Get short interest of ticker. Data from https://www.stockgrid.io/shortinterest
    """
    pd.options.display.float_format = '{:.2f}'.format
    df_high_short_interest = pd.read_sql("SELECT * FROM short_interest", con=conn)
    df_high_short_interest.reset_index(inplace=True)
    df_high_short_interest.rename(columns={"index": "Rank"}, inplace=True)
    df_high_short_interest["Rank"] = df_high_short_interest["Rank"] + 1
    df = df_high_short_interest.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def low_float(request):
    """
    Get short interest of ticker. Data if from lowfloat.com
    """
    pd.options.display.float_format = '{:.2f}'.format
    df_low_float = pd.read_sql("SELECT * FROM low_float", con=conn)
    df_low_float.reset_index(inplace=True)
    df_low_float.rename(columns={"index": "Rank"}, inplace=True)
    df_low_float["Rank"] = df_low_float["Rank"] + 1
    df = df_low_float.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def ipo_calendar(request):
    df = pd.read_csv("database/ipo_calendar.csv").to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def stocktwits(request, ticker_selected="TSLA"):
    ticker_selected = default_ticker(ticker_selected)
    ticker_df = pd.read_sql_query("SELECT rank, watchlist, date_updated FROM stocktwits_trending WHERE "
                                  "symbol='{}' ".format(ticker_selected), conn)
    df = ticker_df.to_dict(orient="records")
    return JSONResponse(df)


@csrf_exempt
def jim_cramer(request, ticker_selected=""):
    df = pd.read_sql_query("SELECT * FROM jim_cramer_trades ORDER BY Date DESC", conn)
    if ticker_selected:
        df = df[df["Symbol"] == ticker_selected.upper()]
    df = df.to_dict(orient="records")
    return JSONResponse(df)
