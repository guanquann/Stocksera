import os
import pandas as pd


def preprocess_hedge_funds(csv, fund_name):
    """
    Get hedge funds holding from their 13F filling. Data is from https://whalewisdom.com/. You need to sign up a free account to access the csv files. Data is updated quarterly.
    csv: csv file path
    fund_name: name of the csv file you want to save. I would advice you to name it the same as the hedge fund name.
    """
    df = pd.read_csv(csv)
    df.fillna("N/A", inplace=True)
    df = df.apply(lambda x: x.astype(str).str.upper())
    del df["Qtr first owned"]
    del df["Recent Price"]
    df = df[df["source_type"] == "13F"]
    df["% Ownership"] = df["% Ownership"].round(2)
    rank_col = df.pop("Ranking")
    df = pd.concat((rank_col, df), axis=1)
    df.columns = ["Rank", "Stock", "Ticker", "Type", "Quantity", "Market Value", "% Portfolio", "Previous % Portfolio",
                  "Change", "% Change", "Change Type", "% Ownership", "Sector", "Source Type",
                  "Source Date", "Avg Price"]

    df.to_csv(os.path.join(os.getcwd(), "hedge_funds_holdings", "{}.csv".format(fund_name)), index=False)


if __name__ == '__main__':
    preprocess_hedge_funds(r"C:\Users\Acer\Desktop\melvin_capital_management_lp-current-2021-06-23_14_21_47.csv", "melvin_capital")
