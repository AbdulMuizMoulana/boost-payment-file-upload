import os
from datetime import datetime, timedelta

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# ---------------- PIE CHART COUNTERS ----------------
PASSED = 0
FAILED = 0
SKIPPED = 0


# ---------------------------------------------------
def cleanup_old_reports(reports_root, days_to_keep=2):
    cutoff = datetime.now() - timedelta(days=days_to_keep)

    for file in Path(reports_root).rglob("*.html"):
        if datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
            file.unlink(missing_ok=True)


def pytest_addoption(parser):
    # ---------- Browser option ----------
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge, safari"
    )

    # ---------- Environment option ----------
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment to run: dev / uat / all"
    )

    # ---------- headless Option ----------
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )


@pytest.fixture()
def browser(request):
    return request.config.getoption("browser")


@pytest.fixture()
def setup(browser, request):
    headless_cli = request.config.getoption("headless")
    headless_env = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")

    headless = headless_cli or headless_env

    browser_name = (browser or "chrome").lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=en-US")
        # options.add_argument("--incognito")

        if headless:
            options.add_argument("--lang=en-US")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--force-device-scale-factor=1")
            options.add_argument("--high-dpi-support=1")
            options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # explicit headless setup
        if headless:
            driver.set_window_size(1920, 1080)
            options.add_argument("--start-maximized")

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
            options.add_argument("--window-size=1920,1080")
        service = GeckoService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    elif browser_name == "safari":
        if headless:
            raise RuntimeError("Safari does not support headless mode.")
        driver = webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    try:
        driver.maximize_window()
    except:
        pass

    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def _default_report_path(config):
    # Get selected environment from pytest CLI
    env = config.getoption("env").upper()

    project_root = Path.cwd()

    # Create Reports/DEV or Reports/UAT or Reports/ALL
    reports_dir = project_root / "Reports" / env
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    filename = f"Boost_FileUpload_Report_{env}_{timestamp}.html"

    return str(reports_dir / filename)


def pytest_html_report_title(report):
    report.title = "Internal Batch File Upload Report"


def pytest_metadata(metadata, config):
    selected_env = config.getoption("env").upper()

    metadata["Project"] = "Boost File Upload Automation"
    metadata["Tester"] = "Abdul Muyeez"
    metadata["Framework"] = "Pytest + Selenium"
    metadata["Environment"] = selected_env
    metadata["Execution"] = "Local / CI"

    metadata.pop("JAVA_HOME", None)
    # metadata.pop("Java Home", None)
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)
    # metadata.pop("Platform", None)
    # metadata.pop("Python", None)




def pytest_configure(config):
    reports_root = Path.cwd() / "Reports"
    cleanup_old_reports(reports_root, days_to_keep=2)

    env = config.getoption("env").upper()

    #  Make env available globally (logs, screenshots, etc.)
    os.environ["TEST_ENV"] = env

    # Auto-generate report path if not provided
    if not getattr(config.option, "htmlpath", None):
        config.option.htmlpath = _default_report_path(config)


from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup", None)
        if driver:
            try:
                # ---------- SAVE TO FOLDER ----------

                project_root = os.path.dirname(os.path.abspath(__file__))

                screenshots_dir = os.path.join(project_root, "screenshots")

                #  DELETE SCREENSHOTS OLDER THAN 2 DAYS
                cutoff = datetime.now() - timedelta(days=2)

                for file in os.listdir(screenshots_dir):
                    file_path = os.path.join(screenshots_dir, file)

                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(
                            os.path.getmtime(file_path)
                        )
                        if file_time < cutoff:
                            os.remove(file_path)

                # Take screenshot in base64
                png_b64 = driver.get_screenshot_as_base64()

                # IMPORTANT: remove whitespace + line breaks
                png_b64 = png_b64.replace("\n", "").replace("\r", "").strip()

                # Do NOT recreate folder – just use it
                screenshot_name = (
                    f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)

                # Save PNG
                driver.save_screenshot(screenshot_path)

                print(f"Screenshot saved at: {screenshot_path}")

                # Attach screenshot as proper PNG
                extra = extras.png(png_b64, "Screenshot on failure")

                if hasattr(report, "extra"):
                    report.extra.append(extra)
                else:
                    report.extra = [extra]

            except Exception as e:
                print(f"Screenshot capture failed: {e}")


def pytest_runtest_logreport(report):
    global PASSED, FAILED, SKIPPED

    # PASSED / FAILED --> only during call
    if report.when == "call":
        if report.passed:
            PASSED += 1
        elif report.failed:
            FAILED += 1

    # SKIPPED --> can happen in setup OR call
    if report.skipped:
        SKIPPED += 1


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append(
        f"""
        <style>
            body {{
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }}

            h1 {{
                padding : 5px 0px;
                border-radius : 12px;
                background: linear-gradient(to right,#020024, #090979, #09B6D9);
                text-align: center;
                color: #FFFFFF !important;
            }}

            h2, h3 {{
                color: #F5F5F5 !important;
            }}

            table {{
                color: #E0E0E0 !important;
            }}

            th {{
                color: #FFFFFF !important;
            }}

            td {{
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }}

            p {{
            color: #FFFFFF !important;
            }}

            canvas {{
            padding: 15px;
            border-radius: 12px;
            background-color: #E0E0E0 !important;
            }}
        </style>

        <h2>Test Result Distribution</h2>

        <canvas id="resultChart" width="360" height="360"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            const passed = {PASSED};
            const failed = {FAILED};
            const skipped = {SKIPPED};
            const total = passed + failed + skipped;

            new Chart(document.getElementById('resultChart'), {{
                type: 'pie',
                data: {{
                    labels: ['Passed', 'Failed', 'Skipped'],
                    datasets: [{{
                        data: [passed, failed, skipped],
                        backgroundColor: ['#2ecc71', '#FF0000', '#f1c40f'],
                        borderColor: '#121212',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: false,
                    plugins: {{
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const value = context.raw;
                                    const percent = ((value / total) * 100).toFixed(1);
                                    return `${{context.label}}: ${{value}} (${{percent}}%)`;
                                }}
                            }}
                        }},
                        legend: {{
                            labels: {{
                                color: '#000000',
                                font: {{ size: 14 }}
                            }}
                        }}
                    }}
                }}
            }});
        </script>
        """
    )

    prefix.insert(0, """
        <div style="
            background: #1e1e1e;
            color: #ffffff;
            text-align: center;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 32px;
            font-weight: bold;
        ">
        </div>
    """)


# ===================== this code will update the Excel file =========
from pathlib import Path
from datetime import date
import pytest
from utilities.excelUtils import update_amounts


@pytest.fixture(scope="session", autouse=True)
def update_excel_once_per_day():
    """
    Updates Excel only once per calendar day.
    Runs automatically before any test.
    """

    project_root = Path(__file__).parent
    excel_path = project_root / "test_data" / "AWX_Bank_Transfer_testing_v3_Latest.xlsx"

    today = date.today().isoformat()  # 2026-02-10
    flag_file = project_root / f".excel_updated_{today}.flag"

    # Delete OLD flag files
    for file in project_root.glob(".excel_updated_*.flag"):
        if file.name != flag_file.name:
            file.unlink(missing_ok=True)

    if flag_file.exists():
        print(f"Excel already updated for today ({today}). Skipping update.")
        return

    print(f"Updating Excel for today ({today})")
    update_amounts(excel_path)

    flag_file.touch()
