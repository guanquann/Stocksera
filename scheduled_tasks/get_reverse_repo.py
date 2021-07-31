import sqlite3
import pandas as pd

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

# x = "https://websvcgatewayx2.frbny.org/autorates_tomo_external/services/v1_0/tomo/retrieveHistoricalExcel?f=01022014&t=07282021&ctt=true&&cta=true&ctm=true"
x = r"C:\Users\Acer\Desktop\tomo-01022014-07282021.xls"

df = pd.read_excel(x)
df = df[df["Op Type"] == "RRP"]
df["Deal Date"] = df["Deal Date"].str.replace("/", "-")
df["Average"] = df["Total-Submit"].astype(float) / df["Participating Counterparties"].astype(float)
df["Average"] = df["Average"].round(2)
df.fillna(0, inplace=True)
for index, row in df[::-1].iterrows():
    date = row["Deal Date"]
    amount = row["Total-Submit"]
    participants = row["Participating Counterparties"]
    avg = row["Average"]
    db.execute("INSERT INTO reverse_repo VALUES (?, ?, ?, ?)", (date, amount, participants, avg))
    conn.commit()
