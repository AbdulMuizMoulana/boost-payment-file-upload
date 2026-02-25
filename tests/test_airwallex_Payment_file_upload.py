from pathlib import Path

import pytest

from pages.login_page import LoginPage
from pages.merchant_alias_page import MerchantAliasPage
from pages.dashboard_page import DashboardPage
from utilities.excelUtils import read_payment_excel
from utilities.readProperties import ReadConfig

# ======= DEV CREDENTIALS =============
DEV_USERNAME = ReadConfig.DEV_USERNAME
DEV_PASSWORD = ReadConfig.DEV_PASSWORD
DEV_URL = ReadConfig.DEV_URL

# ========= UAT CREDENTIALS ========
UAT_USERNAME = ReadConfig.UAT_USERNAME
UAT_PASSWORD = ReadConfig.UAT_PASSWORD
UAT_URL = ReadConfig.UAT_URL

# ========= CREDENTIALS =========

ALL_ENV_DATA = [
    {
        "env": "dev",
        "url": DEV_URL,
        "username": DEV_USERNAME,
        "password": DEV_PASSWORD
    },
    {
        "env": "uat",
        "url": UAT_URL,
        "username": UAT_USERNAME,
        "password":UAT_PASSWORD
    },
]


@pytest.mark.parametrize("environment", ALL_ENV_DATA)
def test_airwallex_gateway_update_and_upload(setup, environment, request):
    selected_env = request.config.getoption("env").lower()

    # Skip environments not selected
    if selected_env != "all" and environment["env"] != selected_env:
        pytest.skip(f"Skipping {environment['env']} environment")

    driver = setup

    project_root = Path(__file__).parent.parent
    excel_path = project_root / "test_data" / "AWX_Bank_Transfer_testing_v3_Latest.xlsx"

    data = read_payment_excel(excel_path)

    login = LoginPage(driver)
    merchant = MerchantAliasPage(driver)
    dashboard = DashboardPage(driver)

    login.login(environment["url"], environment["username"], environment["password"])

    merchant.navigate_to_merchant_alias()

    for _, row in data.iterrows():
        merchant.filter_by_email(row["Intercept Email Address"])

        merchant.edit_and_update_gateway(
            supplier_name=row["Supplier Name"],
            gateway_supplier_id=row["Gateway Supplier ID"]
        )


    dashboard.upload_and_validate_file(excel_path)
    dashboard.validate_total_amounts(excel_path)


"""This code is to run the UAT env Explicitly 
def test_uat_airwallex_gateway_update(setup):
    driver = setup
    project_root = Path(__file__).parent.parent
    excel_path = project_root / "test_data" / "AWX_Bank_Transfer_testing_v3_Latest (1).xlsx"

    data = read_payment_excel(excel_path)

    login = LoginPage(driver)
    merchant = MerchantAliasPage(driver)
    dashboard = DashboardPage(driver)

    login.login(UAT_URL, UAT_USERNAME, UAT_PASSWORD)

    merchant.navigate_to_merchant_alias()

    for _, row in data.iterrows():
        merchant.filter_by_email(row["Intercept Email Address"])

        merchant.edit_and_update_gateway(
            supplier_name=row["Supplier Name"],
            gateway_supplier_id=row["Gateway Supplier ID"]
        )

    dashboard.upload_and_validate_file(excel_path)
    dashboard.validate_total_amounts(excel_path)
"""