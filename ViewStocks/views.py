import os
import time

from custom_extensions.custom_words import *
from helpers import *

import psycopg2

from yahoo_earnings_calendar import YahooEarningsCalendar
from finvizfinance.quote import finvizfinance

from django.shortcuts import render, redirect
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# If using database from Heroku
if os.environ.get('DATABASE_URL'):
    postgres_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(postgres_url, sslmode='require')
# If using local database
else:
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            database="stocks_analysis")

conn.autocommit = True
db = conn.cursor()

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)


def main(request):
    return render(request, "home.html")


def stock_price(request):
    if request.GET.get("financial"):
        ticker_selected = request.GET['financial'].upper()
        return redirect('/ticker/financial/?quote=%s' % ticker_selected)

    elif request.GET.get("options"):
        ticker_selected = request.GET['options'].upper()
        return redirect('/ticker/options/?quote=%s' % ticker_selected)

    elif request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()
        try: 
            ticker = yf.Ticker(ticker_selected)
            ticker_fin = finvizfinance(ticker_selected)
            ticker_fin_fundament = ticker_fin.TickerFundament()
                            
            if "five_day" in request.GET:
                price_df = ticker.history(period="5d", interval="30m")
                ticker_date_max = list(map(lambda x: x.split(" ")[0], price_df.index.astype(str).to_list()))
                duration = "1"
            elif "one_month" in request.GET:
                price_df = ticker.history(period="1mo", interval="1d")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "2"
            elif "one_year" in request.GET:
                price_df = ticker.history(period="1y", interval="1d")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "3"
            elif "five_year" in request.GET:
                price_df = ticker.history(period="5y", interval="1wk")
                ticker_date_max = price_df.index.astype(str).to_list()
                duration = "4"
            else:
                price_df = ticker.history(period="1d", interval="2m")
                ticker_date_max = list(map(lambda x: x.split(" ")[1].split("-")[0].rsplit(":", 1)[0],
                                       price_df.index.astype(str).to_list()))
                duration = "0"

            information = ticker.info
            img = information["logo_url"]
            official_name = ticker_fin_fundament["Company"]

            try:
                recommendations = ticker_fin.TickerOuterRatings()
                recommendations = recommendations.to_html(index=False)
            except AttributeError:
                recommendations = "N/A"

            major_holders = ticker.major_holders
            major_holders = major_holders.to_html(index=False, header=False)
            
            institutional_holders = ticker.institutional_holders
            if institutional_holders is not None:
                institutional_holders = institutional_holders.to_html(index=False)
            else:
                institutional_holders = "N/A"

            # print(ticker.calendar)
            # print(ticker.financials)
            # print(ticker.earnings)
            # print(ticker.sustainability, "SUS")

            sector = ticker_fin_fundament['Sector']
            industry = ticker_fin_fundament["Industry"]
            summary = ticker_fin.TickerDescription()
            if "website" in information and information['website'] is not None:
                website = information["website"]
            else:
                website = "https://finance.yahoo.com/quote/{}".format(ticker_selected)

            latest_price = information["regularMarketPrice"]

            mkt_open = round(information["regularMarketOpen"], 2)
            mkt_close = round(information["previousClose"], 2)
            mkt_low = round(information["regularMarketDayLow"], 2)
            mkt_high = round(information["dayHigh"], 2)
            mkt_vol = information["regularMarketVolume"]

            twoHundredDayAverage = information["twoHundredDayAverage"]
            averageDailyVolume10Day = information["averageDailyVolume10Day"]

            dividend_yield = information["trailingAnnualDividendYield"]
            dividend_amount = information["trailingAnnualDividendRate"]
            if dividend_yield is not None:
                dividend_yield = str(round(dividend_yield * 100, 2)) + "%"
                dividend_amount = "$" + str(dividend_amount)
            else:
                dividend_yield = "N/A"
                dividend_amount = "N/A"

            ex_div_date = information["exDividendDate"]
            if ex_div_date is not None:
                ex_div_date = str(time.strftime('%Y-%m-%d %H:%M:%S',
                                                time.localtime(information["exDividendDate"]))).split()[0]
            else:
                ex_div_date = "N/A"

            mkt_cap = ticker_fin_fundament["Market Cap"]

            p_e_ratio = ticker_exception("trailingPE", information)
            forward_p_e = ticker_exception("forwardPE", information)
            beta = ticker_exception("beta", information)
            eps = ticker_exception("trailingEps", information)

            if mkt_vol < 1000000:
                mkt_vol = str(round(mkt_vol/1000, 2)) + "K"
            elif 1000000 <= mkt_vol < 1000000000:
                mkt_vol = str(round(mkt_vol / 1000000, 2)) + "M"
            else:
                mkt_vol = str(round(mkt_vol / 1000000000, 2)) + "B"

            mkt_year_high = round(information["fiftyTwoWeekHigh"], 2)
            mkt_year_low = round(information["fiftyTwoWeekLow"], 2)
            
            price_change = round(latest_price - mkt_close, 2)
            price_percentage_change = ticker_fin_fundament['Change']

            shares_outstanding = ticker_fin_fundament['Shs Outstand']
            shares_float = ticker_fin_fundament['Shs Float']
            short_float = ticker_fin_fundament['Short Float']
            short_ratio = ticker_fin_fundament['Short Ratio']
            price_target = ticker_fin_fundament['Target Price']
            rsi = ticker_fin_fundament['RSI (14)']
            sma20 = ticker_fin_fundament['SMA20']
            sma50 = ticker_fin_fundament['SMA50']
            sma200 = ticker_fin_fundament['SMA200']

            news_df = ticker_fin.TickerNews()
            news_df["Date"] = news_df["Date"].dt.date
            del news_df["Link"]

            news_df = news_df.to_html(index=False)

            return render(request, 'ticker_price.html', {"ticker_selected": ticker_selected,
                                                         "ticker_date_max": ticker_date_max,
                                                         "ticker_price_max": list(map(lambda x: round(x, 2),
                                                                                      price_df["Close"].to_list())),
                                                         "duration": duration,
                                                         "img": img, "official_name": official_name,
                                                         "sector": sector, "industry": industry,
                                                         "mkt_open": mkt_open, "mkt_close": mkt_close,
                                                         "mkt_low": mkt_low, "mkt_high": mkt_high, "mkt_vol": mkt_vol,
                                                         "mkt_year_high": mkt_year_high, "mkt_year_low": mkt_year_low,
                                                         "latest_price": latest_price, "price_change": price_change,
                                                         "price_percentage_change": price_percentage_change,
                                                         "dividend_yield": dividend_yield,
                                                         "dividend_amount": dividend_amount,
                                                         "ex_div_date": ex_div_date,
                                                         "mkt_cap": mkt_cap, "p_e_ratio": p_e_ratio,
                                                         "twoHundredDayAverage": twoHundredDayAverage,
                                                         "averageDailyVolume10Day": averageDailyVolume10Day,
                                                         "forward_p_e": forward_p_e, "eps": eps, "beta": beta,
                                                         "recommendations": recommendations,
                                                         "institutional_holders": institutional_holders,
                                                         "major_holders": major_holders,
                                                         "website": website, "summary": summary,
                                                         "shares_outstanding": shares_outstanding,
                                                         "shares_float": shares_float,
                                                         "short_float": short_float,
                                                         "short_ratio": short_ratio, "price_target": price_target,
                                                         "rsi": rsi, "sma20": sma20, "sma50": sma50, "sma200": sma200,
                                                         "news_df": news_df
                                                         })
        except (IndexError, KeyError, Exception):
            return render(request, 'ticker_price.html', {"ticker_selected": "-", "incorrect_ticker": ticker_selected})
    return render(request, 'ticker_price.html')


