import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from helpers import get_ticker_list_stats

INDICES_PATH = "database/indices"


def main():
    """
    Get performance of stocks in DIA, S&P500 and Nasdaq
    """
    print("Getting Stocks Summary...")

    if not os.path.exists(INDICES_PATH):
        os.mkdir(INDICES_PATH)

    snp500_df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]
    snp500_df.rename(columns={"Symbol": "symbol"}, inplace=True)
    snp500_df = snp500_df[["symbol", "GICS Sector", "GICS Sub-Industry"]]

    nasdaq_df = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]
    nasdaq_df.rename(columns={"Ticker": "symbol"}, inplace=True)
    nasdaq_df = nasdaq_df[["symbol", "GICS Sector", "GICS Sub-Industry"]]

    dia_df = pd.read_html(
        "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    )[1]
    dia_df.rename(columns={"Symbol": "symbol"}, inplace=True)
    dia_df = dia_df[["symbol"]]
    dia_df = dia_df.merge(
        snp500_df,
        how="left",
        on="symbol",
    )

    merged_df = (
        pd.concat([snp500_df, nasdaq_df], ignore_index=True)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    ticker_stats_df = get_ticker_list_stats(merged_df["symbol"].to_list())[
        ["symbol", "marketCap", "changesPercentage"]
    ]

    snp500_df = snp500_df.merge(
        ticker_stats_df,
        how="left",
        on="symbol",
    )[["symbol", "marketCap", "changesPercentage", "GICS Sector", "GICS Sub-Industry"]]
    snp500_df.columns = ["Symbol", "Market Cap", "% Change", "Sector", "Industry"]

    snp500_df.to_csv(f"database/indices/snp500_heatmap.csv", index=False)

    nasdaq_df = nasdaq_df.merge(
        ticker_stats_df,
        how="left",
        on="symbol",
    )[["symbol", "marketCap", "changesPercentage", "GICS Sector", "GICS Sub-Industry"]]
    nasdaq_df.columns = ["Symbol", "Market Cap", "% Change", "Sector", "Industry"]

    nasdaq_df.to_csv(f"database/indices/nasdaq100_heatmap.csv", index=False)

    dia_df = dia_df.merge(
        ticker_stats_df,
        how="left",
        on="symbol",
    )[["symbol", "marketCap", "changesPercentage", "GICS Sector", "GICS Sub-Industry"]]
    dia_df.columns = ["Symbol", "Market Cap", "% Change", "Sector", "Industry"]

    dia_df.to_csv(f"database/indices/dia_heatmap.csv", index=False)

    print("Stocks Summary Successfully Completed...\n")


if __name__ == "__main__":
    main()
