from datetime import datetime, timedelta
import sqlite3
import yfinance.ticker as yf
from yahoo_earnings_calendar import YahooEarningsCalendar

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()

yec = YahooEarningsCalendar(0)


def get_new_earnings():
    """
    Get the earnings for the next 7 days
    """
    date_from = datetime.now()
    date_to = datetime.now() + timedelta(days=7)
    for i in yec.earnings_between(date_from, date_to):  # for i in yec.earnings_on(date_to):
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

        db.execute("""INSERT INTO earnings_calendar 
                      (name, symbol, mkt_cap, eps_est, eps_act, img_url, earning_date, earning_time) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                   (name, symbol, mkt_cap, epsestimate, epsactual, img, date, time))
        conn.commit()
        print(ticker, date, time)
    print("Added new earnings successfully")


def update_previous_earnings():
    """
        Update the earnings (eps_actual) for the last 7 days
    """
    date_from = datetime.now() - timedelta(days=7)
    date_to = datetime.now()
    for i in yec.earnings_between(date_from, date_to):
        symbol = i["ticker"]
        epsactual = str(i["epsactual"]).replace("None", "N/A")
        db.execute("UPDATE earnings_calendar SET eps_act=? WHERE symbol=? ", (epsactual, symbol))
    print("Updated previous earnings successfully")


if __name__ == '__main__':
    get_new_earnings()
    update_previous_earnings()
    print("DONE")
