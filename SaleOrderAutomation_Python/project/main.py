from scripts.dms_download import download_from_dms
from scripts.file_handler import move_files_to_input
from scripts.file_handler import clear_folder, move_files_to_input,rename_downloaded_files
from config.config import DOWNLOAD_DIR, INPUT_DIR, OUTPUT_DIR
from scripts.merlin_api import upload_to_merlin
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

    # STEP 0 – Clean folders
    clear_folder(DOWNLOAD_DIR)
    clear_folder(INPUT_DIR)
    clear_folder(OUTPUT_DIR)
    print(f"cleared download and input folders")

    download_from_dms()

    print("✅ Step 1 completed")
    # ✅ Rename DMS files
    rename_downloaded_files(DOWNLOAD_DIR)
    print("✅ Step 1.1 completed")
    print(f"Raw files are renamed")
    sales_file, customer_file = move_files_to_input()

    print("✅ Step 2 completed")
    print("Sales Order File:", sales_file)
    print("Customer Master File:", customer_file)

    sales_df = read_excel_file(sales_file)
    customer_df = read_excel_file(customer_file)
    print("✅ Step 3.1 completed – Files validated and loaded")
    print(sales_df)
    print(customer_df)

    if sales_df is None or customer_df is None:
     print("❌ One or more files invalid. Stopping automation.")
     return

    # Validate columns
    # if not validate_mandatory_columns(sales_df, SALES_REQUIRED_COLUMNS, "Sales Order"):
    #     return

    if not validate_mandatory_columns(customer_df, CUSTOMER_REQUIRED_COLUMNS, "Customer Master"):
        return

    print("✅ Step 3 completed – Files validated")

    sales_df = merge_customer_city(sales_df, customer_df)

    print("✅ Step 4.1 completed – merged sales and customer report")
    print(sales_df)
    
    sales_df = add_total_price(sales_df)
    print("✅ Step 4.2 completed – created_total_priceColumn")
    print(sales_df)

    merlin_df = map_to_merlin_format(sales_df, customer_df)
    print("✅ Step 4.3 completed – mapped merlin columns")
    print(merlin_df)

    # ✅ Step 4.4 – Clean datatypes
    merlin_df = clean_merlin_dtypes(merlin_df)

    output_file = write_merlin_output(merlin_df, OUTPUT_DIR)
    print("✅ Step 4 completed – Merlin Excel ready")

    merlin_payload = prepare_merlin_payload(merlin_df)

    print("✅ Step 5 completed – Payload ready for API upload")
    print(merlin_payload)

    upload_response = upload_to_merlin(merlin_payload)

    print("✅ Step 7 completed – Data uploaded to Merlin")
    # Step 4 → transform
    # Step 5 → API upload
    # Step 6 → email

if __name__ == "__main__":
    main()