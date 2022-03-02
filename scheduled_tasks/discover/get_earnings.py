import os
import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database, finnhub_client


def main():
    cnx, engine = connect_mysql_database()
    cur = cnx.cursor()

    current_date = datetime.utcnow().date()
    current_index = -7

    cur.execute("DELETE FROM earnings")
    while current_index != 28:
        df = pd.DataFrame(finnhub_client.earnings_calendar(_from=str(current_date+timedelta(days=current_index)),
                                                           to=str(current_date+timedelta(days=current_index+7)),
                                                           symbol="",
                                                           international=False)["earningsCalendar"])
        print(df)
        df = df[["date", "hour", "symbol", "epsEstimate", "epsActual", "revenueEstimate", "revenueActual", "year", "quarter"]]
        df.fillna("", inplace=True)
        current_index += 7
        cur.executemany("INSERT INTO earnings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", df.values.tolist())
        cnx.commit()


if __name__ == '__main__':
    main()
