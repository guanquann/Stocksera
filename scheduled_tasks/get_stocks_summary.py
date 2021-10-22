import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from scheduled_tasks.reddit.stocks.fast_yahoo import download_advanced_stats

INDICES_PATH = "database/indices"

if not os.path.exists(INDICES_PATH):
    os.mkdir(INDICES_PATH)
    snp500_df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    snp500_df["Symbol"].to_csv(INDICES_PATH + "snp500.csv", index=False)

    nasdaq_df = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[3]
    nasdaq_df.rename(columns={"Ticker": "Symbol"})
    nasdaq_df["Symbol"].to_csv(INDICES_PATH + "nasdaq100.csv", index=False)


def main():
    quick_stats_dict = {'price': {"marketCap": "Market Cap",
                                  "regularMarketChangePercent": "price_change",
                                  'regularMarketPrice': 'current_price'},
                        'summaryDetail': {"sector": "Sector",
                                          "industry": "Industry"}}
    # quick_stats_dict = {'price': {"marketCap": "Market Cap", 'regularMarketChangePercent': '% Change'},
    #                     'summaryProfile': {'sector': "Sector", 'industry': "Industry", }
    #                     }
    for indice in ["snp500", "nasdaq100"]:
        snp = pd.read_csv(os.path.join(INDICES_PATH, f"{indice}.csv"))
        symbol_list = snp["Symbol"].to_list()
        symbol_list.remove("GOOG")
        original_df = pd.DataFrame()

        current_index = 0
        while current_index < len(symbol_list):
            quick_stats_df = download_advanced_stats(symbol_list[current_index:current_index + 100],
                                                     quick_stats_dict, threads=True)
            original_df = pd.concat([original_df, quick_stats_df])
            current_index += 100

        original_df["% Change"] = original_df["% Change"] * 100
        original_df = original_df.reindex(symbol_list)
        original_df.reset_index(inplace=True)

        original_df = original_df[original_df["Market Cap"] != "N/A"]
        print(original_df)
        original_df.to_csv(f"database/indices/{indice}_heatmap.csv", index=False)


if __name__ == '__main__':
    main()
