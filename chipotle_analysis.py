#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.request
urllib.request.urlretrieve(https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv, "chipotle.tsv")


# In[ ]:


import csv
with open("chipotle.tsv")


# In[23]:


import urllib.request
import csv
from collections import defaultdict

URL = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv"

def download_data(URL, path):
    try:
        urllib.request.urlretrieve(URL,path)
        print(f"Download to {path}")
    except Exception as e:
        print(f"Download Failed: {e}")

def load_rows(path):
    rows=[]
    with open(path, "r", encoding="utf-8") as f:
        reader=csv.DictReader(f, delimiter="\t")
        for row in reader:
            quantity=int(row["quantity"])
            price=float(row["item_price"].replace("$","").strip())
            row["item_price"]=price
            row["quantity"]=quantity
            rows.append(row)
    return rows

def analyze(rows):
    order_ids=set()
    item_quantity=defaultdict(int)
    total_revenue=0
    items_10=set()

    for row in rows:
        order_ids.add(row["order_id"])
        item_quantity[row["item_name"]]+=row["quantity"]
        row_total=row["item_price"]*row["quantity"]
        total_revenue+=row_total
        if (row["item_price"]/row["quantity"])>10:
            items_10.add(row["item_name"])

    sorted_items=sorted(item_quantity.items(), key=lambda x: x[1], reverse=True)
    unique_order_count = len(order_ids)
    avg_revenue_per_order = round(total_revenue / unique_order_count, 2)

    return {
    "unique_orders": len(order_ids),
    "top_5_items": sorted_items[:5],
    "avg_revenue_per_order": avg_revenue_per_order,
    "expensive_items": items_10,
}

def write_summary(rows, out_path):
    # build per-item totals
    item_quantities = defaultdict(int)
    item_revenues = defaultdict(float)
    for row in rows:
        item_quantities[row["item_name"]] += row["quantity"]
        item_revenues[row["item_name"]] += row["item_price"] * row["quantity"]

    summary_rows = []
    for item in item_quantities:
        summary_rows.append({
            "item_name": item,
            "total_quantity": item_quantities[item],
            "total_revenue": round(item_revenues[item], 2),
        })

    # sort descending by revenue
    summary_rows.sort(key=lambda r: r["total_revenue"], reverse=True)

    # write to CSV
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["item_name", "total_quantity", "total_revenue"])
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Summary written to {out_path}")


# verify by reading back the first 10 rows
def main():
    download_data(URL, "chipotle.tsv")
    rows = load_rows("chipotle.tsv")
    results = analyze(rows)

    print(f"Unique orders: {results['unique_orders']}")
    print(f"Avg revenue per order: ${results['avg_revenue_per_order']}")
    print("\nTop 5 items by quantity:")
    for item, qty in results['top_5_items']:
        print(f"  {item}: {qty}")
    print(f"\nItems with unit price > $10:")
    for item in sorted(results['expensive_items']):
        print(f"  {item}")

    write_summary(rows, "chipotle_summary.csv")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




