import os
import yaml
import numpy as np
import finnhub
import yfinance as yf
import mysql.connector
from datetime import date
from sqlalchemy import create_engine
from django.http import HttpResponse
from finvizfinance.quote import finvizfinance
from json.decoder import JSONDecodeError
from fast_yahoo import *
from custom_extensions.custom_words import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

with open("config.yaml") as config_file:
    config_keys = yaml.load(config_file, Loader=yaml.Loader)

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

# https://finnhub.io/
finnhub_client = finnhub.Client(api_key=config_keys["FINNHUB_KEY1"])

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                        "50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}

engine = create_engine(f'mysql://{config_keys["MYSQL_USER"]}:{config_keys["MYSQL_PASSWORD"]}@'
                       f'{config_keys["MYSQL_HOST"]}/{config_keys["MYSQL_DATABASE"]}')
cnx = mysql.connector.connect(user=config_keys["MYSQL_USER"],
                              password=config_keys["MYSQL_PASSWORD"],
                              host=config_keys["MYSQL_HOST"],
                              database=config_keys["MYSQL_DATABASE"])
cnx.autocommit = True
cur = cnx.cursor()


def connect_mysql_database():
    global engine
    global cnx
    global cur
    if not cnx.is_connected():
        engine = create_engine(f'mysql://{config_keys["MYSQL_USER"]}:{config_keys["MYSQL_PASSWORD"]}@'
                               f'{config_keys["MYSQL_HOST"]}/{config_keys["MYSQL_DATABASE"]}')
        cnx = mysql.connector.connect(user=config_keys["MYSQL_USER"],
                                      password=config_keys["MYSQL_PASSWORD"],
                                      host=config_keys["MYSQL_HOST"],
                                      database=config_keys["MYSQL_DATABASE"])
        cnx.autocommit = True
        cur = cnx.cursor()
    return cnx, cur, engine


def default_ticker(request, ticker="AAPL"):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper().replace(" ", "")
    else:
        ticker_selected = ticker
    return ticker_selected


def get_all_tickers():
    """
    Get full ticker list for dropdown box
    """
    all_ticker_list = pd.read_csv(r"database/all_tickers.csv")
    symbol_list = all_ticker_list["SYMBOL"].to_list()
    description = all_ticker_list["DESCRIPTION"].to_list()
    return symbol_list, description


def check_json(r):
    """
    Sometimes when updating json file, there would be an error raised. This function fix this problem
    """
    try:
        data = json.load(r)
    except JSONDecodeError as e:
        print(e)
        data = {}
    return data


