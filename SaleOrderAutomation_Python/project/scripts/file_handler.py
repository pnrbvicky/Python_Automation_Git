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
