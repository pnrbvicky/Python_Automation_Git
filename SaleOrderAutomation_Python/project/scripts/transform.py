import os
import pandas as pd

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