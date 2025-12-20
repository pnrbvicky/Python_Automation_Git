import os
import pandas as pd
from datetime import datetime

def read_excel_file(file_path):
    print(f"🔍 Checking file: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError("❌ Input file not found")

    if os.path.getsize(file_path) == 0:
        raise ValueError("❌ Input file is empty (0 KB)")

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"❌ Failed to read Excel: {e}")

    if df.empty:
        raise ValueError("❌ Excel file has no data rows")

    print(f"✅ File loaded successfully ({len(df)} rows)")
    return df

def validate_mandatory_columns(df, required_columns, file_name):
    missing_columns = []

    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)

    if missing_columns:
        print(f"❌ Missing mandatory columns in {file_name}: {missing_columns}")
        return False

    print(f"✅ All mandatory columns present in {file_name}")
    return True

def merge_customer_city(sales_df, customer_df):
    """
    Merge city from customer master into sales data using retailer_id
    """

    merged_df = sales_df.merge(
        customer_df[["retailer_id", "city"]],
        on="retailer_id",
        how="left"
    )

    # Validation: city should not be missing
    if merged_df["city"].isnull().any():
        raise ValueError("❌ City missing for some retailer_id")

    print("✅ Customer city merged successfully")

    return merged_df

def add_total_price(df):
    """
    Create total_price = QTY * UNIT_PRICE
    """

    df["total_price"] = df["QTY"] * df["UNIT_PRICE"]

    # Validation
    if (df["total_price"] < 0).any():
        raise ValueError("❌ total_price has negative values")

    print("✅ total_price column created")

    return df

def map_to_merlin_format(sales_df, customer_df):
    """
    Map raw sales + customer data into Merlin upload format
    """

    merlin_df = sales_df.copy()

    # 🔹 Column mapping dictionary
    column_mapping = {
        "SO_NO": "merlin_order_no",
        "SKU_ID": "merlin_sku",
        "QTY": "merlin_qty",
        "UNIT_PRICE": "merlin_unit_price",
        "retailer_id": "merlin_retailer_id",
        "total_price": "merlin_total_price",
        "city": "merlin_city"
    }

    # Rename columns
    merlin_df.rename(columns=column_mapping, inplace=True)

    # # 🔹 VLOOKUP equivalent → add city
    # merlin_df = merlin_df.merge(
    #     customer_df[["retailer_id", "city"]],
    #     on="retailer_id",
    #     how="left"
    # )

    # # Rename city to Merlin format
    # merlin_df.rename(columns={"city": "merlin_city"}, inplace=True)

    print("✅ Mapped data to Merlin format")

    return merlin_df

def clean_merlin_dtypes(df):
    """
    Ensure correct datatypes for Merlin upload
    """

    df["merlin_qty"] = df["merlin_qty"].astype(int)
    df["merlin_unit_price"] = df["merlin_unit_price"].astype(float)
    df["merlin_total_price"] = df["merlin_total_price"].astype(float)

    df["merlin_order_no"] = df["merlin_order_no"].astype(str)
    df["merlin_city"] = df["merlin_city"].astype(str)

    print("✅ Merlin datatypes cleaned")

    return df



def write_merlin_output(merlin_df, output_dir):
    """
    Write Merlin formatted DataFrame to Excel
    """

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"merlin_upload_{timestamp}.xlsx")

    # output_file = os.path.join(output_dir, "merlin_upload.xlsx")

    try:
        merlin_df.to_excel(
            output_file,
            index=False,
            engine="openpyxl"
        )
    except Exception as e:
        raise RuntimeError(f"❌ Failed to write Merlin Excel file: {e}")

    print(f"✅ Merlin output written to: {output_file}")

    return output_file

def prepare_merlin_payload(merlin_df):
    """
    Convert merlin DataFrame into API-ready JSON payload
    """

    if merlin_df.empty:
        raise ValueError("❌ Merlin DataFrame is empty")

    # Replace NaN with None for JSON compatibility
    merlin_df = merlin_df.where(pd.notnull(merlin_df), None)

    payload = merlin_df.to_dict(orient="records")

    if not payload:
        raise ValueError("❌ Payload is empty after conversion")

    print(f"✅ Merlin payload prepared ({len(payload)} records)")

    return payload


