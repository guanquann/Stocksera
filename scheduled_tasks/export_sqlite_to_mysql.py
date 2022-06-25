import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from helpers import connect_mysql_database

cnx, cur, engine = connect_mysql_database()

PATH = r"C:\Users\Acer\Desktop\test"

for file in os.listdir(PATH):
    df = pd.read_csv(os.path.join(PATH, file))
    df.fillna("", inplace=True)
    cur.execute("SELECT count(*) FROM information_schema.columns WHERE table_name = '{}'".format(file.split(".")[0]))
    num_col = cur.fetchone()[0]
    print(file, len(df.columns), num_col)
    if len(df.columns) == num_col:
        start = 0
        while start < len(df):
            cur.executemany("INSERT IGNORE INTO {} VALUES ({})".format(file.split(".")[0], str("%s, "*num_col)[:-2]),
                            df[start:start+50000].values.tolist())
            cnx.commit()
            start += 50000
