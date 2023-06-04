import os
import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database, finnhub_client
from scheduled_tasks.reddit.stocks.fast_yahoo import download_advanced_stats_multi_thread

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
    mkt_cap_df = download_advanced_stats_multi_thread(main_df["symbol"].tolist(),
                                                      {'price': {"marketCap": "mkt_cap"}}, 1)
    mkt_cap_df.reset_index(inplace=True)
    mkt_cap_df.replace("N/A", 0, inplace=True)
    mkt_cap_df.rename(columns={"Symbol": "symbol"}, inplace=True)
    main_df = pd.merge(main_df, mkt_cap_df, on="symbol", how="left")
    main_df.fillna("N/A", inplace=True)
    main_df["hour"] = main_df["hour"].str.upper()
    cur.executemany("INSERT IGNORE INTO earnings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    main_df.values.tolist())
    cnx.commit()
    print("Earnings Successfully Completed...\n")


if __name__ == '__main__':
    main()
