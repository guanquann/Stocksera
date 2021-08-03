import yfinance.ticker as yf
import numpy as np
import json
from datetime import datetime, timedelta

# Time Format: HHMMSS
market_open_time = "133000"
market_close_time = "200000"


def default_ticker(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()
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


def check_market_hours(ticker, ticker_selected):
    """
    Cache ticker information into a json file to speed up rendering time
    Criteria for update:
        1. When market is open (data is updated every 15 minutes to prevent excessive API call)
        2. When a new ticker is mentioned
    Parameters
    ----------
    ticker:
    ticker_selected: str
        ticker symbol (e.g: AAPL)
    """
    current_datetime = datetime.utcnow()

    next_update_time = str(current_datetime + timedelta(seconds=600))
    current_utc_date = str(current_datetime).split()[0]

    current_utc_time = str(current_datetime).split()[1].split(".")[0].replace(":", "")

    # If market is closed
    if current_utc_time > market_close_time or current_utc_time < market_open_time or current_datetime.today().weekday() >= 5:
        with open(r"database/yf_cached_api.json", "r+") as r:
            data = json.load(r)
            if ticker_selected in data:
                # Last updated time is before market close and after open, update information
                last_updated_date = data[ticker_selected]["next_update"].split()[0]
                last_updated_time = data[ticker_selected]["next_update"].split()[1].split(".")[0].replace(":", "")
                # print(last_updated_date, current_utc_date, last_updated_time)
                if (market_close_time > last_updated_time > market_open_time) or last_updated_date != current_utc_date:
                    information = ticker.info
                    information["logo_url"] = check_img(ticker_selected, information)
                    data[ticker_selected] = information
                    data[ticker_selected]["next_update"] = next_update_time
                    r.seek(0)
                    r.truncate()
                    json.dump(data, r, indent=4)
                    print("Market Close. Updating data")
                else:
                    information = data[ticker_selected]
                    print("Market Close. Using cached data")
            else:
                information = ticker.info
                information["logo_url"] = check_img(ticker_selected, information)
                data[ticker_selected] = information
                data[ticker_selected]["next_update"] = next_update_time
                r.seek(0)
                r.truncate()
                json.dump(data, r, indent=4)
                print("Market Close. Scraping data")
    # If market is opened
    else:
        with open(r"database/yf_cached_api.json", "r+") as r:
            data = json.load(r)
            if ticker_selected in data and str(current_datetime) < data[ticker_selected]["next_update"]:
                information = data[ticker_selected]
                print("Market Open. Using cached data")
            else:
                information = ticker.info
                information["logo_url"] = check_img(ticker_selected, information)
                data[ticker_selected] = information
                data[ticker_selected]["next_update"] = next_update_time
                r.seek(0)
                r.truncate()
                json.dump(data, r, indent=4)
                print("Market Open. Scraping data")
    return information


def ticker_bar():
    """
    Custom ticker bar in HTML page. I did not use this anymore, since I replaced it with the ticker bar provided by Trading View
    """
    popular_ticker_list = ["SPY", "QQQ", "DIA", "AAPL", "GME", "AMC", "TSLA", "NIO", "PLTR", "NVDA"]
    popular_name_list = ["S&P500 ETF", "NASDAQ-100", "Dow ETF", "Apple", "GameStop", "AMC", "Tesla", "Nio",
                         "Palantir", "NVIDIA"]

    price_list = list()
    for ticker in popular_ticker_list:
    
        ticker = yf.Ticker(ticker)
        price_df = ticker.history(period="3d")['Close']
        opening_price = float(price_df.iloc[1])
        closing_price = float(price_df.iloc[2])
        price_change = round(closing_price - opening_price, 2)

        percentage_change = round(((price_change / opening_price) * 100), 2)
        if percentage_change >= 0:
            price_change = '+' + str(price_change)
            percentage_change = '+' + str(percentage_change)

        price_list.append([round(closing_price, 2), price_change, percentage_change])
    return popular_ticker_list, popular_name_list, price_list


def check_financial_data(ticker_selected, ticker, data, r):
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
