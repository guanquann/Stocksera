import os
import sys
import sqlite3
import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()


def main(days=180):
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
                    symbol = tds[0].get_text()
                    symbol = symbol[symbol.find("(") + 1:symbol.find(")")]
                    call = call_dict[tds[3].find("img")["alt"]]
                    price = tds[4].get_text()
                    print(symbol, date, segment, call, price)
                    final_list.append({"Symbol": symbol,
                                       "Date": date,
                                       "Segment": segment,
                                       "Call": call,
                                       "Price": price})
        except IndexError:
            pass

    df = pd.DataFrame(final_list)
    df.to_sql("jim_cramer_trades", conn, if_exists="append", index=False)


if __name__ == '__main__':
    main(days=5)
