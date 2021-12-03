from custom_extensions.stopwords import *
from scheduled_tasks.reddit.get_subreddit_count import *
from email_server import *
from fast_yahoo_options import *

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

option_market_open_time = "110000"    # 9.30PM - 2H30MIN = 7PM   133000
option_market_close_time = "030000"   # 4.15AM + 6H45MIN = 11AM   201500


def main(request):
    db.execute("SELECT * FROM stocksera_trending ORDER BY count DESC LIMIT 10")
    trending = db.fetchall()
    trending = list(map(list, trending))
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
    db.execute("SELECT * FROM sec_fillings WHERE ticker=?", (ticker_selected, ))
    sec = db.fetchall()
    if not sec:
        get_sec_fillings(ticker_selected)
    df = pd.read_sql_query("SELECT * FROM sec_fillings WHERE ticker='{}' ".format(ticker_selected), conn)
    del df["ticker"]
    df.rename(columns={"filling": "Filling", "description": "Description", "filling_date": "Filling Date"},
              inplace=True)
    df = df.to_html(index=False)
    return render(request, 'stock/sec_fillings.html', {"sec_fillings_df": df})


def news_sentiment(request):
    """
    Show news and sentiment of ticker in /ticker?quote={TICKER}. Data from Finviz
    Note: News are only available if hosted locally. Read README.md for more details
    """
    ticker_selected = default_ticker(request)
    db.execute("SELECT * FROM daily_ticker_news WHERE ticker=?", (ticker_selected,))
    news = db.fetchall()
    if not news:
        news_df = get_ticker_news(ticker_selected)
    else:
        news_df = pd.read_sql_query("SELECT * FROM daily_ticker_news WHERE ticker='{}' ".format(ticker_selected), conn)
        del news_df["Ticker"]
    news_df = news_df.to_html(index=False)
    return render(request, 'stock/recent_news.html', {"title": "News", "recent_news_df": news_df})


def insider_trading(request):
    """
    Get a specific ticker's insider trading data from Finviz
    """
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(request)
    db.execute("SELECT * FROM insider_trading WHERE Ticker=?", (ticker_selected,))
    transactions = db.fetchall()
    if not transactions:
        inside_trader_df = get_insider_trading(ticker_selected)
    else:
        inside_trader_df = pd.read_sql_query("SELECT * FROM insider_trading WHERE Ticker='{}' ".format(ticker_selected), conn)
        del inside_trader_df["Ticker"]
        inside_trader_df.rename(columns={"TransactionDate": "Date",
                                         "TransactionType": "Transaction",
                                         "Value": "Value ($)",
                                         "SharesLeft": "#Shares Total",
                                         "URL": ""}, inplace=True)
    inside_trader_df = inside_trader_df.to_html(index=False)
    return render(request, 'stock/insider_trading.html', {"inside_trader_df": inside_trader_df})


def latest_insider(request):
    """
    Get latest insider trading data from Finviz and perform analysis
    """
    pd.options.display.float_format = '{:.2f}'.format

    recent_activity = pd.read_sql_query("SELECT * FROM latest_insider_trading ORDER BY DateFilled DESC LIMIT 2000", conn)
    recent_activity.rename(columns={"TransactionDate": "Date",
                                    "TransactionType": "Transaction",
                                    "Value": "Value ($)",
                                    "SharesLeft": "#Shares Total",
                                    "URL": ""}, inplace=True)

    insider_analysis = pd.read_sql_query("SELECT * FROM latest_insider_trading_analysis", conn)
    insider_analysis.rename(columns={"MktCap": "Market Cap", "Proportion": "% of Mkt Cap"}, inplace=True)

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
    trends.build_payload(kw_list=[ticker_selected], timeframe=timeframe)  #  cat=7
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


