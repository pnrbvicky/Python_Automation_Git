import pandas as pd
import os

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

# -------- Sales Order Data --------
sales_data = {
    "SO_NO": ["SO1001", "SO1002", "SO1003"],
    "SKU_ID": ["SKU01", "SKU02", "SKU03"],
    "QTY": [2, 1, 5],
    "UNIT_PRICE": [500, 1200, 150],
    "retailer_id": ["R002", "R001", "R002"]
}




sales_df = pd.DataFrame(sales_data)
sales_df.to_excel("reports/sales_order.xlsx", index=False)

# -------- Customer Master Data --------
customer_data = {
    "retailer_id": ["R001", "R002"],
    "retailer_name": ["ABC Stores", "XYZ Mart"],
    "city": ["Chennai", "Bangalore"]
}


customer_df = pd.DataFrame(customer_data)
customer_df.to_excel("reports/customer_master.xlsx", index=False)

print("Reports created successfully")