def financial(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()

        balance_list = []        
        balance_sheet = yf.Ticker(ticker_selected).quarterly_balance_sheet.replace(np.nan, 0)
        print(balance_sheet)

        date_list = balance_sheet.columns.astype("str").to_list()
        balance_col_list = balance_sheet.index.tolist()
        
        for i in range(len(balance_sheet)):
            values = balance_sheet.iloc[i].tolist()
            balance_list.append(values)

        yec = YahooEarningsCalendar(0)
        earnings = yec.get_earnings_of(ticker_selected)
        
        earnings_list, financial_quarter_list = [], []
        # [[1, 0.56, 0.64], [2, 0.51, 0.65], [3, 0.7, 0.73], [4, 1.41, 1.68], [5, 0.98]]
        count = 5
        for earning in earnings:
            if len(earnings_list) != 5:   
                if earning["epsestimate"] is not None:
                    if earning["epsactual"] is not None:
                        earnings_list.append([count, earning["epsestimate"], earning["epsactual"]])
                    else:
                        earnings_list.append([count, earning["epsestimate"]])   

                    year_num = earning["startdatetime"].split("T")[0].split("-")[0]  
                    month_num = int(earning["startdatetime"].split("T")[0].split("-")[1])
                    if month_num in [1, 2, 3]:
                        year_num = int(year_num) - 1
                        quarter = "Q4"
                    elif month_num in [4, 5, 6]:
                        quarter = "Q1"
                    elif month_num in [7, 8, 9]:
                        quarter = "Q2"
                    else:
                        quarter = "Q3"
                    financial_quarter_list.append("{} {}".format(year_num, quarter))

                count -= 1  
            else:
                break
        return render(request, 'financial.html', {"ticker_selected": ticker_selected,
                                                  "date_list": date_list,
                                                  "balance_list": balance_list,
                                                  "balance_col_list": balance_col_list,
                                                  "earnings_list": earnings_list,
                                                  "financial_quarter_list": financial_quarter_list, })
    else:
        return render(request, 'financial.html')


def options(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()
        ticker = yf.Ticker(ticker_selected)

        information = ticker.info
        try:
            sector = information["sector"]
            industry = information["industry"]
        except KeyError:
            sector = "-"
            industry = "-"
        img = information["logo_url"]
        official_name = information["longName"]

        options_dates = ticker.options

        if request.GET.get("date"):
            date_selected = request.GET["date"]
        else:
            date_selected = options_dates[0]

        calls = ticker.option_chain(date_selected).calls

        del calls["contractSize"]
        del calls["currency"]
        calls.columns = ["Contract Name", "Last Trade Date", "Strike", "Last Price", "Bid", "Ask", "Change",
                         "% Change", "Volume", "Open Interest", "Implied Volatility", "ITM"]

        last_adj_close_price = float(ticker.info['previousClose'])
        df_calls = calls.pivot_table(
            index="Strike", values=["Volume", "Open Interest"], aggfunc="sum"
        ).reindex()
        df_calls["Strike"] = df_calls.index
        df_calls["Type"] = "calls"
        df_calls["Open Interest"] = df_calls["Open Interest"]
        df_calls["Volume"] = df_calls["Volume"]
        df_calls["oi+v"] = df_calls["Open Interest"] + df_calls["Volume"]
        df_calls["Spot"] = round(last_adj_close_price, 2)

        calls["Volume"].fillna('-', inplace=True)
        calls["Open Interest"].fillna('-', inplace=True)
        calls["Implied Volatility"] = calls["Implied Volatility"].astype("float").multiply(100)
        
        calls["Change"] = calls["Change"].round(2)
        calls["% Change"] = calls["% Change"].round(2)
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

        puts["Volume"].fillna('-', inplace=True)
        puts["Open Interest"].fillna('-', inplace=True)
        puts["Implied Volatility"] = puts["Implied Volatility"].astype("float").multiply(100)

        puts["Change"] = puts["Change"].round(2)
        puts["% Change"] = puts["% Change"].round(2)
        puts["Implied Volatility"] = puts["Implied Volatility"].round(2)

        df_merge = pd.merge(calls, puts, on="Strike")
        df_merge = df_merge[["Last Price_x", "Change_x", "% Change_x", "Volume_x", "Open Interest_x", "Strike",
                             "Last Price_y", "Change_y", "% Change_y", "Volume_y", "Open Interest_y"]]
        df_merge.columns = ["Last Price", "Change", "% Change", "Volume", "Open Interest", "Strike",
                            "Last Price", "Change", "% Change", "Volume", "Open Interest"]
        
        df_opt = pd.merge(df_calls, df_puts, left_index=True, right_index=True)
        df_opt = df_opt[["Open Interest_x", "Open Interest_y"]].rename(
            columns={"Open Interest_x": "OI Calls", "Open Interest_y": "OI Puts"})
        max_pain, call_loss_list, put_loss_list = get_max_pain(df_opt)        
        
        return render(request, 'options.html', {"ticker_selected": ticker_selected, 
                                                "official_name": official_name,
                                                "img": img,
                                                "industry": industry,
                                                "sector": sector,
                                                "options_dates": options_dates, 
                                                "date_selected": date_selected, 
                                                "max_pain": max_pain, 
                                                "call_loss_list": call_loss_list, 
                                                "put_loss_list": put_loss_list, 
                                                "calls": calls.to_html(index=False), 
                                                "puts": puts.to_html(index=False), 
                                                "merge": df_merge.to_html(index=False)})
    else:
        return render(request, 'options.html')


def earnings_calendar(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    db.execute("SELECT * FROM earnings_calendar ORDER BY earning_date ASC")
    calendar = db.fetchall()
    calendar = list(map(list, calendar))

    return render(request, 'earnings_calendar.html', {"popular_ticker_list": popular_ticker_list,
                                                      "popular_name_list": popular_name_list,
                                                      "price_list": price_list, 
                                                      "earnings_calendar": calendar})


def reddit_analysis(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    if request.GET.get("subreddit"):
        subreddit = request.GET.get("subreddit").lower().replace(" ", "")
        if subreddit == "all":
            db.execute("SELECT * FROM reddit_trending ORDER BY score DESC")
        else:
            db.execute("SELECT * FROM {} ORDER BY recent DESC LIMIT 50".format(subreddit))
        trending_tickers = db.fetchall()
        database_mapping = {"wallstreetbets": "Wall Street Bets"}

        subreddit = database_mapping[subreddit]
        return render(request, 'reddit_sentiment.html', {"popular_ticker_list": popular_ticker_list,
                                                         "popular_name_list": popular_name_list,
                                                         "price_list": price_list,
                                                         "trending_tickers": trending_tickers,
                                                         "subreddit_selected": subreddit})
    else:
        return render(request, 'reddit_sentiment.html', {"popular_ticker_list": popular_ticker_list,
                                                         "popular_name_list": popular_name_list,
                                                         "price_list": price_list})


def subreddit_count(request):
    db.execute("SELECT * FROM subreddit_count ")
    subscribers = db.fetchall()
    subscribers = list(map(list, subscribers))
    return render(request, 'subreddit_count.html', {"subscribers": subscribers})


def top_movers(request):
    top_gainers = pd.read_html("https://finance.yahoo.com/screener/predefined/day_gainers")[0]
    top_gainers["PE Ratio (TTM)"] = top_gainers["PE Ratio (TTM)"].replace(np.nan, "N/A")
    del top_gainers["52 Week Range"]

    top_losers = pd.read_html("https://finance.yahoo.com/screener/predefined/day_losers")[0]
    top_losers["PE Ratio (TTM)"] = top_gainers["PE Ratio (TTM)"].replace(np.nan, "N/A")
    del top_losers["52 Week Range"]

    return render(request, 'top_movers.html', {"top_gainers": top_gainers.to_html(index=False),
                                               "top_losers": top_losers.to_html(index=False)})


def short_interest(request):
    df_high_short_interest = get_high_short_interest()
    return render(request, 'short_interest.html',
                  {"df_high_short_interest": df_high_short_interest.to_html(index=False)})


def low_float(request):
    df_low_float = get_low_float()
    return render(request, 'low_float.html', {"df_low_float": df_low_float.to_html(index=False)})


def penny_stocks(request):
    df_penny_stocks = get_penny_stocks()
    return render(request, 'penny_stocks.html', {"df_penny_stocks": df_penny_stocks.to_html(index=False)})


def latest_news(request):
    if request.GET.get("quote"):
        ticker_selected = request.GET['quote'].upper()
    else:
        ticker_selected = "AAPL"
    ticker_fin = finvizfinance(ticker_selected)

    news_df = ticker_fin.TickerNews()
    news_df["Date"] = news_df["Date"].dt.date
    del news_df["Link"]

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
    return render(request, 'news_sentiment.html', {"news_df": news_df})


def industries_analysis(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    return render(request, 'industry.html')


def reddit_etf(request):
    popular_ticker_list, popular_name_list, price_list = ticker_bar()
    db.execute("SELECT * FROM wallstreetbets LIMIT 100")
    return render(request, 'reddit_etf.html', {"popular_ticker_list": popular_ticker_list,
                                               "popular_name_list": popular_name_list,
                                               "price_list": price_list})


def opinion(request):
    return render(request, 'opinion.html')


def contact(request):
    return render(request, 'contact.html')
