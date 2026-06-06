"""
MSRIT Contineo Auto-Login Script
---------------------------------
Opens Chrome, fills login form (USN + DOB dropdowns), and clicks Login.
Just run it and pick Odd or Even semester — done.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ============================================================
# HARDCODED CREDENTIALS — edit these if your details change
# ============================================================
USN = "1MS23IS049"
DOB_DAY = "22 "    # trailing space matches the portal's option values
DOB_MONTH = "12"   # 12 = December
DOB_YEAR = "2005"

# Portal URLs
URLS = {
    "1": ("Odd Semester", "https://parents.msrit.edu/newparentsodd/index.php"),
    "2": ("Even Semester", "https://parents.msrit.edu/newparents/index.php"),
}


def pick_semester():
    """Simple console prompt — pick 1 or 2, that's it."""
    print("\n  MSRIT Contineo Auto-Login")
    print("  ========================")
    print("  1. Odd Semester")
    print("  2. Even Semester")
    choice = input("\n  Enter 1 or 2: ").strip()
    if choice not in URLS:
        print("  Invalid choice. Exiting.")
        sys.exit(1)
    return URLS[choice]


def login(name, url):
    """Launch Chrome, fill the form, click Login, then exit."""
    print(f"\n  Opening {name} portal...")

    # Chrome setup — fast, no unnecessary flags
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--log-level=3")          # suppress console noise
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    opts.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=opts)

    try:
        driver.get(url)

        # Wait for the login form to be present (max 15s)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.ID, "login-form")))

        # --- Fill USN ---
        usn_field = driver.find_element(By.ID, "username")
        usn_field.clear()
        usn_field.send_keys(USN)

        # --- Select Day dropdown ---
        Select(driver.find_element(By.ID, "dd")).select_by_value(DOB_DAY)

        # --- Select Month dropdown ---
        Select(driver.find_element(By.ID, "mm")).select_by_value(DOB_MONTH)

        # --- Select Year dropdown (this triggers putdate() via onchange) ---
        Select(driver.find_element(By.ID, "yyyy")).select_by_value(DOB_YEAR)

        # Ensure the hidden passwd field is set correctly via JS
        driver.execute_script("putdate();")

        # Small pause for reCAPTCHA to auto-resolve (invisible v3)
        time.sleep(2)

        # --- Click Login ---
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, 'input[type="submit"][value="Login"]'
        )
        submit_btn.click()

        print("  Login submitted! Browser will stay open.")
        print("  This script will now exit.\n")

    except Exception as e:
        print(f"\n  ERROR: {e}")
        print("  The browser is still open — you can try manually.")


if __name__ == "__main__":
    name, url = pick_semester()
    login(name, url)
