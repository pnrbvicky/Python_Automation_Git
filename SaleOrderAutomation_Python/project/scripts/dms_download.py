import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import *

def download_from_dms():
    print("🚀 Automation Started - Downloading file...")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Selenium Manager automatically downloads correct ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(LOGIN_URL)

        # --- LOGIN ---
        try:
            username_input = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(USERNAME)
            time.sleep(1)

            password_input = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(PASSWORD)
            time.sleep(1)

            # Click login button
            login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()

            print("✅ Logged in successfully!")

        except TimeoutException:
            print("❌ Login fields not found! Check HTML or selectors.")
            return

        time.sleep(2)  # wait for page to load after login

        # --- DOWNLOAD SALES ORDER ---
        try:
            download_sales = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Download Sales Order"]'))
            )
            download_sales.click()
            print("✅ Sales Order downloaded")
        except TimeoutException:
            print("❌ Download Sales Order button not found!")

        # --- DOWNLOAD CUSTOMER MASTER ---
        try:
            download_customer = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Download Customer Master"]'))
            )
            download_customer.click()
            print("✅ Customer Master downloaded")
        except TimeoutException:
            print("❌ Download Customer Master button not found!")

        # Optional: wait for files to complete download
        time.sleep(5)

    finally:
        driver.quit()
