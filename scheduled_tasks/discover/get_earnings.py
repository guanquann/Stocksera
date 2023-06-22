import os
import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database, finnhub_client, long_number_format, get_ticker_list_stats

cnx, cur, engine = connect_mysql_database()


def main():
    print("Getting Earnings...")
    current_date = datetime.utcnow().date()
    current_index = 0

    cur.execute("DELETE FROM earnings")
    main_df = pd.DataFrame()
    while current_index != 21:
        df = pd.DataFrame(finnhub_client.earnings_calendar(_from=str(current_date+timedelta(days=current_index)),
                                                           to=str(current_date+timedelta(days=current_index+7)),
                                                           symbol="",
                                                           international=False)["earningsCalendar"])
        df = df[["date", "hour", "symbol", "epsEstimate", "epsActual", "revenueEstimate", "revenueActual",
                 "year", "quarter"]]
        current_index += 7
        main_df = main_df.append(df)
    main_df = main_df[main_df["symbol"].str.len() <= 4]

    mkt_cap_df = get_ticker_list_stats(main_df["symbol"].tolist())[["symbol", "marketCap"]]

    main_df = pd.merge(main_df, mkt_cap_df, on="symbol", how="left")
    main_df.fillna("N/A", inplace=True)
    main_df["hour"] = main_df["hour"].str.upper()
    main_df["marketCap"] = main_df["marketCap"].apply(lambda x: long_number_format(x))
    cur.executemany("INSERT IGNORE INTO earnings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    main_df.values.tolist())
    cnx.commit()
    print("Earnings Successfully Completed...\n")


if __name__ == '__main__':
    main()