def check_market_hours(ticker_selected):
    """
    1. Cache ticker information into a json file to speed up rendering time.
    2. Insert ticker symbol into Stocksera trending table in db
    3. Find related tickers to ticker selected
    Parameters
    ----------
    ticker_selected: str
        ticker symbol (e.g: AAPL)
    """
    current_datetime = datetime.utcnow()

    next_update_time = str(current_datetime + timedelta(seconds=600))
    with open(r"database/yf_cached_api.json", "r+") as r:
        data = check_json(r)
        if ticker_selected in data and str(current_datetime) < data[ticker_selected]["next_update"]:
            information = data[ticker_selected]
        else:
            information = download_advanced_stats([ticker_selected])
            data.update(information)
            information = data[ticker_selected]

            information["next_update"] = next_update_time
            r.seek(0)
            r.truncate()
            json.dump(data, r, indent=4)

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        if "." not in ticker_selected:
            cur.execute("INSERT INTO stocksera_trending (ticker, name, count) VALUES (%s, %s, 1) ON DUPLICATE "
                        "KEY UPDATE count=count+1", (ticker_selected, information["longName"]))
            cnx.commit()

        cur.execute("SELECT * FROM related_tickers WHERE ticker=%s", (ticker_selected, ))
        related_tickers = cur.fetchall()
        if not related_tickers:
            related_tickers = finnhub_client.company_peers(ticker_selected)
            if ticker_selected in related_tickers:
                related_tickers.remove(ticker_selected)
            upload_to_db = related_tickers.copy()
            while len(upload_to_db) <= 6:
                upload_to_db += [""]
            cur.execute("INSERT INTO related_tickers VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        tuple([ticker_selected] + upload_to_db[:6]))
            cnx.commit()
        else:
            related_tickers = list(related_tickers[0])[1:]
            related_tickers = [i for i in related_tickers if i != ""]
        if not related_tickers:
            related_tickers = ["AAPL", "TSLA", "NVDA"]
    else:
        related_tickers = []
    return information, related_tickers


def check_financial_data(ticker_selected, ticker, data, r):
    """
    Get financial data of ticker selected and save to json file
    """
    balance_sheet = ticker.quarterly_balance_sheet
    balance_sheet = balance_sheet.replace(np.nan, 0)[balance_sheet.columns[::-1]]
    date_list = balance_sheet.columns.astype("str").to_list()
    balance_col_list = balance_sheet.index.tolist()
    balance_list = []

    for i in range(len(balance_sheet)):
        values = balance_sheet.iloc[i].tolist()
        balance_list.append(values)
    data[ticker_selected] = {
        "date_list": date_list,
        "balance_list": balance_list,
        "balance_col_list": balance_col_list,
        "next_update": str(datetime.now().date() + timedelta(days=7))
    }
    r.seek(0)
    r.truncate()
    json.dump(data, r, indent=4)
    return date_list, balance_list, balance_col_list


def convert_date(date):
    return date[0].split()[0]


def get_sec_fillings(ticker_selected):
    current_date = datetime.utcnow().date()
    sec_list = finnhub_client.filings(symbol=ticker_selected, _from=str(current_date - timedelta(days=365*3)),
                                      to=str(current_date))[:100]
    for filling in sec_list:
        ticker = filling["symbol"]
        fillings = filling["form"]
        description = ""
        filling_date = filling["filedDate"].split()[0]
        report_url = filling["reportUrl"]
        filing_url = filling["filingUrl"]
        cur.execute("INSERT INTO sec_fillings VALUES (%s, %s, %s, %s, %s, %s)",
                    (ticker, fillings, description, filling_date, report_url, filing_url))
        cnx.commit()
    df = pd.DataFrame(sec_list)
    df.rename(columns={"form": "Filling", "filedDate": "Filling Date"},
              inplace=True)
    df["Description"] = ""
    df = df[["Filling", "Description", "Filling Date", "reportUrl", "filingUrl"]]
    return df


def get_ticker_news(ticker_selected):
    """
    Get news article of ticker selected and find the news sentiment of the news title
    """
    try:
        ticker_fin = finvizfinance(ticker_selected)
        news_df = ticker_fin.ticker_news()
        news_df = news_df.drop_duplicates(subset=['Title'])
        news_df["Date"] = news_df["Date"].dt.date
        news_df["Date"] = news_df["Date"].astype(str)

        # Get sentiment of each news title and add it to a new column in news_df
        sentiment_list = list()
        for index, row in news_df.iterrows():
            vs = analyzer.polarity_scores(row["Title"])
            sentiment_score = vs['compound']
            if sentiment_score > 0.2:
                sentiment = "Bullish"
            elif sentiment_score < -0.2:
                sentiment = "Bearish"
            else:
                sentiment = "Neutral"
            sentiment_list.append(sentiment)
            cur.execute("INSERT INTO daily_ticker_news VALUES (%s, %s, %s, %s, %s)",
                        (ticker_selected, row[0], row[1], row[2], sentiment))
            cnx.commit()
        news_df["Sentiment"] = sentiment_list
    except:
        news_df = pd.DataFrame(columns=["Date", "Title", "Link", "Sentiment"])
        news_df.loc[0] = ["N/A", "N/A", "https://finance.yahoo.com/news/", "N/A"]
        cur.execute("INSERT INTO daily_ticker_news VALUES (%s, %s, %s, %s, %s)",
                    (ticker_selected, "N/A", "N/A", "https://finance.yahoo.com/news/", "N/A"))
        cnx.commit()
    return news_df


def get_insider_trading(ticker_selected):
    """
    Get insider trading of ticker selected
    """
    try:
        ticker_fin = finvizfinance(ticker_selected)
        inside_trader_df = ticker_fin.ticker_inside_trader()
        inside_trader_df["Insider Trading"] = inside_trader_df["Insider Trading"].str.title()
        inside_trader_df.rename(columns={"Insider Trading": "Name", "SEC Form 4 Link": ""}, inplace=True)
        inside_trader_df["Date"] = inside_trader_df["Date"] + " {}".format(str(date.today().year))
        inside_trader_df["Date"] = pd.to_datetime(inside_trader_df["Date"], format="%b %d %Y")
        del inside_trader_df["Insider_id"]
        del inside_trader_df["SEC Form 4"]
        last_date = datetime.utcnow().date()
        for index, row in inside_trader_df.iterrows():
            if row[2] > last_date:
                x = row[2] - timedelta(days=365)
            else:
                x = row[2]
            date_to_insert = str(x).split()[0]
            last_date = x
            cur.execute("INSERT INTO insider_trading VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (ticker_selected, row[0], row[1], date_to_insert, row[3], row[4],
                         row[5], row[6], row[7], row[8]))
            cnx.commit()
    except:
        inside_trader_df = pd.DataFrame(columns=["Name", "Relationship", "Date", "Transaction", "Cost", "Shares",
                                                 "Value ($)", "#Shares Total", ""])
        inside_trader_df.loc[0] = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    return inside_trader_df