# def options(request):
#     """
#     Get options (Max pain, option chain, C/P ratio) of ticker.
#     """
#     pd.options.display.float_format = '{:.1f}'.format
#     ticker_selected = default_ticker(request)
#
#     information, related_tickers = check_market_hours(ticker_selected)
#     if "longName" in information and information["regularMarketPrice"] != "N/A":
#         # with open(r"database/yf_cached_options.json", "r+") as r:
#         #     # Update date if
#         #     #   1. Weekday
#         #     #   2. Current datetime > next update time
#         #     #   3. Market is open
#         #     current_datetime = datetime.utcnow()
#         #     current_str_time = str(current_datetime).split()[1].replace(":", "").split(".")[0]
#         #
#         #     data = check_json(r)
#         #     if ticker_selected in data:
#         #         print("{} in option data. Looking for correct date now...".format(ticker_selected))
#         #         options_info = data[ticker_selected]
#         #     else:
#         #         # weekday, option mkt open and current time is in range and ticker not in db
#         #         # if current_datetime.weekday() < 5 and option_market_open_time <= current_str_time <= \
#         #         #         option_market_close_time:
#         #         if current_datetime.weekday() < 5 and (option_market_open_time <= current_str_time <= "235959"
#         #                                                or current_str_time < option_market_close_time):
#         #             print("No option data for {} & mkt open. Scraping data now".format(ticker_selected))
#         #             options_info = save_options_to_json([ticker_selected])[ticker_selected]
#         #         # weekend ... ticker not in db, mkt close
#         #         else:
#         #             print("No option data for {} and its the weekend. Scraping data now.".format(ticker_selected))
#         #             options_info = save_options_to_json([ticker_selected])[ticker_selected]
#         #
#         #     options_dates = options_info["ExpirationDate"]
#         #     if request.GET.get("date") not in ["", None] and options_dates != []:
#         #         date_selected = request.GET["date"]
#         #     elif not options_dates:
#         #         return render(request, 'options.html', {"ticker_selected": ticker_selected,
#         #                                                 "error": "error_true",
#         #                                                 "error_msg": "There is no options data for {}.".
#         #                       format(ticker_selected)})
#         #     else:
#         #         date_selected = options_dates[0]
#         #
#         #     if date_selected in options_info["CurrentDate"]:
#         #         options_info = options_info["CurrentDate"][date_selected]
#         #         if str(current_datetime) > options_info["NextUpdate"] and \
#         #                 current_datetime.weekday() < 5 and \
#         #                 (option_market_open_time <= current_str_time <= "235959"
#         #                  or current_str_time < option_market_close_time):
#         #             print("Ticker {} present, same date but outdated".format(ticker_selected))
#         #             options_info = save_options_to_json([ticker_selected], int(datetime.timestamp(
#         #                 datetime.strptime(date_selected, "%Y-%m-%d") + timedelta(seconds=60*60*8))))[
#         #                 ticker_selected]["CurrentDate"][date_selected]
#         #         else:
#         #             print("Ticker {} present, same date and not outdated".format(ticker_selected))
#         #
#         #     else:
#         #         # if (current_datetime.weekday() < 5 and option_market_open_time <= current_str_time <=
#         #         #         option_market_close_time) or current_datetime.weekday() >= 5:
#         #         if (current_datetime.weekday() < 5 and
#         #             (option_market_open_time <= current_str_time <= "235959" or
#         #              current_str_time < option_market_close_time)) or \
#         #                 current_datetime.weekday() >= 5:
#         #             print("Ticker {} present, but not same date".format(ticker_selected))
#         #             options_info = save_options_to_json([ticker_selected], int(datetime.timestamp(datetime.strptime(date_selected, "%Y-%m-%d") + timedelta(seconds=60*60*8))))[ticker_selected]["CurrentDate"][date_selected]
#         #         else:
#         #             return render(request, 'options.html', {"ticker_selected": ticker_selected,
#         #                                                     "error": "error_true",
#         #                                                     "error_msg": "The market is closed & options data for {} "
#         #                                                                  "on {} is currently unavailable. "
#         #                                                                  "Please come back nearing market open!".
#         #                           format(ticker_selected, date_selected)})
#         #     max_pain = options_info["MaxPain"]
#         #     call_loss_list = options_info["CallLoss"]
#         #     put_loss_list = options_info["PutLoss"]
#         #
#         # op_put = options_info["OptionChainPut"]
#         # put_df = pd.DataFrame(op_put, columns=["Strike", "Volume", "OI"])
#         #
#         # op_call = options_info["OptionChainCall"]
#         # call_df = pd.DataFrame(op_call, columns=["Strike", "Volume", "OI"])
#         #
#         # df_merge = pd.merge(call_df, put_df, on="Strike", how="outer")
#         # df_merge.sort_values(by=["Strike"], inplace=True)
#         # df_merge["Strike"] = df_merge["Strike"].apply(lambda x: "$" + str(x))
#         # df_merge = df_merge[["OI_x", "Volume_x", "Strike", "OI_y", "Volume_y"]]
#         # df_merge.columns = ["OI", "Volume", "", "OI", "Volume"]
#         # df_merge.replace(np.nan, 0, inplace=True)
#         # df_merge["OI"] = df_merge["OI"].astype(int)
#         # df_merge["Volume"] = df_merge["Volume"].astype(int)
#
#         k = requests.get(f"https://www.optionsprofitcalculator.com/ajax/getOptions?stock={ticker_selected}&reqId=1").json()
#         if "options" not in k:
#             render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
#                                              "error": "error_true",
#                                              "error_msg": "There is no options data for {}.".
#                    format(ticker_selected)})
#         options_dates = list(k["options"].keys())
#         if request.GET.get("date") not in ["", None] and options_dates != []:
#             date_selected = request.GET["date"]
#         else:
#             date_selected = options_dates[0]
#         chain_selected = k["options"][date_selected]
#         calls_df = pd.DataFrame.from_dict(chain_selected['c'], orient="index", dtype=float)
#
#         puts_df = pd.DataFrame.from_dict(chain_selected['p'], orient="index", dtype=float)
#
#         df_merge = pd.merge(calls_df, puts_df, left_index=True, right_index=True)
#         df_merge = df_merge[['oi_x', 'l_x', 'b_x', 'a_x', 'v_x', 'oi_y', 'l_y', 'b_y', 'a_y', 'v_y']]
#         df_merge.index = df_merge.index.map(float)
#
#         max_pain, call_loss_list, put_loss_list = get_max_pain(df_merge[["oi_x", "oi_y"]])
#
#         df_merge.reset_index(inplace=True)
#         print(df_merge)
#         df_merge = df_merge[["oi_x", "v_x", "index", "oi_y", "v_y"]]
#         df_merge.columns = ["OI", "Volume", "", "OI", "Volume"]
#         df_merge.replace(np.nan, 0, inplace=True)
#         df_merge[""] = df_merge[""].apply(lambda x: "$" + str(x))
#         df_merge["OI"] = df_merge["OI"].astype(int)
#         df_merge["Volume"] = df_merge["Volume"].astype(int)
#
#         return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
#                                                 "information": information,
#                                                 "related_tickers": related_tickers,
#                                                 "options_dates": options_dates,
#                                                 "date_selected": date_selected,
#                                                 "max_pain": max_pain,
#                                                 "call_loss_list": call_loss_list,
#                                                 "put_loss_list": put_loss_list,
#                                                 "merge": df_merge.to_html(index=False)
#                                                 })
#     else:
#         return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
#                                                 "error": "error_true",
#                                                 "error_msg": "There is no ticker named {} found! "
#                                                              "Please enter a ticker symbol (TSLA) "
#                                                              "instead of the name (Tesla).".format(ticker_selected)})

