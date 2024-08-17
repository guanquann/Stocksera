import os
import sys
import requests
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from helpers import connect_mysql_database, header

cnx, cur, engine = connect_mysql_database()


def main():
    """
    Get Jim Cramer Stock Picks
    """
    print("Getting Jim Cramer Stock Picks...")

    response = requests.get(
        "https://www.quiverquant.com/cramertracker/", headers=header
    )

    if response.status_code == 200:
        df = pd.read_html(response.text)[0]
        df.to_sql("jim_cramer", engine, if_exists="replace", index=False)

    print("Jim Cramer Stock Picks Successfully Completed...\n")


if __name__ == "__main__":
    main()
