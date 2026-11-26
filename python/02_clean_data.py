import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw/superstore.csv")

df.columns = (df.columns.str.strip().str.lower()
              .str.replace(" ", "_").str.replace("-", "_"))

df["region"] = df["region"].str.strip().str.title()

seg_map = df.dropna(subset=["segment"]).groupby("customer_id")["segment"].first()
df["segment"] = df["segment"].fillna(df["customer_id"].map(seg_map)).fillna("Unknown")

before = len(df)
df = df.drop_duplicates(subset=[c for c in df.columns if c != "row_id"])
print("Duplicates removed:", before - len(df))

df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")
df["profit_margin"] = (df["profit"] / df["sales"]).round(4)
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days

Path("data/clean").mkdir(parents=True, exist_ok=True)
df.to_csv("data/clean/superstore_clean.csv", index=False)
print("Missing values left:", int(df.isnull().sum().sum()))
print(df["region"].value_counts())
print("Clean data saved:", df.shape) 