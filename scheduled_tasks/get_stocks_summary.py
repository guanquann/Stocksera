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
    snp = pd.read_csv(os.path.join(INDICES_PATH, "snp500.csv"))
    nasdaq = pd.read_csv(os.path.join(INDICES_PATH, "nasdaq100.csv"))
    merge_df = snp.append(nasdaq)
    merge_df.drop_duplicates(inplace=True)

    quick_stats_dict = {'price': {"marketCap": "Market Cap",
                                  "regularMarketPreviousClose": "Prev Close",
                                  'regularMarketPrice': 'Current Price'},
                        'summaryProfile': {"sector": "Sector",
                                           "industry": "Industry"}}

    symbol_list = merge_df["Symbol"].to_list()
    symbol_list.remove("GOOG")
    original_df = pd.DataFrame()

    current_index = 0
    while current_index < len(symbol_list):
        quick_stats_df = download_advanced_stats(symbol_list[current_index:current_index + 100],
                                                 quick_stats_dict, threads=True)
        original_df = pd.concat([original_df, quick_stats_df])
        current_index += 100

    original_df["Current Price"] = pd.to_numeric(original_df["Current Price"], errors='coerce')
    original_df["Prev Close"] = pd.to_numeric(original_df["Prev Close"], errors='coerce')
    original_df["% Change"] = (original_df["Current Price"] - original_df["Prev Close"]) * 100 / original_df["Prev Close"]
    original_df = original_df.reindex(symbol_list)
    original_df.reset_index(inplace=True)

    original_df = original_df[original_df["Market Cap"] != "N/A"]
    original_df = original_df[["Symbol", "Market Cap", "% Change", "Sector", "Industry"]]

    snp_out = pd.merge(snp, original_df, on="Symbol", how="left")
    snp_out.to_csv(f"database/indices/snp500_heatmap.csv", index=False)
    print(snp_out)

    nasdaq_out = pd.merge(nasdaq, original_df, on="Symbol", how="left")
    nasdaq_out.to_csv(f"database/indices/nasdaq100_heatmap.csv", index=False)
    print(nasdaq_out)


if __name__ == '__main__':
    main()
