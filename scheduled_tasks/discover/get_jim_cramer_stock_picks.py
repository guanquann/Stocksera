import os
import sys
import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def main(days=360):
    """
    Get the amazing Jim Cramer recent stocks recommendations
    """
    final_list = []
    for i in range(days, 0, -1):
        try:
            date = str(datetime.utcnow().date() - timedelta(days=i))
            url = f"https://madmoney.thestreet.com/screener/index.cfm?showview=stocks&showrows=500&airdate={date}"
            x = BeautifulSoup(requests.get(url).text, "lxml").find(id="stockTable")

            segment_dict = {"F": "Featured", "D": "Discussed", "L": "Lightning", "I": "Guest"}
            call_dict = {"5": "Buy", "4": "Positive", "3": "Hold", "2": "Negative", "1": "Sell"}

            for tr in x.find_all("tr")[1:]:
                tds = tr.find_all("td")

                segment = tds[2].find("img")["alt"]
                if segment in segment_dict.keys():
                    segment = segment_dict[segment]
                    ticker = tds[0].get_text()
                    ticker = ticker[ticker.find("(") + 1:ticker.find(")")]
                    call = call_dict[tds[3].find("img")["alt"]]
                    price = float(tds[4].get_text().replace("$", ""))
                    print(ticker, date, segment, call, price)
                    final_list.append({"Ticker": ticker,
                                       "Date": date,
                                       "Segment": segment,
                                       "Call": call,
                                       "Price": price})
        except IndexError:
            pass
    df = pd.DataFrame(final_list)
    print(df)
    df.to_sql("jim_cramer_trades", engine, if_exists="append", index=False)


if __name__ == '__main__':
    main()
