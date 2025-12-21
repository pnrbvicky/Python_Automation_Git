import sqlite3

def write_merlin_to_db(merlin_df, db_path):
    conn = sqlite3.connect(db_path)

    merlin_df.to_sql(
        name="merlin_sales",
        con=conn,
        if_exists="append",   # or "replace" for fresh load
        index=False
    )

    conn.close()
    print("✅ Data written directly to database")
