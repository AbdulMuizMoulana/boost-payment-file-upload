# 🚀 Boost Payment File Upload Automation

Automated end-to-end testing framework for **Boost Payment File Upload & Gateway Update workflows** using **Pytest + Selenium**.

This project validates:

* Merchant Gateway updates (Airwallex)
* File upload process
* Excel-driven payment data
* Total validation between Excel and UI
* Multi-environment execution (DEV / UAT)
* Headless browser support
* Rich HTML reporting with screenshots

---

## 🧰 Tech Stack

* Python 3.10+
* Pytest
* Selenium WebDriver
* Pandas
* OpenPyXL / XLWings
* WebDriver Manager
* Pytest-HTML Reports
* Pytest-xdist (parallel execution)
* dotenv for environment config

---

## 📂 Project Structure

```
FileUploadAutomation/
│
├── .github/                 # CI workflows (GitHub Actions)
├── configurations/          # Environment & config files
├── locators/                # Page element locators
├── logs/                    # Execution logs
├── pages/                   # Page Object Model classes
├── Reports/                 # Generated HTML reports
├── screenshots/             # Failure screenshots
├── test_data/               # Excel test files
├── tests/                   # Test cases
├── utilities/               # Helper utilities (Excel, logging, etc.)
│
├── .env                     # Environment variables
├── conftest.py              # Fixtures & driver setup
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Dependencies
├── run.bat                  # Windows run script
└── README.md
```

---

## ⚙️ Features

✔ Page Object Model (POM) design
✔ Data-driven testing using Excel
✔ Automatic Excel updates (once per day)
✔ Gateway update automation
✔ File upload validation
✔ Total amount verification
✔ Screenshot capture on failure
✔ Dark-theme HTML reports with charts
✔ Parallel execution support
✔ CI/CD ready

---

## 🧪 Supported Environments

* DEV
* UAT
* ALL (run both)

Select environment via CLI.

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/AbdulMuizMoulana/boost-payment-file-upload.git
cd boost-payment-file-upload
```

---

### 2️⃣ Create virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Tests

### Run all tests (default Chrome)

```bash
pytest
```

---

### Run with specific browser

```bash
pytest --browser chrome
pytest --browser firefox
pytest --browser edge
pytest --browser safari
```

---

### Run in headless mode

```bash
pytest --headless
```

Or using environment variable:

```bash
set HEADLESS=true
pytest
```

---

### Run for specific environment

```bash
pytest --env dev
pytest --env uat
pytest --env all
```

---

### Parallel execution

```bash
pytest -n 4
```

---

## 📊 Test Reports

HTML reports are generated automatically:

```
Reports/<ENV>/Boost_FileUpload_Report_<ENV>_<timestamp>.html
```

Report includes:

* Test summary
* Execution metadata
* Screenshots on failure
* Pie chart of results
* Logs

---

## 📸 Screenshots

Failure screenshots are saved to:

```
screenshots/
```

Old screenshots are automatically cleaned.

---

## 📁 Test Data

Excel files used for payment upload:

```
test_data/AWX_Bank_Transfer_testing_v3_Latest.xlsx
```

Framework reads:

* Supplier details
* Intercept email
* Gateway IDs
* Payment totals

---

## 🔄 Excel Auto-Update

The framework updates payment amounts **once per day** before tests run.

A flag file is created to prevent multiple updates:

```
.excel_updated_<date>.flag
```

---

## 🧱 Framework Design

### Page Object Model

Each screen has a dedicated page class:

* LoginPage
* MerchantAliasPage
* DashboardPage
* etc.

---

### Key Utilities

* Excel readers & writers
* Logging helpers
* Report customization
* Screenshot handling

---

## 🔐 Environment Configuration

Sensitive values should be stored in `.env` file:

```
USERNAME=...
PASSWORD=...
BASE_URL=...
```

Loaded automatically using python-dotenv.

---

## 🧪 Markers

Defined in `pytest.ini`:

| Marker     | Description           |
| ---------- | --------------------- |
| smoke      | Smoke tests           |
| regression | Full regression       |
| uat        | UAT environment tests |
| skip       | Skip test             |

---

## 🤖 CI/CD Support

GitHub Actions workflows available in:

```
.github/workflows/
```

Supports automated execution on push / schedule. -- Not Configured Yet

---

## ❗ Troubleshooting

### Excel totals returning None

If totals are calculated using formulas, ensure:

* File is saved after recalculation
* Or totals are computed in Python

---

### Browser issues in headless mode

Use modern headless:

```
--headless=new
--window-size=1920,1080
```

---

## 👤 Author

**Abdul Muiz Moulana**

GitHub:
👉 https://github.com/AbdulMuizMoulana

---

## 📄 License

This project is for internal automation purposes.

---

⭐ If this project helps you, consider giving it a star!
