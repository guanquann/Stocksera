import os
import sys
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import *

cnx, cur, engine = connect_mysql_database()


def get_high_short_interest():
    """
    Returns a high short interest DataFrame.
    """
    print("Getting Short Interest...")
    df = pd.DataFrame.from_dict(requests.get("https://www.stockgrid.io/get_short_interest").json()["data"])
    df.sort_values(by=["Short Interest"], ascending=False, inplace=True)
    df = df[["Ticker", "Date", "Short Interest", "Average Volume", "Days To Cover", "%Float Short"]]
    df.to_sql("short_interest", engine, if_exists="replace", index=False)
    print("Short Interest Successfully Completed...\n")


def get_low_float():
    """
    Returns low float DataFrame
    Adapted from https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal
    """
    print("Getting Low Float...")
    text_soup_low_float_stocks = BeautifulSoup(requests.get("https://www.lowfloat.com").text, "lxml")

    a_low_float_header = list()
    for low_float_header in text_soup_low_float_stocks.findAll(
        "td", {"class": "tblhdr"}
    ):
        a_low_float_header.append(low_float_header.text.strip("\n").split("\n")[0])
    df_low_float = pd.DataFrame(columns=a_low_float_header)

    stock_list_tr = text_soup_low_float_stocks.find_all("tr")

    for a_stock in stock_list_tr:
        a_stock_txt = a_stock.text

        if a_stock_txt == "":
            continue

        low_float_data = a_stock_txt.split("\n")

        if len(low_float_data) == 8:
            df_low_float.loc[len(df_low_float.index)] = low_float_data[:-1]

    stats_df = get_ticker_list_stats(df_low_float["Ticker"].to_list())
    stats_df.rename(columns={"symbol": "Ticker"}, inplace=True)

    results_df = pd.merge(df_low_float, stats_df, on="Ticker")

    cur.execute("DELETE FROM low_float")
    for index, row in results_df.iterrows():
        cur.execute("INSERT INTO low_float VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (row['Ticker'], row['name'], row['exchange'], row['previousClose'],
                     round(row['changesPercentage'], 2), row['Float'], row['Outstd'], row['ShortInt'],
                     long_number_format(row['marketCap']), row['Industry']))
        cnx.commit()
    print("Low Float Successfully Completed...\n")


def main():
    get_high_short_interest()
    get_low_float()


if __name__ == '__main__':
    main()