def government_daily_trades(df, date_selected, col_name):
    if not date_selected:
        date_selected = df["Disclosure Date"].iloc[0]
    latest_df = df[df["Disclosure Date"] == date_selected]
    group_by_govt_official = pd.DataFrame(df.groupby([col_name]).agg({"Transaction Date": "count",
                                                                      "Disclosure Date": lambda x: x.iloc[0]}))
    group_by_govt_official.sort_values(by=["Disclosure Date"], ascending=False, inplace=True)
    group_by_govt_official.rename(columns={"Transaction Date": "Total",
                                           "Disclosure Date": "Last Disclosure"}, inplace=True)
    group_by_govt_official.reset_index(inplace=True)

    group_by_ticker = pd.DataFrame(df["Ticker"].value_counts())
    group_by_ticker.reset_index(inplace=True)
    group_by_ticker.columns = ["Ticker", "Count"]
    group_by_ticker = group_by_ticker[group_by_ticker["Ticker"] != "Unknown"]
    return date_selected, latest_df, group_by_govt_official, group_by_ticker


def long_number_format(num):
    """
    Convert long number to short form (e.g: 1000000 to 1M)
    """
    if isinstance(num, float):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        num_str = int(num) if num.is_integer() else f"{num:.3f}"
        return f"{num_str}{' KMBTP'[magnitude]}".strip()
    if isinstance(num, int):
        num = str(num)
    if num is not None and num.lstrip("-").isdigit():
        num = int(num)
        num /= 1.0
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        num_str = int(num) if num.is_integer() else f"{num:.3f}"
        return f"{num_str}{' KMBTP'[magnitude]}".strip()
    return num


def download_file(df, file_name):
    """
    Allow users to download data as CSV
    """
    df.to_csv(file_name, index=False)
    with open(file_name) as to_download:
        response = HttpResponse(to_download, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        if os.path.isfile(file_name):
            os.remove(file_name)
        return response


def linear_regression(x, y):
    """
    Linear Regression model without sklearn library
    Parameters
    ----------
        x: list of x axis
        y: list of y axis
    """
    # calculate mean of x & y using an inbuilt numpy method mean()
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    m = len(y)

    # using the formula to calculate m & c
    numer = 0
    denom = 0
    for i in range(m):
        numer += (x[i] - mean_x) * (y[i] - mean_y)
        denom += (x[i] - mean_x) ** 2
    if denom == 0:
        denom = 1
    m = numer / denom
    return m