def options(request):
    """
    Get options (Max pain, option chain, C/P ratio) of ticker.
    """
    pd.options.display.float_format = '{:.1f}'.format
    ticker_selected = default_ticker(request)

    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        with open(r"database/yf_cached_options.json", "r+") as r:
            # Update date if
            #   1. Weekday
            #   2. Current datetime > next update time
            #   3. Market is open
            current_datetime = datetime.utcnow()
            current_str_time = str(current_datetime).split()[1].replace(":", "").split(".")[0]

            data = check_json(r)
            print("DATA SUCCESSFUL")
            if ticker_selected in data:
                print("{} in option data. Looking for correct date now...".format(ticker_selected))
                options_info = data[ticker_selected]
            else:
                # weekday, option mkt open and current time is in range and ticker not in db
                # if current_datetime.weekday() < 5 and option_market_open_time <= current_str_time <= \
                #         option_market_close_time:
                if current_datetime.weekday() < 5 and (option_market_open_time <= current_str_time <= "235959"
                                                       or current_str_time < option_market_close_time):
                    print("No option data for {} & mkt open. Scraping data now".format(ticker_selected))
                    options_info = save_options_to_json([ticker_selected], data=data, r=r)[ticker_selected]
                # weekend ... ticker not in db
                elif current_datetime.weekday() >= 5:
                    print("No option data for {} and its the weekend. Scraping data now.".format(ticker_selected))
                    options_info = save_options_to_json([ticker_selected], data=data, r=r)[ticker_selected]

                # weekday and current time out of range (bug in YF) and ticker not in db
                else:
                    return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                                  "error": "error_true",
                                                                  "error_msg": "The market is closed & options data for"
                                                                               " {} is currently unavailable. "
                                                                               "Please come back nearing market open!".
                                  format(ticker_selected)})

            options_dates = options_info["ExpirationDate"]
            if request.GET.get("date") not in ["", None] and options_dates != []:
                date_selected = request.GET["date"]
            elif not options_dates:
                return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                              "error": "error_true",
                                                              "error_msg": "There is no options data for {}.".
                              format(ticker_selected)})
            else:
                date_selected = options_dates[0]

            if date_selected in options_info["CurrentDate"]:
                options_info = options_info["CurrentDate"][date_selected]
                if str(current_datetime) > options_info["NextUpdate"] and \
                        current_datetime.weekday() < 5 and \
                        (option_market_open_time <= current_str_time <= "235959"
                         or current_str_time < option_market_close_time):
                    print("Ticker {} present, same date but outdated".format(ticker_selected))
                    options_info = save_options_to_json([ticker_selected], int(datetime.timestamp(
                        datetime.strptime(date_selected, "%Y-%m-%d") + timedelta(seconds=60*60*8))), data=data, r=r)[
                        ticker_selected]["CurrentDate"][date_selected]
                else:
                    print("Ticker {} present, same date and not outdated".format(ticker_selected))

            else:
                # if (current_datetime.weekday() < 5 and option_market_open_time <= current_str_time <=
                #         option_market_close_time) or current_datetime.weekday() >= 5:
                if (current_datetime.weekday() < 5 and
                    (option_market_open_time <= current_str_time <= "235959" or
                     current_str_time < option_market_close_time)) or \
                        current_datetime.weekday() >= 5:
                    print("Ticker {} present, but not same date".format(ticker_selected))
                    options_info = save_options_to_json([ticker_selected], int(datetime.timestamp(datetime.strptime(date_selected, "%Y-%m-%d") + timedelta(seconds=60*60*8))), data=data, r=r)[ticker_selected]["CurrentDate"][date_selected]
                else:
                    return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                                  "error": "error_true",
                                                                  "error_msg": "The market is closed & options data "
                                                                               "for {} on {} is currently unavailable. "
                                                                               "Please come back nearing market open!".
                                  format(ticker_selected, date_selected)})
            max_pain = options_info["MaxPain"]
            call_loss_list = options_info["CallLoss"]
            put_loss_list = options_info["PutLoss"]

        op_put = options_info["OptionChainPut"]
        put_df = pd.DataFrame(op_put, columns=["Strike", "Volume", "OI"])

        op_call = options_info["OptionChainCall"]
        call_df = pd.DataFrame(op_call, columns=["Strike", "Volume", "OI"])

        df_merge = pd.merge(call_df, put_df, on="Strike", how="outer")
        df_merge.sort_values(by=["Strike"], inplace=True)
        df_merge["Strike"] = df_merge["Strike"].apply(lambda x: "$" + str(x))
        df_merge = df_merge[["OI_x", "Volume_x", "Strike", "OI_y", "Volume_y"]]
        df_merge.columns = ["OI", "Volume", "", "OI", "Volume"]
        df_merge.replace(np.nan, 0, inplace=True)
        df_merge["OI"] = df_merge["OI"].astype(int)
        df_merge["Volume"] = df_merge["Volume"].astype(int)

        return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
                                                      "information": information,
                                                      "related_tickers": related_tickers,
                                                      "options_dates": options_dates,
                                                      "date_selected": date_selected,
                                                      "max_pain": max_pain,
                                                      "call_loss_list": call_loss_list,
                                                      "put_loss_list": put_loss_list,
                                                      "merge": df_merge.to_html(index=False)
                                                      })
    else:
        return render(request, 'stock/options.html', {"ticker_selected": ticker_selected,
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
        pd.options.display.float_format = '{:.2f}'.format
        highest_short_vol = pd.read_csv(r"database/highest_short_volume.csv")
        return render(request, 'stock/top_short_volume.html',
                      {"highest_short_vol": highest_short_vol.to_html(index=False)})

    information, related_tickers = check_market_hours(ticker_selected)

    if "longName" in information and information["regularMarketPrice"] != "N/A":
        pd.options.display.float_format = '{:.2f}'.format
        short_volume_data = pd.read_csv("database/short_volume.csv")
        short_volume_data = short_volume_data[short_volume_data["ticker"] == ticker_selected][::-1]
        history = pd.DataFrame(yf.Ticker(ticker_selected).history(interval="1d", period="1y")["Close"])
        history.reset_index(inplace=True)
        history["Date"] = history["Date"].astype(str)
        short_volume_data = pd.merge(short_volume_data, history, on=["Date"], how="left")

        if "download_csv" in request.GET:
            file_name = "{}_short_volume.csv".format(ticker_selected)
            short_volume_data.to_csv(file_name, index=False)
            response = download_file(short_volume_data, file_name)
            return response

        del short_volume_data["ticker"]

        short_volume_data.rename(columns={"reported_date": "Date", "short_vol": "Short Volume",
                                          "short_exempt_vol": "Short Exempt Vol", "total_vol": "Total Volume",
                                          "percent": "% Shorted", "close_price": "Close Price"}, inplace=True)

        highest_short_vol = pd.read_csv(r"database/highest_short_volume.csv")["Symbol"].tolist()[:20]

        return render(request, 'stock/short_volume.html', {"ticker_selected": ticker_selected,
                                                           "information": information,
                                                           "related_tickers": related_tickers,
                                                           "highest_short_vol": highest_short_vol,
                                                           "short_volume_data": short_volume_data.to_html(index=False)})
    else:
        return render(request, 'stock/short_volume.html', {"ticker_selected": ticker_selected,
                                                           "error": "error_true"})


def failure_to_deliver(request):
    """
    Get FTD of tickers. Data from SEC
    """
    ticker_selected = default_ticker(request)

    if ticker_selected == "TOP_FTD":
        top_ftd = pd.read_csv(r"database/failure_to_deliver/top_ftd.csv")
        top_ftd = top_ftd.replace(np.nan, "")
        return render(request, 'stock/top_ftd.html', {"top_ftd": top_ftd.to_html(index=False)})

    information, related_tickers = check_market_hours(ticker_selected)
    if "longName" in information and information["regularMarketPrice"] != "N/A":
        ftd = pd.read_csv(r"database/failure_to_deliver/ftd.csv")
        ftd = ftd[ftd["Symbol"] == ticker_selected]
        ftd = ftd[::-1]
        ftd["Amount (FTD x $)"] = (ftd["Failure to Deliver"].astype(int) * ftd["Price"].astype(float)).astype(int)
        del ftd["Symbol"]
        ftd = ftd[['Date', 'Failure to Deliver', 'Price', 'Amount (FTD x $)', 'T+35 Date']]

        if "download_csv" in request.GET:
            file_name = "{}_ftd.csv".format(ticker_selected)
            ftd.to_csv(file_name, index=False)
            response = download_file(ftd, file_name)
            return response

        return render(request, 'stock/ftd.html', {"ticker_selected": ticker_selected,
                                                  "information": information,
                                                  "related_tickers": related_tickers,
                                                  "90th_percentile": ftd["Amount (FTD x $)"].quantile(0.90),
                                                  "ftd": ftd.to_html(index=False)})
    else:
        return render(request, 'stock/ftd.html', {"ticker_selected": ticker_selected,
                                                  "error": "error_true"})


def earnings_calendar(request):
    """
    Get earnings for the upcoming week. Data from yahoo finance
    """
    db.execute("SELECT * FROM earnings_calendar ORDER BY earning_date ASC")
    calendar = db.fetchall()
    calendar = list(map(list, calendar))
    return render(request, 'market_summary/earnings_calendar.html', {"earnings_calendar": calendar})


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
        return render(request, 'reddit/cryptocurrency.html', {"date_selected": date_selected,
                                                              "all_dates": all_dates,
                                                              "trending_tickers": trending_tickers})

    database_mapping = {"wallstreetbets": "Wall Street Bets",
                        "stocks": "Stocks",
                        "shortsqueeze": "Shortsqueeze",
                        "options": "Options",
                        "spacs": "SPACs",
                        "pennystocks": "Pennystocks"}
    subreddit = database_mapping[subreddit]

    return render(request, 'reddit/reddit_sentiment.html', {"all_dates": all_dates,
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
    db.execute("SELECT * FROM reddit_etf WHERE status='Open' ORDER BY open_date DESC")
    open_trade = db.fetchall()

    db.execute("select sum(PnL) from reddit_etf WHERE status='Open'")
    unrealized_PnL = round(db.fetchone()[0], 2)

    db.execute("SELECT * FROM reddit_etf WHERE status='Close' ORDER BY close_date DESC")
    close_trade = db.fetchall()

    db.execute("select sum(PnL) from reddit_etf WHERE status='Close'")
    realized_PnL = round(db.fetchone()[0], 2)

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
        pd.options.display.float_format = '{:.2f}'.format
        stats = pd.read_sql_query("SELECT * FROM subreddit_count WHERE ticker='{}'".format(ticker_selected), conn)
        stats.rename(columns={"subscribers": "Redditors", "active": "Active", "updated_date": "Date",
                              "percentage_active": "% Active", "growth": "% Growth",
                              "percentage_price_change": "% Price Change"}, inplace=True)
        information, related_tickers = check_market_hours(ticker_selected)
        try:
            subreddit = stats.iloc[0][2]
            del stats["ticker"]
            del stats["subreddit"]
        except (TypeError, IndexError):
            subreddit = "N/A"
        return render(request, 'reddit/subreddit_count_individual.html', {"ticker_selected": ticker_selected,
                                                                          "information": information,
                                                                          "subreddit": subreddit,
                                                                          "stats": stats[::-1].to_html(index=False),
                                                                          "interested_subreddits": all_subreddits})
    else:
        db.execute("SELECT * FROM subreddit_count WHERE subreddit in ('wallstreetbets', 'stocks', "
                   " 'amcstock', 'Superstonk', 'options','pennystocks', 'cryptocurrency')")
        subscribers = db.fetchall()
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

    query = "SELECT ticker AS Ticker, SUM(mentions) AS Mentions, AVG(sentiment) AS Sentiment FROM wsb_trending_24H " \
            "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) DESC".format(date_threshold)

    mentions_df = pd.read_sql_query(query, conn)
    mentions_df.index += 1
    mentions_df.reset_index(inplace=True)
    mentions_df.rename(columns={"index": "Rank"}, inplace=True)

    # db.execute(query)
    # top_12 = db.fetchall()
    # trending_list = list()
    # for ticker in top_12[:12]:
    #     db.execute("SELECT ticker, date_updated, SUM(mentions) OVER (ROWS UNBOUNDED PRECEDING) FROM "
    #                "wsb_trending_24H WHERE ticker=? AND date_updated >= ?", (ticker[0], date_threshold))
    #     running_sum = db.fetchall()
    #     running_sum = list(map(list, running_sum))
    #     trending_list.append(running_sum)

    # Get word cloud
    db.execute("SELECT word, SUM(mentions) FROM wsb_word_cloud WHERE date_updated >= ? GROUP BY word ORDER BY "
               "SUM(mentions) DESC LIMIT 50", (date_threshold, ))
    wsb_word_cloud = db.fetchall()
    wsb_word_cloud = list(map(list, wsb_word_cloud))

    # Get trending tickers in the past 7 days
    date_threshold = str(datetime.utcnow() - timedelta(hours=24*7))

    mentions_7d_df = pd.read_sql_query("select ticker, sum(mentions)from wsb_trending_hourly where date_updated >= "
                          "'{}' GROUP BY ticker ORDER BY SUM(mentions) DESC LIMIT 30".format(date_threshold), conn)
    mentions_7d_df.reset_index(inplace=True)

    # query = "SELECT ticker AS Ticker, SUM(mentions) AS Mention, AVG(sentiment) AS Sentiment FROM wsb_trending_hourly " \
    #         "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) DESC LIMIT 12".format(date_threshold)
    # db.execute(query)
    # top_12 = db.fetchall()
    # trending_list_by_hour = list()
    # for ticker in top_12:
    #     db.execute("SELECT ticker, date_updated, SUM(mentions) OVER (ROWS UNBOUNDED PRECEDING) FROM "
    #                "wsb_trending_hourly WHERE ticker=? AND date_updated >= ?", (ticker[0], date_threshold))
    #     running_sum = db.fetchall()
    #     running_sum = list(map(list, running_sum))
    #     trending_list_by_hour.append(running_sum)

    # Get calls/puts mentions
    trending_options = pd.read_sql_query("SELECT ticker as Ticker, SUM(calls) AS Calls, SUM(puts) AS Puts, "
                                         "CAST(SUM(calls) AS float)/SUM(puts) as Ratio FROM wsb_trending_24H "
                                         "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(puts + calls) "
                                         "DESC LIMIT 30".format(date_threshold), conn)

    # Get change in mentions
    change_df = pd.read_sql_query("SELECT * FROM wsb_change", conn)

    # Get yahoo financial comparison
    wsb_yf = pd.read_sql_query("SELECT * FROM wsb_yf", conn)

    return render(request, 'reddit/wsb_live.html', {
                                                    # "trending_list": trending_list,
                                                    # "trending_list_by_hour": trending_list_by_hour,
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

    df = pd.read_sql_query("SELECT mentions, calls, puts, date_updated FROM wsb_trending_hourly WHERE "
                           "ticker='{}' ".format(ticker_selected), conn)

    sentiment_df = pd.read_sql_query("SELECT AVG(sentiment) as sentiment, strftime('%Y-%m-%d', date_updated) AS "
                                     "date_updated FROM wsb_trending_hourly WHERE ticker='{}' "
                                     "group by strftime('%Y-%m-%d', date_updated)".format(ticker_selected), conn)

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
        previous_calls = df[(df["date_updated"] >= last_14D) & (df["date_updated"] < last_7D)]["calls"].sum().astype(int)

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

    # Get trending tickers in the past 24H
    date_threshold = str(datetime.utcnow() - timedelta(hours=24))

    query = "SELECT ticker AS Ticker, SUM(mentions) AS Mentions, AVG(sentiment) AS Sentiment FROM crypto_trending_24H " \
            "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) DESC".format(date_threshold)

    mentions_df = pd.read_sql_query(query, conn)
    mentions_df.index += 1
    mentions_df.reset_index(inplace=True)
    mentions_df.rename(columns={"index": "Rank"}, inplace=True)

    db.execute(query)
    top_12 = db.fetchall()
    trending_list = list()
    for ticker in top_12[:12]:
        db.execute("SELECT ticker, date_updated, SUM(mentions) OVER (ROWS UNBOUNDED PRECEDING) FROM "
                   "crypto_trending_24H WHERE ticker=? AND date_updated >= ?", (ticker[0], date_threshold))
        running_sum = db.fetchall()
        running_sum = list(map(list, running_sum))
        trending_list.append(running_sum)

    # Get word cloud
    db.execute("SELECT word, SUM(mentions) FROM crypto_word_cloud WHERE date_updated >= ? GROUP BY word ORDER BY "
               "SUM(mentions) DESC LIMIT 50", (date_threshold, ))
    crypto_word_cloud = db.fetchall()
    crypto_word_cloud = list(map(list, crypto_word_cloud))

    # Get trending tickers in the past 7 days
    date_threshold = str(datetime.utcnow() - timedelta(hours=24*7))
    query = "SELECT ticker AS Ticker, SUM(mentions) AS Mention, AVG(sentiment) AS Sentiment FROM crypto_trending_hourly " \
            "WHERE date_updated >= '{}' GROUP BY ticker ORDER BY SUM(mentions) DESC LIMIT 12".format(date_threshold)
    db.execute(query)
    top_12 = db.fetchall()
    trending_list_by_hour = list()
    for ticker in top_12:
        db.execute("SELECT ticker, date_updated, SUM(mentions) OVER (ROWS UNBOUNDED PRECEDING) FROM "
                   "crypto_trending_hourly WHERE ticker=? AND date_updated >= ?", (ticker[0], date_threshold))
        running_sum = db.fetchall()
        running_sum = list(map(list, running_sum))
        trending_list_by_hour.append(running_sum)

    # Get change in mentions
    change_df = pd.read_sql_query("SELECT * FROM crypto_change", conn)

    return render(request, 'reddit/crypto_live.html', {"trending_list": trending_list,
                                                       "trending_list_by_hour": trending_list_by_hour,
                                                       "crypto_word_cloud": crypto_word_cloud,
                                                       "mentions_df": mentions_df.to_html(index=False),
                                                       "change_df": change_df.to_html(index=False),
                                                       })


def crypto_live_ticker(request):
    pd.options.display.float_format = '{:.2f}'.format
    ticker_selected = default_ticker(request, "BTC")

    df = pd.read_sql_query("SELECT mentions, sentiment, date_updated FROM crypto_trending_hourly "
                           "WHERE ticker='{}' ".format(ticker_selected), conn)

    sentiment_df = pd.read_sql_query("SELECT AVG(sentiment) as sentiment, strftime('%Y-%m-%d', date_updated) AS "
                                     "date_updated FROM crypto_trending_hourly WHERE ticker='{}' "
                                     "group by strftime('%Y-%m-%d', date_updated)".format(ticker_selected), conn)

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
        previous_snt = round(sentiment_df[(sentiment_df["date_updated"] >= last_14D) & (sentiment_df["date_updated"] < last_7D)]["sentiment"].mean(),
                             4)

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

    if request.GET.get("type") == "nasdaq100":
        filename = "database/indices/nasdaq100_heatmap.csv"
        title = "Nasdaq 100"
    elif request.GET.get("type") == "dia":
        filename = "database/indices/dia_heatmap.csv"
        title = "DIA"
    elif request.GET.get("type") == "crypto":
        title = "Cryptocurrency"
        return render(request, 'market_summary/market_summary.html', {"title": title})
    elif request.GET.get("type") == "wsb":
        title = "Wallstreetbets"
        summary_df = pd.read_sql_query("SELECT ticker, mentions, mkt_cap, price_change FROM wsb_yf", conn)
        return render(request, 'market_summary/market_summary.html', {"title": title,
                                                                      "summary_df": summary_df.to_html(index=False)})
    else:
        filename = "database/indices/snp500_heatmap.csv"
        title = "S&P 500"

    summary_df = pd.read_csv(filename)

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
    df = pd.read_csv("database/government/senate.csv")
    df["Disclosure Date"] = df["Disclosure Date"].astype(str)

    senator = request.GET.get("senator")
    ticker_selected = request.GET.get("quote")

    if senator:
        senator_df = df[df["Senator"] == senator]
        all_senators = df["Senator"].drop_duplicates().sort_values().to_list()
        del senator_df["Senator"]
        return render(request, 'government/senate_trading_individual.html',
                      {"senator_df": senator_df.to_html(index=False),
                       "senator": senator,
                       "all_senators": all_senators})

    elif ticker_selected:
        ticker_selected = ticker_selected.upper()

        ticker_df = df[df["Ticker"] == ticker_selected]
        del ticker_df["Ticker"]
        del ticker_df["Asset Description"]
        history_df = yf.Ticker(ticker_selected).history(period="5y", interval="1d")
        history_df.reset_index(inplace=True)
        history_df = history_df[["Date", "Close"]]

        all_tickers = df["Ticker"].drop_duplicates().sort_values().to_list()
        all_tickers.sort()
        all_tickers.remove("Unknown")
        return render(request, 'government/senate_ticker_analysis.html', {"ticker_df": ticker_df.to_html(index=False),
                                                                          "history_df": history_df.to_html(index=False),
                                                                          "ticker_selected": ticker_selected,
                                                                          "ticker_list": all_tickers})

    else:
        date_selected = request.GET.get("date_selected")
        if not date_selected:
            date_selected = df["Disclosure Date"].iloc[0]
        latest_df = df[df["Disclosure Date"] == date_selected]
        group_by_senator = pd.DataFrame(df.groupby(["Senator"]).agg({"Transaction Date": "count",
                                                                     "Disclosure Date": lambda x: x.iloc[0]}))
        group_by_senator.sort_values(by=["Disclosure Date"], ascending=False, inplace=True)
        group_by_senator.rename(columns={"Transaction Date": "Total",
                                         "Disclosure Date": "Last Disclosure"}, inplace=True)
        group_by_senator.reset_index(inplace=True)

        group_by_ticker = pd.DataFrame(df["Ticker"].value_counts())
        group_by_ticker.reset_index(inplace=True)
        group_by_ticker.columns = ["Ticker", "Count"]
        group_by_ticker = group_by_ticker[group_by_ticker["Ticker"] != "Unknown"]

        return render(request, 'government/senate_trading.html',
                      {"group_by_senator": group_by_senator.to_html(index=False),
                       "group_by_ticker": group_by_ticker.to_html(index=False),
                       "latest_df": latest_df.to_html(index=False),
                       "dates_available": df["Disclosure Date"].drop_duplicates().to_list(),
                       "date_selected": date_selected})


def crypto_transactions(request):
    return render(request, 'crypto_transaction.html')


def reverse_repo(request):
    """
    Get reverse repo. Data is from https://apps.newyorkfed.org/
    """
    pd.options.display.float_format = '{:.2f}'.format
    reverse_repo_stats = pd.read_sql_query("SELECT * FROM reverse_repo", conn)
    reverse_repo_stats['Moving Avg'] = reverse_repo_stats['amount'].rolling(window=7).mean()
    reverse_repo_stats.rename(columns={"record_date": "Date", "amount": "Amount", "parties": "Num Parties",
                                       "average": "Average"}, inplace=True)

    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/reverse_repo.html',
                  {"reverse_repo_stats": reverse_repo_stats[::-1].to_html(index=False),
                   "next_date": data})


def daily_treasury(request):
    """
    Get daily treasury. Data is from https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/operating-cash-balance
    """
    pd.options.display.float_format = '{:.2f}'.format
    daily_treasury_stats = pd.read_sql_query("SELECT * FROM daily_treasury", conn)
    daily_treasury_stats['Moving Avg'] = daily_treasury_stats['close_today_bal'].rolling(window=7).mean()
    daily_treasury_stats.rename(columns={"record_date": "Date", "close_today_bal": "Close Balance",
                                         "open_today_bal": "Open Balance", "amount_change": "Amount Change",
                                         "percent_change": "Percent Change"},
                                inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/daily_treasury.html',
                  {"daily_treasury_stats": daily_treasury_stats[::-1].to_html(index=False),
                   "next_date": data})


def inflation(request):
    """
    Get inflation. Data is from https://www.usinflationcalculator.com/inflation/current-inflation-rates/
    """
    pd.options.display.float_format = '{:.1f}'.format
    inflation_stats = pd.read_sql_query("SELECT * FROM inflation", conn).to_html(index=False)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/inflation.html', {"inflation_stats": inflation_stats, "next_date": data})


def retail_sales(request):
    """
    Get retail sales. Data is from https://ycharts.com/indicators/us_retail_and_food_services_sales
    """
    pd.options.display.float_format = '{:.2f}'.format
    retail_stats = pd.read_sql_query("SELECT * FROM retail_sales", conn)
    retail_stats.rename(columns={"record_date": "Date", "value": "Amount", "percent_change": "Percent Change",
                                 "covid_monthly_avg": "Monthly Avg Cases"}, inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/retail_sales.html',
                  {"retail_stats": retail_stats[::-1].to_html(index=False),
                   "next_date": data})


def initial_jobless_claims(request):
    pd.options.display.float_format = '{:.2f}'.format
    jobless_claims = pd.read_sql_query("SELECT * FROM initial_jobless_claims", conn)
    jobless_claims.rename(columns={"record_date": "Date", "value": "Number", "percent_change": "Percent Change"
                                   }, inplace=True)
    with open(r"database/economic_date.json", "r+") as r:
        data = json.load(r)
    return render(request, 'economy/initial_jobless_claims.html',
                  {"jobless_claims": jobless_claims[::-1].to_html(index=False),
                   "next_date": data})


def short_interest(request):
    """
    Get short interest of ticker. Data from https://www.stockgrid.io/shortinterest
    """
    pd.options.display.float_format = '{:.2f}'.format
    df_high_short_interest = pd.read_sql("SELECT * FROM short_interest", con=conn)
    df_high_short_interest.reset_index(inplace=True)
    df_high_short_interest.rename(columns={"index": "Rank"}, inplace=True)
    df_high_short_interest["Rank"] = df_high_short_interest["Rank"] + 1
    return render(request, 'discover/short_interest.html',
                  {"df_high_short_interest": df_high_short_interest.to_html(index=False)})


def low_float(request):
    """
    Get short interest of ticker. Data if from lowfloat.com
    """
    pd.options.display.float_format = '{:.2f}'.format
    df_low_float = pd.read_sql("SELECT * FROM low_float", con=conn)
    df_low_float.reset_index(inplace=True)
    df_low_float.rename(columns={"index": "Rank"}, inplace=True)
    df_low_float["Rank"] = df_low_float["Rank"] + 1
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
    df = pd.read_csv("database/ipo_calendar.csv")
    return render(request, 'discover/ipo_calendar.html', {"ipo_df": df.to_html(index=False)})


def stocktwits(request):
    ticker_selected = default_ticker(request, "TSLA")
    ticker_df = pd.read_sql_query("SELECT rank, watchlist, date_updated FROM stocktwits_trending WHERE "
                                  "symbol='{}' ".format(ticker_selected), conn)
    trending_df = pd.read_sql_query("SELECT rank, watchlist, symbol FROM stocktwits_trending "
                                    "ORDER BY date_updated DESC LIMIT 30", conn)
    return render(request, 'social/stocktwits.html', {"ticker_selected": ticker_selected,
                                                        "ticker_df": ticker_df.to_html(index=False),
                                                        "trending_df": trending_df.to_html(index=False)})


def twitter_trending(request):
    ticker_selected = default_ticker(request, "TSLA")
    ticker_df = pd.read_sql_query("SELECT tweet_count, updated_date FROM twitter_trending WHERE "
                                  "ticker='{}' ".format(ticker_selected), conn)
    # trending_df = pd.read_sql_query("SELECT rank, watchlist, symbol FROM stocktwits_trending "
    #                                 "ORDER BY date_updated DESC LIMIT 30", conn)
    print(ticker_df)
    return render(request, 'social/twitter_trending.html', {"ticker_selected": ticker_selected,
                                                        "ticker_df": ticker_df.to_html(index=False),
                                                        # "trending_df": trending_df.to_html(index=False)
                                                            })


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
                                                  "interval": interval.replace("1mo", "Monthly").replace("1d", "Daily")})


def covid_beta(request):
    """
    Compare performance of ticker with covid cases
    """
    pd.options.display.float_format = '{:.3f}'.format
    ticker_interested = default_ticker(request)
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
