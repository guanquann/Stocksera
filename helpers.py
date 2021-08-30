import sqlite3
import numpy as np
import os
from django.http import HttpResponse
from fast_yahoo import *

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

# Time Format: HHMMSS
market_open_time = "080000"  # 133000
market_close_time = "200000"


def default_ticker(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper().replace(" ", "")
    else:
        ticker_selected = "AAPL"
    return ticker_selected


def check_img(ticker_selected, information):
    if ticker_selected == "TSLA":
        return "https://logo.clearbit.com/tesla.cn"
    elif ticker_selected == "BABA":
        return "https://logo.clearbit.com/alibaba.com"
    elif ticker_selected == "MRNA":
        return "https://g.foolcdn.com/art/companylogos/mark/mrna.png"
    else:
        return information["logo_url"]


def get_all_tickers():
    all_ticker_list = pd.read_csv(r"database/all_tickers.csv")
    symbol_list = all_ticker_list["SYMBOL"].to_list()
    description = all_ticker_list["DESCRIPTION"].to_list()
    return symbol_list, description


def check_market_hours(ticker_selected):
    """
    Cache ticker information into a json file to speed up rendering time
    Criteria for update:
        1. When market is open (data is updated every 15 minutes to prevent excessive API call)
        2. When a new ticker is mentioned
    Parameters
    ----------
    ticker_selected: str
        ticker symbol (e.g: AAPL)
    """
    current_datetime = datetime.utcnow()

    next_update_time = str(current_datetime + timedelta(seconds=600))
    with open(r"database/yf_cached_api.json", "r+") as r:
        data = json.load(r)
        if ticker_selected in data and str(current_datetime) < data[ticker_selected]["next_update"]:
            information = data[ticker_selected]
            print("Market Open. Using cached data")
        else:
            information = download_advanced_stats([ticker_selected])
            data.update(information)
            information = data[ticker_selected]

            information["next_update"] = next_update_time
            r.seek(0)
            r.truncate()
            json.dump(data, r, indent=4)
            print("Market Open. Scraping data", type(information))

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        # db.execute("SELECT * FROM stocksera_trending WHERE symbol=?", (ticker_selected,))
        # count = db.fetchone()
        # if count is None:
        #     count = 1
        # else:
        #     count = count[2] + 1
        #
        # db.execute("DELETE from stocksera_trending WHERE symbol=?", (ticker_selected,))
        #
        # db.execute("INSERT INTO stocksera_trending (symbol, name, count) VALUES (?, ?, ?) ",
        #            (ticker_selected, information["longName"], count))
        db.execute("INSERT INTO stocksera_trending (symbol, name, count) VALUES (?, ?, 1) ON CONFLICT (symbol) "
                   "DO UPDATE SET count=count+1", (ticker_selected, information["longName"]))
        # db.execute("UPDATE stocksera_trending SET next_update=?", (next_update_time, ))
        conn.commit()

    return information


def check_financial_data(ticker_selected, ticker, data, r):
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


def long_number_format(num):
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
    m = numer / denom
    return m
