import os
import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database, finnhub_client
import scheduled_tasks.reddit.stocks.fast_yahoo as fast_yahoo


cnx, cur, engine = connect_mysql_database()


def main():
    current_date = datetime.utcnow().date()
    current_index = 0

    cur.execute("DELETE FROM earnings")
    main_df = pd.DataFrame()
    while current_index != 21:
        df = pd.DataFrame(finnhub_client.earnings_calendar(_from=str(current_date+timedelta(days=current_index)),
                                                           to=str(current_date+timedelta(days=current_index+7)),
                                                           symbol="",
                                                           international=False)["earningsCalendar"])
        df = df[["date", "hour", "symbol", "epsEstimate", "epsActual", "revenueEstimate", "revenueActual", "year", "quarter"]]
        current_index += 7
        main_df = main_df.append(df)

    # mkt_cap_df = fast_yahoo.download_quick_stats(main_df["symbol"].tolist(), {'marketCap': 'mkt_cap'})

    mkt_cap_df = pd.DataFrame()
    current_index = 0
    while current_index < len(main_df["symbol"].tolist()):
        quick_stats_df = fast_yahoo.download_advanced_stats(main_df["symbol"].tolist()
                                                            [current_index:current_index + 100],
                                                            {'price': {"marketCap": "mkt_cap"}}, threads=True)
        mkt_cap_df = pd.concat([mkt_cap_df, quick_stats_df])
        current_index += 100

    mkt_cap_df.reset_index(inplace=True)
    mkt_cap_df.replace("N/A", 0, inplace=True)
    mkt_cap_df.rename(columns={"Symbol": "symbol"}, inplace=True)
    main_df = pd.merge(main_df, mkt_cap_df, on="symbol", how="left")
    main_df.fillna("N/A", inplace=True)
    main_df["hour"] = main_df["hour"].str.upper()
    print(main_df)
    cur.executemany("INSERT IGNORE INTO earnings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    main_df.values.tolist())
    cnx.commit()


if __name__ == '__main__':
    main()
