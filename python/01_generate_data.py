import numpy as np
import pandas as pd
from pathlib import Path

Path("data/raw").mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(42)

products = pd.DataFrame([
    ("Technology", "Phones", "Smartphone X1", 30000, 0.15),
    ("Technology", "Phones", "Smartphone Lite", 15000, 0.15),
    ("Technology", "Accessories", "Wireless Mouse", 600, 0.30),
    ("Technology", "Accessories", "USB Keyboard", 1200, 0.30),
    ("Technology", "Copiers", "Office Copier", 45000, 0.28),
    ("Furniture", "Chairs", "Ergonomic Chair", 8000, 0.10),
    ("Furniture", "Tables", "Conference Table", 20000, 0.04),
    ("Furniture", "Bookcases", "Wooden Bookcase", 9000, 0.03),
    ("Furniture", "Furnishings", "Desk Lamp", 1500, 0.25),
    ("Office Supplies", "Paper", "A4 Paper Pack", 400, 0.40),
    ("Office Supplies", "Binders", "Heavy Binder", 250, 0.30),
    ("Office Supplies", "Storage", "Storage Box", 900, 0.22),
    ("Office Supplies", "Art", "Marker Set", 300, 0.35),
], columns=["Category", "Sub-Category", "Product Name", "Price", "Margin"])

geo = {
    "South": ["Karnataka", "Tamil Nadu", "Andhra Pradesh", "Telangana", "Kerala"],
    "West": ["Maharashtra", "Gujarat", "Rajasthan"],
    "North": ["Delhi", "Punjab", "Uttar Pradesh"],
    "East": ["West Bengal", "Odisha", "Bihar"],
}
state_to_region = {s: r for r, states in geo.items() for s in states}
states = list(state_to_region.keys())

first = ["Aarav", "Diya", "Rohan", "Sneha", "Kiran", "Meera", "Arjun", "Priya",
         "Vikram", "Ananya", "Suresh", "Lakshmi", "Rahul", "Divya", "Manoj"]
last = ["Reddy", "Sharma", "Naidu", "Iyer", "Patel", "Das", "Gupta", "Rao",
        "Singh", "Kumar", "Nair", "Joshi"]
names = [f"{f} {l}" for f in first for l in last]
cust_names = rng.choice(names, 150, replace=False)
customers = pd.DataFrame({
    "Customer ID": [f"CU-{i:04d}" for i in range(1, 151)],
    "Customer Name": cust_names,
    "Segment": rng.choice(["Consumer", "Corporate", "Home Office"], 150, p=[0.5, 0.3, 0.2]),
})

days = pd.date_range("2022-01-01", "2025-12-31")
weights = np.where(days.month >= 10, 1.6, 1.0)
weights = weights / weights.sum()

rows = []
for i in range(2000):
    order_date = rng.choice(days, p=weights)
    cust = customers.iloc[rng.integers(0, len(customers))]
    state = rng.choice(states)
    ship_mode = rng.choice(["Standard Class", "Second Class", "First Class", "Same Day"],
                           p=[0.6, 0.2, 0.15, 0.05])
    ship_date = pd.Timestamp(order_date) + pd.Timedelta(days=int(rng.integers(1, 8)))
    for _ in range(int(rng.integers(1, 5))):
        p = products.iloc[rng.integers(0, len(products))]
        qty = int(rng.integers(1, 6))
        discount = float(rng.choice([0, 0.1, 0.2, 0.3, 0.4], p=[0.45, 0.2, 0.15, 0.12, 0.08]))
        sales = p["Price"] * qty * (1 - discount) * rng.uniform(0.95, 1.05)
        profit = sales * (p["Margin"] - 0.5 * discount) + rng.normal(0, sales * 0.01)
        rows.append({
            "Order ID": f"IN-{pd.Timestamp(order_date).year}-{i+1:05d}",
            "Order Date": pd.Timestamp(order_date).date(),
            "Ship Date": ship_date.date(),
            "Ship Mode": ship_mode,
            "Customer ID": cust["Customer ID"],
            "Customer Name": cust["Customer Name"],
            "Segment": cust["Segment"],
            "Country": "India",
            "State": state,
            "Region": state_to_region[state],
            "Category": p["Category"],
            "Sub-Category": p["Sub-Category"],
            "Product Name": p["Product Name"],
            "Sales": round(sales, 2),
            "Quantity": qty,
            "Discount": discount,
            "Profit": round(profit, 2),
        })

df = pd.DataFrame(rows)

dup = df.sample(30, random_state=1)
df = pd.concat([df, dup], ignore_index=True)
df.insert(0, "Row ID", range(1, len(df) + 1))

df.loc[df.sample(20, random_state=2).index, "Segment"] = np.nan
idx = df.sample(25, random_state=3).index
df.loc[idx, "Region"] = df.loc[idx, "Region"].str.lower() + " "

df.to_csv("data/raw/superstore.csv", index=False)
print("Saved!", df.shape) 