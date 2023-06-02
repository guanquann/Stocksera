from helpers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import schema
from rest_framework.schemas.openapi import AutoSchema
from rest_framework_api_key.models import APIKey
from rest_framework.decorators import api_view, permission_classes

cnx, cur, engine = connect_mysql_database()


def default_ticker(ticker):
    if not ticker:
        return "AAPL"
    return ticker.upper()


def get_days_params(request, default_days, max_days):
    try:
        num_days = int(request.GET.get("days", default_days))
        if num_days > max_days:
            num_days = max_days
    except ValueError:
        num_days = default_days

    date_threshold = str(datetime.utcnow() - timedelta(hours=24 * num_days))

    return date_threshold


def get_date(df, date_to, date_from, col_name="Date"):
    df[col_name] = df[col_name].astype(str)
    if date_to:
        df = df[df[col_name] <= date_to]
    if date_from:
        df = df[df[col_name] >= date_from]
    return df


def get_user_api(request):
    meta = request.META
    if "HTTP_AUTHORIZATION" in meta:
        return meta["HTTP_AUTHORIZATION"].split()[1]
    else:
        return ""


def check_validity(key):
    key = APIKey.objects.is_valid(key)
    local_url = config_keys["IS_LOCALLY_HOSTED"] is True
    if local_url:
        return True
    elif key and not local_url:
        return True
    else:
        return False


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


ERROR_MSG = JSONResponse({"Error": "Invalid API Key / Authorization Headers is empty"})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stocksera_api_key(request):
    data = request.data
    user = authenticate(username=data["username"], password=data["password"])
    if user:
        api_key, key = APIKey.objects.create_key(name=str(user))
        return JSONResponse({str(user): {"api_key": str(api_key), "key": str(key)}})
    else:
        return JSONResponse({"Anonymous": "Unauthorized Access"})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data["username"]
    email = request.data["email"]
    password = request.data["password"]
    if User.objects.filter(username=username).first():
        return JSONResponse({"Error": "Username is already taken"})
    user = User.objects.create_user(username, email, password)
    return JSONResponse({str(user): "User created successfully"})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data["username"]
    password = request.data["password"]
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)
    if user is not None:
        return JSONResponse({str(user): "No error"})
    else:
        return JSONResponse({"Anonymous": "Error logging in"})


