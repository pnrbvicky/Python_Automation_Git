import sqlite3
from scripts.merlin_api import upload_single_record_to_merlin


def process_pending_merlin_records(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rowid,
               merlin_order_no,
               merlin_sku,
               merlin_qty,
               merlin_unit_price,
               merlin_total_price,
               merlin_retailer_id,
               merlin_city
        FROM merlin_sales
        WHERE status = 'PENDING'
    """)

    rows = cursor.fetchall()
    print(f"🚀 Processing {len(rows)} pending records")

    for row in rows:
        record_id = row[0]

        #✅ EXACT MERLIN API FORMAT
        record = {
            "merlin_order_no": row[1],
            "merlin_sku": row[2],
            "merlin_qty": row[3],
            "merlin_unit_price": row[4],
            "merlin_total_price": row[5],
            "merlin_retailer_id": row[6],
            "merlin_city": row[7]
        } 

        
        
        

        # ✅ API EXPECTS A LIST
        payload = [record]

        result = upload_single_record_to_merlin(payload)

        if result["status"] == "SUCCESS":
            cursor.execute("""
                UPDATE merlin_sales
                SET status = 'SUCCESS',
                    error_message = NULL
                WHERE rowid = ?
            """, (record_id,))
        else:
            cursor.execute("""
                UPDATE merlin_sales
                SET status = 'FAILED',
                    error_message = ?
                WHERE rowid = ?
            """, (result["error"], record_id))

        conn.commit()

    conn.close()
    print("✅ Merlin upload processing completed")
