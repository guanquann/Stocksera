import pandas as pd

df = pd.read_json("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json")
for i in ["transaction_date", "disclosure_date"]:
    df[i] = pd.to_datetime(df[i], errors='coerce')
    df[i] = df[i].dt.strftime('%Y-%m-%d')
df.to_csv("database/government/house.csv", index=False)
