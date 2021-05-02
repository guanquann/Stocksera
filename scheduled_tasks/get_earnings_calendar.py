from datetime import datetime, timedelta
import os
import psycopg2
import yfinance.ticker as yf
from yahoo_earnings_calendar import YahooEarningsCalendar

# If using database from Heroku
if os.environ.get('DATABASE_URL'):
    postgres_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(postgres_url, sslmode='require')
# If using local database
else:
    conn = psycopg2.connect("dbname=stocks_analysis "
                            "user=postgres "
                            "password=admin")
conn.autocommit = True
db = conn.cursor()

yec = YahooEarningsCalendar(0)

# db.execute("DELETE FROM earnings_calendar")

ticker_list = list()
date_from = datetime.now()+timedelta(days=2)
date_to = datetime.now()+timedelta(days=5)
for i in yec.earnings_on(date_to):
# for i in yec.earnings_between(date_from, date_to):
    symbol = i["ticker"]
    ticker = yf.Ticker(symbol)

    name = i["companyshortname"]
    date = i["startdatetime"].split("T")[0]
    time = i["startdatetimetype"]
    epsestimate = str(i["epsestimate"]).replace("None", "N/A")
    epsactual = str(i["epsactual"]).replace("None", "N/A")

    information = ticker.info
    mkt_cap = information["marketCap"]
    img = information["logo_url"]

    db.execute("""INSERT INTO earnings_calendar (name, symbol, mkt_cap, eps_est, eps_act, img_url, earning_date, earning_time) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                (name, symbol, mkt_cap, epsestimate, epsactual, img, date, time))
    print(ticker, date, time)
print("DONE")