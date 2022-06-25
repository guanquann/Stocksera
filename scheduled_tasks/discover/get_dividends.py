import os
import sys
import yaml
import requests
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()

with open("config.yaml") as config_file:
    config_keys = yaml.load(config_file, Loader=yaml.Loader)


def main():
    url = f"https://api.polygon.io/v3/reference/dividends?limit=1000&apiKey={config_keys['POLYGON_KEY']}"
    df = pd.DataFrame(requests.get(url).json()["results"])
    df = df[["ticker", "cash_amount", "declaration_date", "ex_dividend_date", "pay_date", "record_date",
             "dividend_type", "frequency"]]
    print(df)
    cur.executemany("INSERT IGNORE INTO dividends VALUES (%s ,%s ,%s ,%s, %s ,%s ,%s ,%s)", df.values.tolist())
    cnx.commit()


if __name__ == '__main__':
    main()