class AutoDocstringSchema(AutoSchema):
    @property
    def documentation(self):
        if not hasattr(self, "_documentation"):
            try:
                self._documentation = yaml.safe_load(self.view.__doc__)
            except yaml.scanner.ScannerError:
                self._documentation = {}
        return self._documentation

    def get_components(self, path, method):
        components = super().get_components(path, method)
        doc_components = self.documentation.get("components", {})
        components.update(doc_components)
        return components

    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        doc_operation = self.documentation.get(method.lower(), {})
        operation.update(doc_operation)
        return operation


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def stocksera_trending(request):
    """
    Get most searched tickers in Stocksera.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query("SELECT * FROM stocksera_trending ORDER BY count DESC LIMIT 10", cnx)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def sec_fillings(request, ticker_selected="AAPL"):
    """
    Get SEC fillings of tickers.
    """
    key = get_user_api(request)
    if check_validity(key):
        ticker_selected = default_ticker(ticker_selected)
        df = get_sec_fillings(ticker_selected)
        df = get_date(df, request.GET.get("date_to"), request.GET.get("date_from"), "Filling Date")
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def news_sentiment(request, ticker_selected="AAPL"):
    """
    Show news and sentiment of tickers.
    """
    key = get_user_api(request)
    if check_validity(key):
        ticker_selected = default_ticker(ticker_selected)
        df = get_ticker_news(ticker_selected)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def insider_trading(request, ticker_selected="AAPL"):
    """
    Get ticker's insider trading data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        ticker_selected = default_ticker(ticker_selected)
        get_insider_trading(ticker_selected)
        df = pd.read_sql_query("SELECT * FROM insider_trading WHERE Ticker='{}' ".format(ticker_selected), cnx)
        df.rename(columns={"TransactionDate": "Date",
                           "TransactionType": "Transaction",
                           "Value": "Value ($)",
                           "SharesLeft": "#Shares Total",
                           "URL": ""}, inplace=True)
        del df["Ticker"]
        df = get_date(df, request.GET.get("date_to"), request.GET.get("date_from"))
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def latest_insider_summary(request):
    """
    Get latest insider trading summary.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query("SELECT * FROM latest_insider_trading_analysis", cnx)
        df.rename(columns={"MktCap": "Market Cap", "Proportion": "% of Mkt Cap"}, inplace=True)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def latest_insider(request):
    """
    Get latest insider trading data of all tickers.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        try:
            n_rows = int(request.GET.get("limit", 500))
            if n_rows <= 0 or n_rows > 5000:
                n_rows = 500
        except ValueError:
            n_rows = 500

        df = pd.read_sql_query("SELECT * FROM latest_insider_trading ORDER BY DateFilled DESC LIMIT {}".format(n_rows),
                               cnx)

        df.rename(columns={"TransactionDate": "Date",
                           "TransactionType": "Transaction",
                           "Value": "Value ($)",
                           "SharesLeft": "#Shares Total",
                           "URL": ""}, inplace=True)

        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def top_short_volume(request):
    """
    Get tickers with the highest short volume for the day.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        pd.options.display.float_format = '{:.2f}'.format
        df = pd.read_sql_query("SELECT * FROM highest_short_volume", cnx)
        df.fillna('', inplace=True)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def short_volume(request, ticker_selected="AAPL"):
    """
    Get short volume of tickers.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()

        ticker_selected = default_ticker(ticker_selected)

        df = pd.read_sql_query(
            "SELECT * FROM short_volume WHERE Ticker='{}' ORDER BY Date DESC".format(ticker_selected), cnx)
        del df["Ticker"]
        history = pd.DataFrame(yf.Ticker(ticker_selected).history(interval="1d", period="1y")["Close"])
        history.reset_index(inplace=True)
        history["Date"] = history["Date"].astype(str)
        df = pd.merge(df, history, on=["Date"], how="left")
        df.rename(columns={"close_price": "Close Price"}, inplace=True)
        df = get_date(df, request.GET.get("date_to"), request.GET.get("date_from"))
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def top_failure_to_deliver(request):
    """
    Get tickers with most FTD.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        top_ftd = pd.read_sql_query("SELECT * FROM top_ftd", cnx)
        top_ftd = top_ftd.replace(np.nan, "")
        df = top_ftd.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def failure_to_deliver(request, ticker_selected="AAPL"):
    """
    Get FTD of tickers.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        ticker_selected = default_ticker(ticker_selected)

        ftd = pd.read_sql_query("SELECT * FROM ftd WHERE Ticker='{}' ORDER BY Date DESC".format(ticker_selected), cnx)
        del ftd["Ticker"]
        if not ftd.empty:
            ftd["Amount (FTD x $)"] = (ftd["Failure to Deliver"].astype(int) * ftd["Price"].astype(float)).astype(int)
            ftd = ftd[['Date', 'Failure to Deliver', 'Price', 'Amount (FTD x $)', 'T+35 Date']]
        ftd = get_date(ftd, request.GET.get("date_to"), request.GET.get("date_from"))
        df = ftd.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def regsho(request, ticker_selected=None):
    """
    Get Regulation SHO data from SEC
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()

        if ticker_selected:
            ticker_selected = default_ticker(ticker_selected)
            df = pd.read_sql_query("SELECT * FROM threshold_securities WHERE ticker='{}' ORDER BY date_updated DESC"
                                   .format(ticker_selected), cnx)
            df.rename(columns={"ticker": "Ticker", "date_updated": "Date"}, inplace=True)
            if df.empty:
                df = pd.DataFrame({"Ticker": [ticker_selected], "Close": ["N/A"], "Date": ["N/A"]})
            else:
                history = pd.DataFrame(yf.Ticker(ticker_selected).history(interval="1d", period="5y")["Close"])
                history.reset_index(inplace=True)
                history["Date"] = history["Date"].astype(str)
                df = pd.merge(df, history, on=["Date"], how="left")
                df = df[["Ticker", "Close", "Date"]]

        else:
            df = pd.read_sql_query("SELECT * FROM threshold_securities ORDER BY date_updated DESC", cnx)
            df.rename(columns={"ticker": "Ticker", "date_updated": "Date"}, inplace=True)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def earnings_calendar(request):
    """
    Get tickers with upcoming earnings.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query("SELECT * FROM earnings ORDER BY date ASC", cnx)
        df = get_date(df, request.GET.get("date_to"), request.GET.get("date_from"), "date")
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def market_news(request):
    """
    Get breaking, crypto, forex and merger news.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql("SELECT * FROM market_news ORDER BY Date DESC LIMIT 1000", cnx)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    else:
        return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def trading_halts(request):
    """
    Get stocks with trading halts.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql("SELECT * FROM trading_halts ORDER BY `Halt Date` DESC, `Halt Time` DESC LIMIT 3000", cnx)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def subreddit_count(request, ticker_selected="GME"):
    """
    Get Reddit subreddit user count, growth, active users over time.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        ticker_selected = default_ticker(ticker_selected)
        date_threshold = get_days_params(request, 100, 1000)
        df = pd.read_sql_query("SELECT * FROM subreddit_count WHERE ticker = '{}' AND "
                               "updated_date >= '{}' ".format(ticker_selected, date_threshold), cnx)
        del df["ticker"]
        df.rename(columns={"subscribers": "Redditors", "active": "Active", "updated_date": "Date",
                           "percentage_active": "% Active", "growth": "% Growth",
                           "percentage_price_change": "% Price Change"}, inplace=True)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def reddit_mentions(request, subreddit="wsb", ticker_selected=None):
    """
    Get most mentioned tickers on Reddit.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        if subreddit.lower() != "crypto":
            subreddit = "wsb"
            fields = "mentions, calls, puts"
        else:
            fields = "mentions"

        if ticker_selected:
            pd.options.display.float_format = '{:.2f}'.format
            date_threshold = get_days_params(request, 100, 1000)
            df = pd.read_sql_query(
                "SELECT {}, date_updated FROM {}_trending_hourly WHERE ticker='{}' AND date_updated >= "
                "'{}' ORDER by date_updated DESC".format(fields, subreddit, ticker_selected,
                                                         date_threshold), cnx)
            df.fillna(0, inplace=True)
        else:
            date_threshold = get_days_params(request, 1, 14)

            query = "SELECT ticker AS Ticker, CAST(SUM(mentions) AS UNSIGNED) AS Mentions, " \
                    "AVG(sentiment) AS Sentiment FROM {}_trending_24H WHERE date_updated >= '{}' GROUP BY ticker " \
                    "ORDER BY SUM(mentions) DESC".format(subreddit, date_threshold)
            df = pd.read_sql_query(query, cnx)
            df.index += 1
            df.reset_index(inplace=True)
            df.rename(columns={"index": "Rank"}, inplace=True)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def wsb_options(request):
    """
    Get stock options activity on Reddit r/wallstreetbets.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        date_threshold = get_days_params(request, 1, 14)

        df = pd.read_sql_query("SELECT ticker as Ticker, CAST(SUM(calls) AS UNSIGNED) AS Calls, CAST(SUM(puts) "
                               "AS UNSIGNED) AS Puts, CAST(SUM(calls) AS UNSIGNED)/SUM(puts) as Ratio FROM "
                               "wsb_trending_24H WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(puts + calls) "
                               "DESC LIMIT 30".format(date_threshold), cnx)
        df.fillna(0, inplace=True)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def government(request, gov_type="senate"):
    """
    Get congress trading data.
    """
    key = get_user_api(request)
    if check_validity(key):
        mapping_dict = {"senate": "Senator", "house": "Representative"}
        col_name = mapping_dict[gov_type]

        name = request.GET.get("name")
        ticker = request.GET.get("ticker")
        state = request.GET.get("state")

        df = pd.read_csv(f"database/government/{gov_type}.csv")
        df["Disclosure Date"] = df["Disclosure Date"].astype(str)
        df.fillna(0, inplace=True)
        df_copy = df.copy()

        final_dict = {}
        if name:
            name_list = df_copy[col_name].drop_duplicates().sort_values().to_list()
            df = df[df[col_name] == name]
            final_dict = {**final_dict, **{"names_available": name_list}}
        if ticker:
            ticker_list = df_copy["Ticker"].drop_duplicates().sort_values().to_list()
            ticker_list.remove("Unknown")
            ticker_list.sort()
            ticker = ticker.upper()
            df = df[df["Ticker"] == ticker]
            del df["Ticker"]
            del df["Asset Description"]
            final_dict = {**final_dict, **{"tickers_available": ticker_list}}
        if state:
            district_list = df_copy["District"].str[:2].unique().tolist()
            state = state.upper()
            df = df[df["District"].str.contains(state)]
            final_dict = {**final_dict, **{"districts_available": district_list}}
        df = get_date(df, request.GET.get("date_to"), request.GET.get("date_from"), "Transaction Date")
        df = df.to_dict(orient="records")
        final_dict = {**{gov_type: df}, **final_dict}
        return JSONResponse(final_dict)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def reverse_repo(request):
    """
    Get reverse repo data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        date_threshold = get_days_params(request, 100, 10000)
        reverse_repo_stats = pd.read_sql_query("SELECT * FROM reverse_repo "
                                               "WHERE record_date >= '{}' ".format(date_threshold), cnx)
        reverse_repo_stats['Moving Avg'] = reverse_repo_stats['amount'].rolling(window=7).mean()
        reverse_repo_stats.rename(columns={"record_date": "Date", "amount": "Amount", "parties": "Num Parties",
                                           "average": "Average"}, inplace=True)
        reverse_repo_stats.fillna(0, inplace=True)
        df = reverse_repo_stats.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def daily_treasury(request):
    """
    Get daily treasury data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        date_threshold = get_days_params(request, 100, 10000)
        daily_treasury_stats = pd.read_sql_query("SELECT * FROM daily_treasury WHERE record_date >= '{}' "
                                                 "ORDER BY record_date".format(date_threshold), cnx)
        daily_treasury_stats['Moving Avg'] = daily_treasury_stats['close_today_bal'].rolling(window=7).mean()
        daily_treasury_stats.rename(columns={"record_date": "Date", "close_today_bal": "Close Balance",
                                             "open_today_bal": "Open Balance", "amount_change": "Amount Change",
                                             "percent_change": "Percent Change"},
                                    inplace=True)
        daily_treasury_stats.fillna(0, inplace=True)
        df = daily_treasury_stats.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def inflation(request, area="usa"):
    """
    Get inflation data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.1f}'.format
        cnx, cur, engine = connect_mysql_database()
        if area == "world":
            inflation_stats = pd.read_sql_query("SELECT * FROM world_inflation", cnx)
            inflation_stats.fillna(0, inplace=True)
            df = inflation_stats.to_dict(orient="records")
        else:
            inflation_stats = pd.read_sql_query("SELECT * FROM usa_inflation", cnx)
            inflation_stats.set_index("Year", inplace=True)
            inflation_stats.fillna(0, inplace=True)
            df = inflation_stats.to_dict(orient="index")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def retail_sales(request):
    """
    Get retail sales data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        date_threshold = get_days_params(request, 100, 10000)
        retail_stats = pd.read_sql_query("SELECT * FROM retail_sales "
                                         "WHERE record_date >= '{}' ".format(date_threshold), cnx)
        retail_stats.rename(columns={"record_date": "Date", "value": "Amount", "percent_change": "Percent Change",
                                     "covid_monthly_avg": "Monthly Avg Cases"}, inplace=True)
        retail_stats.fillna(0, inplace=True)
        df = retail_stats.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def interest_rate(request):
    """
    Get interest rate data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query("SELECT * FROM interest_rates", cnx)
        df.rename(columns={"record_date": "Date", "interest": "Rate"}, inplace=True)
        df.fillna(0, inplace=True)
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def initial_jobless_claims(request):
    """
    Get initial jobless claims data.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        date_threshold = get_days_params(request, 100, 10000)
        jobless_claims = pd.read_sql_query("SELECT * FROM initial_jobless_claims "
                                           "WHERE record_date >= '{}' ".format(date_threshold), cnx)
        jobless_claims.rename(columns={"record_date": "Date", "value": "Number", "percent_change": "Percent Change"
                                       }, inplace=True)
        jobless_claims.fillna(0, inplace=True)
        df = jobless_claims.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def short_interest(request):
    """
    Get tickers with highest short interest.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        df_high_short_interest = pd.read_sql_query("SELECT * FROM short_interest", con=cnx)
        df_high_short_interest.reset_index(inplace=True)
        df_high_short_interest.rename(columns={"index": "Rank"}, inplace=True)
        df_high_short_interest["Rank"] = df_high_short_interest["Rank"] + 1
        df = df_high_short_interest.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def low_float(request):
    """
    Get tickers with low float.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()
        df_low_float = pd.read_sql_query("SELECT * FROM low_float", con=cnx)
        df_low_float.reset_index(inplace=True)
        df_low_float.rename(columns={"index": "Rank"}, inplace=True)
        df_low_float["Rank"] = df_low_float["Rank"] + 1
        df = df_low_float.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def ipo_calendar(request):
    """
    Get upcoming and past IPOs.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query("SELECT * FROM ipo_calendar", con=cnx)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def stocktwits(request, ticker_selected=None):
    """
    Get popular tickers on Stocktwits.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        if ticker_selected:
            ticker_selected = default_ticker(ticker_selected)
            df = pd.read_sql_query("SELECT `rank`, watchlist, date_updated FROM stocktwits_trending WHERE "
                                   "ticker='{}' ".format(ticker_selected), cnx)
        else:
            df = pd.read_sql_query("SELECT `rank`, watchlist, ticker FROM stocktwits_trending "
                                   "ORDER BY date_updated DESC, `rank` ASC LIMIT 30", cnx)
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def market_summary(request):
    """
    Get market summary of Nasdaq/DOW/S&P500.
    """
    key = get_user_api(request)
    if check_validity(key):
        pd.options.display.float_format = '{:.2f}'.format
        cnx, cur, engine = connect_mysql_database()

        if request.GET.get("type") == "nasdaq100":
            filename = "database/indices/nasdaq100_heatmap.csv"
            title = "Nasdaq 100"
        elif request.GET.get("type") == "dia":
            filename = "database/indices/dia_heatmap.csv"
            title = "DIA"
        elif request.GET.get("type") == "wsb":
            title = "Wallstreetbets"
            df = pd.read_sql_query("SELECT ticker, mentions, mkt_cap, price_change FROM wsb_yf", cnx)
            df.fillna(0, inplace=True)
            df = {title: df.to_dict(orient="records")}
            return JSONResponse(df)
        else:
            filename = "database/indices/snp500_heatmap.csv"
            title = "S&P 500"

        df = pd.read_csv(filename)
        df.fillna("N/A", inplace=True)
        return JSONResponse({title: df.to_dict(orient="records")})
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def jim_cramer(request, ticker_selected=None):
    """
    Get Jim Cramer's recommendations.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query("SELECT DISTINCT * FROM jim_cramer_trades ORDER BY Date DESC", cnx)
        if ticker_selected:
            df = df[df["Ticker"] == ticker_selected.upper()]
        if request.GET.get("segment"):
            df = df[df["Segment"] == request.GET.get("segment").title()]
        if request.GET.get("call"):
            df = df[df["Call"] == request.GET.get("call").title()]
        df = get_date(df, request.GET.get("date_to"), request.GET.get("date_from"))
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def borrowed_shares(request, ticker_selected=""):
    """
    Get borrow fees and shares available.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        if ticker_selected:
            df = pd.read_sql_query(f"SELECT * FROM shares_available WHERE ticker='{ticker_selected.upper()}' "
                                   f"ORDER BY date_updated DESC", cnx)
        else:
            cur.execute("SELECT date_updated FROM shares_available ORDER BY date_updated DESC LIMIT 1")
            latest_date = cur.fetchone()[0]
            df = pd.read_sql_query(f"SELECT * FROM shares_available WHERE date_updated='{latest_date}' LIMIT 15000",
                                   cnx)
        df = df.replace(np.nan, "")
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def stock_split(request):
    """
    Get stock split history.
    """
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query(f"SELECT * FROM stock_splits ORDER BY `Date` DESC", cnx)
        df = df.replace(np.nan, "")
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG


@csrf_exempt
@api_view(['GET'])
@schema(AutoDocstringSchema())
def dividend_history(request):
    key = get_user_api(request)
    if check_validity(key):
        cnx, cur, engine = connect_mysql_database()
        df = pd.read_sql_query(f"SELECT * FROM dividends ORDER BY `Declaration Date` DESC", cnx)
        df = df.replace(np.nan, "")
        df = df.to_dict(orient="records")
        return JSONResponse(df)
    return ERROR_MSG
