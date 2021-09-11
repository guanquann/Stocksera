import os
import sqlite3
import numpy as np
import finnhub
from django.http import HttpResponse
from finvizfinance.quote import finvizfinance
from json.decoder import JSONDecodeError
from fast_yahoo import *
from custom_extensions.custom_words import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

# https://finnhub.io/
finnhub_client = finnhub.Client(api_key="API_KEY_HERE")

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

# Time Format in UTC: HHMMSS.
market_open_time = "080000"
market_close_time = "200000"

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                        "50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}


def default_ticker(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper().replace(" ", "")
    else:
        ticker_selected = "AAPL"
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
            print("Using cached data for {}".format(ticker_selected))
        else:
            information = download_advanced_stats([ticker_selected])
            data.update(information)
            information = data[ticker_selected]

            information["next_update"] = next_update_time
            r.seek(0)
            r.truncate()
            json.dump(data, r, indent=4)
            print("Scraping data for {}".format(ticker_selected))

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        # Uncomment this if the bottom does not work!
        # db.execute("SELECT * FROM stocksera_trending WHERE symbol=?", (ticker_selected,))
        # count = db.fetchone()
        # if count is None:
        #     count = 1
        # else:
        #     count = count[2] + 1
        #
        # db.execute("DELETE from stocksera_trending WHERE symbol=?", (ticker_selected,))
        # db.execute("INSERT INTO stocksera_trending (symbol, name, count) VALUES (?, ?, ?) ",
        #            (ticker_selected, information["longName"], count))

        # Comment this if you face an error. Uncomment the top instead.
        db.execute("INSERT INTO stocksera_trending (symbol, name, count) VALUES (?, ?, 1) ON CONFLICT (symbol) "
                   "DO UPDATE SET count=count+1", (ticker_selected, information["longName"]))
        conn.commit()

        db.execute("SELECT * FROM related_tickers WHERE ticker=?", (ticker_selected, ))
        related_tickers = db.fetchall()
        if not related_tickers:
            related_tickers = finnhub_client.company_peers(ticker_selected)
            if ticker_selected in related_tickers:
                related_tickers.remove(ticker_selected)
            upload_to_db = related_tickers.copy()
            while len(upload_to_db) <= 8:
                upload_to_db += [""]
            db.execute("INSERT INTO related_tickers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       tuple([ticker_selected] + upload_to_db[:8]))
            conn.commit()
        else:
            related_tickers = list(related_tickers[0])[1:]
            related_tickers = [i for i in related_tickers if i != ""]
        if not related_tickers:
            related_tickers = ["AAPL"]
    else:
        related_tickers = []
    return information, related_tickers


def check_financial_data(ticker_selected, ticker, data, r):
    """
    Get financial data of ticker selected and save to json file
    """
    print("Getting financial data for {}".format(ticker_selected))
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


def get_loss_at_strike(strike, chain):
    """
    Function to get the loss at the given expiry
    Parameters
    ----------
    strike: Union[int,float]
        Value to calculate total loss at
    chain: Dataframe:
        Dataframe containing at least strike and openInterest
    Returns
    -------
    loss: Union[float,int]
        Total loss
    """

    itm_calls = chain[chain.index < strike][["OI Calls"]]
    itm_calls["loss"] = (strike - itm_calls.index) * itm_calls["OI Calls"]
    call_loss = round(itm_calls["loss"].sum() / 10000, 2)

    # The *-1 below is due to a sign change for plotting in the _view code
    itm_puts = chain[chain.index > strike][["OI Puts"]]
    itm_puts["loss"] = (itm_puts.index - strike) * itm_puts["OI Puts"] * -1
    put_loss = round(itm_puts.loss.sum() / 10000, 2)
    loss = call_loss + put_loss
    return loss, call_loss, put_loss


def get_max_pain(chain):
    """
    Returns the max pain for a given call/put dataframe
    Parameters
    ----------
    chain: DataFrame
        Dataframe to calculate value from
    Returns
    -------
    max_pain :
        Max pain value
    call_loss_list:
        Total money value of the call options at the particular strike
    put_loss_list:
        Total money value of the put options at the particular strike
    """
    strikes = np.array(chain.index)
    if ("OI Calls" not in chain.columns) or ("OI Puts" not in chain.columns):
        print("Incorrect columns.  Unable to parse max pain")
        return np.nan
    loss_list, call_loss_list, put_loss_list = [], [], []
    for price_at_exp in strikes:
        net_loss, call_loss, put_loss = get_loss_at_strike(price_at_exp, chain)
        loss_list.append(net_loss)
        call_loss_list.append(call_loss)
        put_loss_list.append(put_loss)
    chain["loss"] = loss_list
    max_pain = chain["loss"].idxmin()
    return max_pain, call_loss_list, put_loss_list


def get_sec_fillings(ticker_selected):
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&action=getcompany&count=100'.format(ticker_selected)
    r = requests.get(url, headers=header)

    df = pd.read_html(r.text)[-1]
    if "Format" in df.columns:
        del df["Format"]
        del df["File/Film Number"]
        df["Link"] = df["Description"].apply(lambda k: k.split("Acc-no: ")[-1].split("Size")[0])
        df["Link"] = df["Link"].apply(
            lambda l: "https://www.sec.gov/Archives/edgar/data/{}/{}/{}-index.htm".format(ticker_selected,
                                                                                          l.replace("-", ""), l))
        df["Description"] = df["Description"].apply(lambda x: x.split("Acc-no: ")[0])
    else:
        df = pd.DataFrame(columns=["Fillings", "Description", "Filling Date", "Link"])
        df.loc[0] = ["N/A", "N/A", "N/A", "https://www.sec.gov/Archives/edgar/data/{}".format(ticker_selected)]
    return df


def get_ticker_news(ticker_selected):
    """
    Get news article of ticker selected and find the news sentiment of the news title
    """
    try:
        ticker_fin = finvizfinance(ticker_selected)
        news_df = ticker_fin.TickerNews()
        news_df = news_df.drop_duplicates(subset=['Title'])
        news_df["Date"] = news_df["Date"].dt.date

        # Get sentiment of each news title and add it to a new column in news_df
        sentiment_list = list()
        for index, row in news_df.iterrows():
            vs = analyzer.polarity_scores(row["Title"])
            sentiment_score = vs['compound']
            if sentiment_score > 0.25:
                sentiment = "Bullish"
            elif sentiment_score < -0.25:
                sentiment = "Bearish"
            else:
                sentiment = "Neutral"
            sentiment_list.append(sentiment)
            db.execute("INSERT INTO daily_ticker_news VALUES (?, ?, ?, ?, ?)",
                       (ticker_selected, row[0], row[1], row[2], sentiment))
            conn.commit()
        news_df["Sentiment"] = sentiment_list
    except:
        news_df = pd.DataFrame(columns=["Date", "Title", "Link", "Sentiment"])
        news_df.loc[0] = ["N/A", "N/A", "https://finance.yahoo.com/news/", "N/A"]
        db.execute("INSERT INTO daily_ticker_news VALUES (?, ?, ?, ?, ?)",
                   (ticker_selected, "N/A", "N/A", "https://finance.yahoo.com/news/", "N/A"))
        conn.commit()
    return news_df


def get_insider_trading(ticker_selected):
    """
    Get insider trading of ticker selected
    """
    try:
        ticker_fin = finvizfinance(ticker_selected)
        inside_trader_df = ticker_fin.TickerInsideTrader()
        inside_trader_df["Insider Trading"] = inside_trader_df["Insider Trading"].str.title()
        inside_trader_df.rename(columns={"Insider Trading": "Name"}, inplace=True)
        del inside_trader_df["Insider_id"]
        del inside_trader_df["SEC Form 4"]
    except:
        inside_trader_df = pd.DataFrame(columns=["Name", "Relationship", "Date", "Transaction", "Cost", "Shares", "Value ($)", "#Shares Total"])
        inside_trader_df.loc[0] = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    return inside_trader_df


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
