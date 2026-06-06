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
        print("  Login clicked. Waiting for dashboard to load...")

        # --- Wait & Close Announcement Popup ---
        # Check for the popup and close button periodically for up to 10 seconds (every 0.2s)
        popup_closed = False
        start_time = time.time()
        
        while time.time() - start_time < 10:
            # Check if login failed (so we don't wait for a popup that won't show)
            try:
                errs = driver.find_elements(By.XPATH, "//*[contains(text(), 'Login Failed') or contains(text(), 'invalid')]")
                if len(errs) > 0 and any(e.is_displayed() for e in errs):
                    print("  [Notice] Login seems to have failed. Please check your credentials.")
                    break
            except Exception:
                pass

            # Highly targeted selectors based on the attendance modal's HTML structure
            selectors = [
                # 1. Specific to the attendance modal dialog and its Close button
                (By.CSS_SELECTOR, ".cn-att-modal button.uk-modal-close"),
                (By.CSS_SELECTOR, ".cn-att-modal .uk-modal-close"),
                
                # 2. Any button inside the modal dialog with text "Close" (matching the exact case "Close" in HTML)
                (By.XPATH, "//*[contains(@class, 'uk-modal-dialog')]//button[normalize-space(text())='Close']"),
                (By.XPATH, "//*[contains(@class, 'uk-modal-dialog')]//button[translate(normalize-space(text()), 'close', 'CLOSE')='CLOSE']"),
                
                # 3. Any button with class uk-modal-close and exact text "Close" (with leading/trailing space handled)
                (By.XPATH, "//button[contains(@class, 'uk-modal-close') and normalize-space(text())='Close']"),
                
                # 4. Fallback selectors
                (By.CSS_SELECTOR, ".uk-modal-close"),
                (By.CSS_SELECTOR, ".uk-modal-close-default"),
                (By.XPATH, "//button[translate(normalize-space(text()), 'close', 'CLOSE')='CLOSE']")
            ]
            
            for by, selector in selectors:
                try:
                    elements = driver.find_elements(by, selector)
                    for el in elements:
                        if el.is_displayed():
                            # Attempt normal click, fall back to JS click if intercepted
                            try:
                                el.click()
                            except Exception:
                                driver.execute_script("arguments[0].click();", el)
                            
                            print("  Successfully closed the announcement popup!")
                            popup_closed = True
                            break
                except Exception:
                    pass
                if popup_closed:
                    break
            
            if popup_closed:
                break
                
            time.sleep(0.2)

        if not popup_closed:
            print("  No active popup detected (it may have been closed or did not appear).")

        print("  Finished! You can now use the browser.\n")

    except Exception as e:
        print(f"\n  ERROR: {e}")
        print("  The browser is still open — you can try manually.")


if __name__ == "__main__":
    name, url = pick_semester()
    login(name, url)
