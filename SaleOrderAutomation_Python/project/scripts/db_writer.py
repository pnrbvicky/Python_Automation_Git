# import sqlite3

# def write_merlin_to_db(merlin_df, db_path):
#     conn = sqlite3.connect(db_path)

#     merlin_df.to_sql(
#         name="merlin_sales",
#         con=conn,
#         if_exists="append",   # or "replace" for fresh load
#         index=False
#     )

#     conn.close()
#     print("✅ Data written directly to database")

import sqlite3
from datetime import datetime

def write_merlin_to_db(merlin_df, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("Test1")
    # Ensure table exists with control columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS merlin_sales (
            merlin_order_no TEXT,
            merlin_sku TEXT,
            merlin_qty INTEGER,
            merlin_unit_price REAL,
            merlin_total_price REAL,
            merlin_retailer_id TEXT       
            merlin_city TEXT,
            status TEXT,
            error_message TEXT,
            created_at TEXT
        )
    """)

    # Add control columns to dataframe
    print("Test2")
    merlin_df["status"] = "PENDING"
    merlin_df["error_message"] = None
    merlin_df["created_at"] = datetime.now().isoformat()
    print("Test3")

    merlin_df.to_sql(
        name="merlin_sales",
        con=conn,
        if_exists="append",
        index=False
    )
    print("Test4")
    conn.close()
    print("✅ Data written to DB with PENDING status")
