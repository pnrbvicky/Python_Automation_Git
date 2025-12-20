import os
import time
import shutil
from config.config import DOWNLOAD_DIR, INPUT_DIR

def clear_folder(folder_path):
    if not os.path.exists(folder_path):
        return

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"🧹 Deleted: {file}")
        except Exception as e:
            print(f"❌ Failed to delete {file}: {e}")

def wait_for_downloads(timeout=30):
    """Wait until Chrome finishes downloading files"""
    end_time = time.time() + timeout

    while time.time() < end_time:
        files = os.listdir(DOWNLOAD_DIR)

        # Ignore .crdownload (incomplete downloads)
        if files and not any(f.endswith(".crdownload") for f in files):
            return files

        time.sleep(1)

    raise TimeoutError("Download did not complete in time")


def move_files_to_input():
    os.makedirs(INPUT_DIR, exist_ok=True)

    files = wait_for_downloads()

    sales_order_file = None
    customer_master_file = None

    for file in files:
        src = os.path.join(DOWNLOAD_DIR, file)
        dest = os.path.join(INPUT_DIR, file)

        if "sales" in file.lower():
            sales_order_file = dest
        elif "customer" in file.lower():
            customer_master_file = dest

        shutil.move(src, dest)
        print(f"📦 Moved file: {file}")

    return sales_order_file, customer_master_file

def rename_downloaded_files(download_dir):
    """
    Rename DMS downloaded files to standard names
    """

    files = os.listdir(download_dir)

    if not files:
        raise FileNotFoundError("❌ No files found in download folder")

    sales_file = None
    customer_file = None

    for file in files:
        lower_name = file.lower()

        if "sales" in lower_name:
            sales_file = file
        elif "customer" in lower_name:
            customer_file = file

    if not sales_file or not customer_file:
        raise ValueError("❌ Could not identify Sales or Customer file")

    sales_new = "sales_order.xlsx"
    customer_new = "customer_master.xlsx"

    os.rename(
        os.path.join(download_dir, sales_file),
        os.path.join(download_dir, sales_new)
    )

    os.rename(
        os.path.join(download_dir, customer_file),
        os.path.join(download_dir, customer_new)
    )

    print("✅ Downloaded files renamed successfully")

    return sales_new, customer_new
