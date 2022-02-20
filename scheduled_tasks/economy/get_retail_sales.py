import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scheduled_tasks.economy.ychart_connection import ychart_data
from helpers import connect_mysql_database

cnx, engine = connect_mysql_database()
cur = cnx.cursor()


def retail_sales():
    """
    Get retail sales and compare it with avg monthly covid cases
    """

    url = "https://ycharts.com/indicators/us_retail_and_food_services_sales"
    df = ychart_data(url)

    combined_df = df[6][::-1].append(df[5][::-1])

    combined_df["Value"] = combined_df["Value"].str.replace("B", "")
    combined_df["Value"] = combined_df["Value"].astype(float)

    combined_df["Percent Change"] = combined_df["Value"].shift(1)
    combined_df["Percent Change"] = combined_df["Percent Change"].astype(float)
    combined_df["Percent Change"] = 100 * (combined_df["Value"] - combined_df["Percent Change"]) / \
                                    combined_df["Percent Change"]
    combined_df["Percent Change"] = combined_df["Percent Change"].round(2)

    combined_df["Date"] = combined_df["Date"].astype('datetime64[ns]').astype(str)

    covid_df = pd.read_csv(r'https://covid.ourworldindata.org/data/owid-covid-data.csv')
    usa_df = covid_df[covid_df["iso_code"] == "USA"]
    usa_df.index = pd.to_datetime(usa_df["date"], errors='coerce')
    usa_df = usa_df.groupby(pd.Grouper(freq="M"))
    usa_df = usa_df.mean()["new_cases"]
    usa_df = pd.DataFrame(usa_df)
    usa_df["new_cases"] = usa_df["new_cases"].round(2)
    usa_df.reset_index(inplace=True)
    usa_df["date"] = usa_df["date"].astype(str)
    usa_df.rename(columns={"date": "Date"}, inplace=True)
    combined_df = pd.merge(combined_df, usa_df, how='left', on='Date')
    combined_df.fillna(0, inplace=True)
    print(combined_df)
    for index, row in combined_df.iterrows():
        cur.execute("INSERT IGNORE INTO retail_sales VALUES (%s, %s, %s, %s)", (row[0], row[1], row[2], row[3]))
        cnx.commit()


if __name__ == '__main__':
    retail_sales()
