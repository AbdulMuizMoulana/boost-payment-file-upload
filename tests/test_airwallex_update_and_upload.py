from pathlib import Path

import pytest

from pages.login_page import LoginPage
from pages.merchant_alias_page import MerchantAliasPage
from pages.dashboard_page import DashboardPage
from utilities.excelUtils import read_payment_excel

# ========= UAT CREDENTIALS ========
UAT_USERNAME = LoginPage.USERNAME_UAT
UAT_PASSWORD = LoginPage.PASSWORD_UAT
UAT_URL = LoginPage.URL_UAT

# ======= DEV CREDENTIALS =============
DEV_USERNAME = LoginPage.USERNAME_DEV
DEV_PASSWORD = LoginPage.PASSWORD_DEV
DEV_URL = LoginPage.URL_DEV


# ========= CREDENTIALS =========

ALL_ENV_DATA = [
    {
        "env": "dev",
        "url": LoginPage.URL_DEV,
        "username": LoginPage.USERNAME_DEV,
        "password": LoginPage.PASSWORD_DEV
    },
    {
        "env": "uat",
        "url": LoginPage.URL_UAT,
        "username": LoginPage.USERNAME_UAT,
        "password": LoginPage.PASSWORD_UAT
    },
]


@pytest.mark.parametrize("t_data", ALL_ENV_DATA)
def test_airwallex_gateway_update_dev_uat(setup, t_data, request):
    selected_env = request.config.getoption("env").lower()

    # Skip environments not selected
    if selected_env != "all" and t_data["env"] != selected_env:
        pytest.skip(f"Skipping {t_data['env']} environment")

    driver = setup

    project_root = Path(__file__).parent.parent
    excel_path = project_root / "test_data" / "AWX_Bank_Transfer_testing_v3_Latest.xlsx"

    data = read_payment_excel(excel_path)

    login = LoginPage(driver)
    merchant = MerchantAliasPage(driver)
    dashboard = DashboardPage(driver)

    login.login(t_data["url"], t_data["username"], t_data["password"])

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