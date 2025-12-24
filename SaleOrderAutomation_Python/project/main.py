from scripts.dms_download import download_from_dms
from scripts.file_handler import move_files_to_input
from scripts.file_handler import clear_folder, move_files_to_input,rename_downloaded_files
from config.config import DOWNLOAD_DIR, INPUT_DIR, OUTPUT_DIR
# from scripts.merlin_api import upload_to_merlin
from scripts.db_writer import write_merlin_to_db
from scripts.merlin_uploader import process_pending_merlin_records
import os
from scripts.logger import setup_logger
from scripts.email_notifier import send_execution_mail
from scripts.email_templates import success_mail, failure_mail

# from scripts.transform import read_excel_file,validate_mandatory_columns
# from scripts.transform import merge_customer_city
# from scripts.transform import add_total_price
# from scripts.transform import map_to_merlin_format
# from scripts.transform import clean_merlin_dtypes
from scripts.transform import (
    read_excel_file,
    validate_mandatory_columns,
    merge_customer_city,
    add_total_price,
    map_to_merlin_format,
    clean_merlin_dtypes,
    write_merlin_output,
    prepare_merlin_payload
   
)

def main():
        
    #logging
    LOG_FILE = os.path.join(OUTPUT_DIR, "automation.log")
    logger = setup_logger(__name__, LOG_FILE)
    
    SALES_REQUIRED_COLUMNS = [
    "SO_NO",
    "SKU_ID",
    "QTY",
    "UNIT_PRICE",
    "retailer_id"
]
    CUSTOMER_REQUIRED_COLUMNS = [
    "retailer_id",
    "retailer_name",
    "city"
]
    print("🚀 Automation Started")
    logger.info("Automation Started")

    # STEP 0 – Clean folders
    clear_folder(DOWNLOAD_DIR)
    clear_folder(INPUT_DIR)
    clear_folder(OUTPUT_DIR)
    print(f"cleared download and input folders")
    logger.info(f"cleared download and input folders")

    # create folder if not exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    logger.info("Created folder if not exist for input,output,download path")

    logger.info("Step 1 completed")

    

    download_from_dms()

    
    # ✅ Rename DMS files
    rename_downloaded_files(DOWNLOAD_DIR)
   
    logger.info("Step 2 completed")
    print("Step 2 completed")
    logger.info(f"Raw files are renamed")
    sales_file, customer_file = move_files_to_input()
    logger.info(f"files are moved to input folder")
   
    
    print("Sales Order File:", sales_file)
    print("Customer Master File:", customer_file)
    logger.info("Step 3 completed")
    print("Step 3 completed")
    sales_df = read_excel_file(sales_file)
    customer_df = read_excel_file(customer_file)
    logger.info(f"sales and customer master files read")
    logger.info("Step 4 completed – Files validated and loaded")
    print("Step 4 completed – Files validated and loaded")
    
    print(sales_df)
    print(customer_df)
    
    if sales_df is None or customer_df is None:
     print("One or more files invalid. Stopping automation.")
     logger.info("One or more files invalid. Stopping automation.")
     return

    # Validate columns
    # if not validate_mandatory_columns(sales_df, SALES_REQUIRED_COLUMNS, "Sales Order"):
    #     return

    if not validate_mandatory_columns(customer_df, CUSTOMER_REQUIRED_COLUMNS, "Customer Master"):
        return

    

    sales_df = merge_customer_city(sales_df, customer_df)

    
    print(sales_df)
    print("Step 5 completed – merged sales and customer report")
    logger.info("Step 5 completed – merged sales and customer report")
    sales_df = add_total_price(sales_df)
    print("Step 6 completed – created_total_priceColumn")
    logger.info("Step 6 completed – created_total_priceColumn")
    print(sales_df)

    merlin_df = map_to_merlin_format(sales_df, customer_df)
    print("Step 7 completed – mapped merlin columns")
    logger.info("Step 7 completed – mapped merlin columns")
    print(merlin_df)

    # ✅ Step 4.4 – Clean datatypes
    merlin_df = clean_merlin_dtypes(merlin_df)
    logger.info("Step 8 completed – mapped merlin columns")
    print("Step 8 completed – mapped merlin columns")
    output_file = write_merlin_output(merlin_df, OUTPUT_DIR)
    print("Step 9 completed – Merlin Excel ready")
    logger.info("Step 9 completed – Merlin Excel ready")

    merlin_payload = prepare_merlin_payload(merlin_df)

    print("Step 10 completed – Payload ready for API upload")
    print("Step 10 completed – Payload ready for API upload")
    print(merlin_payload)

    # upload_response = upload_to_merlin(merlin_payload)

    print("Step 11 completed – Data uploaded to Merlin")
    logger.info("Step 11 completed – Data uploaded to Merlin")

    db_path = os.path.join(OUTPUT_DIR, "merlin.db")
 
    write_merlin_to_db(merlin_df, db_path)    
    print("Data written to DB (PENDING)")
    logger.info("Data written to DB (PENDING)")
    process_pending_merlin_records(db_path)
    print("Step 12 completed – DB API DB status updated")
    logger.info("Step 12 completed – DB API DB status updated")
    # # #email:
    # try:
    #     print("Email bot started")
    #     logger.info("Email bot started")
        
    #     subject, body = success_mail()
    #     send_execution_mail(
    #         subject,
    #         body,
    #         attachments=[
    #             "input/sales_order.xlsx",
    #             "input/customer_master.xlsx",
    #             "output/automation.log"
    #         ]
            
    #     )

    # except Exception as e:
    #     subject, body = failure_mail(str(e))
    #     send_execution_mail(
    #         subject,
    #         body,
    #         attachments=["output/automation.log"]
    #     )
    #     raise
    
if __name__ == "__main__":
    main()