# MSRIT Contineo Auto-Login

A fast, lightweight Python script using Selenium that automates logging into the MSRIT Contineo parent portal (Odd or Even semester). 

It fills in the USN and Date of Birth dropdowns, triggers the login, automatically dismisses the post-login announcement dialog, and leaves Chrome open with your session ready.

---

## 📁 Repository Structure

```text
WEBOPENER/
├── msrit_login.py      # Main Selenium automation script (contains USN & DOB)
├── run_bot.bat         # Launcher batch file executed by the Desktop shortcut
├── setup.bat           # One-click installation & shortcut setup script (self-deletes)
└── README.md           # Documentation
```

---

## ⚡ Installation & Setup

1. **Prerequisites**: Ensure you have [Python 3](https://www.python.org/downloads/) installed. During installation, make sure to check the box **"Add Python to PATH"**.
2. **Clone / Download** this repository to your machine.
3. **Configure Credentials**: Open [msrit_login.py](file:///c:/Users/kssha/Documents/WEBOPENER/msrit_login.py) in any text editor and verify/update your USN and Date of Birth at the top of the file:
   ```python
   USN = "1MS23AI049"
   DOB_DAY = "14 "    # Note the trailing space (e.g. "13 " or "05 ")
   DOB_MONTH = "08"   # Month as a number string (e.g. "12" for Dec, "04" for Apr)
   DOB_YEAR = "2009"  # Year string
   ```
4. **Run Setup**: Double-click [setup.bat](file:///c:/Users/kssha/Documents/WEBOPENER/setup.bat). This will:
   * Install `selenium` automatically.
   * Create a desktop shortcut named **`MSRIT Auto-Login`**.
   * Automatically delete the [setup.bat](file:///c:/Users/kssha/Documents/WEBOPENER/setup.bat) file once it completes.

---

## 🚀 How to Run

1. Double-click the **`MSRIT Auto-Login`** shortcut on your Desktop.
2. Select **`1`** for the **Odd Semester** portal or **`2`** for the **Even Semester** portal and press **Enter**.
3. Chrome will launch automatically, fill in the details, log you in, close the notice banner, and hand control over to you!
