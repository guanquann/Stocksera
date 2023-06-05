import os
import sys
import requests
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def main():
    print("Getting CNN fear and greed...")

    data = requests.get("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", 
                        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}).json()

    df = pd.DataFrame(data["fear_and_greed_historical"]["data"])
    df["x"] = df["x"].apply(lambda x: str(datetime.fromtimestamp(int(str(x)[:-5]))).split()[0])
    df["rating"] = df["rating"].str.title()
    
    cur.executemany("INSERT IGNORE INTO fear_and_greed VALUES (%s, %s, %s)", df.values.tolist())

    print("CNN fear and greed Successfully Completed...\n")


if __name__ == '__main__':
    main()
