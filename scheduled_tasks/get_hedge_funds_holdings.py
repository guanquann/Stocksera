import os
import pandas as pd


def preprocess_hedge_funds(csv, fund_name):
    """
    Get hedge funds holding from their 13F filling. Data is from https://whalewisdom.com/.
    You need to sign up a free account to access the csv files. Data is updated quarterly.
    Parameters
    ----------
    csv: str
        csv file path
    fund_name: str
        name of the csv file you want to save.
        I would advice you to name it the same as the names inside scheduled_tasks/hedge_funds_description.json.
    """
    df = pd.read_csv(csv)
    df.fillna("N/A", inplace=True)
    df = df.apply(lambda x: x.astype(str).str.upper())
    del df["Qtr first owned"]
    del df["Recent Price"]
    del df["Ranking"]
    df = df[df["source_type"] == "13F"]
    df.index = df.index + 1
    df = df.reset_index()

    df.columns = ["Rank", "Stock", "Ticker", "Type", "Quantity", "Market Value", "% Portfolio", "Previous % Portfolio",
                  "Change", "% Change", "Change Type", "% Ownership", "Sector", "Source Type",
                  "Source Date", "Avg Price"]

    df.to_csv(os.path.join("../database", "hedge_funds_holdings", "{}.csv".format(fund_name)), index=False)


if __name__ == '__main__':
    preprocess_hedge_funds(r"C:\Users\Acer\PycharmProjects\StocksAnalysis\database\new\sanders_capital__llc-current-2021-08-18_03_03_12.csv", "sanders_capital")
