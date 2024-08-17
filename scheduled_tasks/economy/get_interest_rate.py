import os
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()


def interest_rate():
    """
    Get retail sales and compare it with avg monthly covid cases
    """
    print("Getting Interest Rate...")

    current_date_time = str(datetime.utcnow().date())
    url = (
        "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20"
        "sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&"
        "width=718&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FEDFUNDS&scale="
        f"left&cosd=1954-07-01&coed={current_date_time}&line_color=%234572a7&link_values=false&line_style="
        f"solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&"
        f"fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={current_date_time}&"
        f"revision_date={current_date_time}&nd=1954-07-01"
    )
    df = pd.read_csv(url)

    cur.executemany(
        "INSERT IGNORE INTO interest_rates VALUES (%s, %s)", df.values.tolist()
    )

    print("Interest Rate Successfully Completed...\n")


if __name__ == "__main__":
    interest_rate()
