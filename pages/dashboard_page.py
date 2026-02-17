from datetime import date
from pathlib import Path

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from locators.elements_locators import Locators
from utilities.excelUtils import read_excel_totals
from selenium.webdriver.support import expected_conditions as EC
from utilities.customLogger import LogMaker
import re


class DashboardPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = LogMaker.log_gen()

    def upload_and_validate_file(self, file_path):
        #  update + refresh Excel BEFORE upload
        # update_amounts(file_path)

        self.wait.until(EC.visibility_of_element_located(Locators.DASHBOARD_TAB)).click()
        # Sources → Internal
        self.wait.until(EC.element_to_be_clickable(Locators.SOURCES_DROPDOWN)).click()

        internal = self.wait.until(EC.visibility_of_element_located(Locators.SOURCES_OPTION_INTERNAL))
        self.driver.execute_script("arguments[0].click();", internal)
        self.wait.until(EC.element_to_be_clickable(Locators.NEW_INTERNAL_BATCH)).click()
        # Template selection (if required)
        self.wait.until(EC.element_to_be_clickable(Locators.TEMPLATE_DROPDOWN)).click()

        self.wait.until(EC.element_to_be_clickable(Locators.INTERNATIONAL_PAYMENTS_TEMPLATE_OPTION)).click()

        # Upload file
        file_input = self.wait.until(EC.presence_of_element_located(Locators.UPLOAD_FILE))

        # Make hidden input usable
        self.driver.execute_script("arguments[0].style.display='block'; arguments[0].style.visibility='visible';",
                                   file_input)
        file_input.send_keys(str(file_path))

        self.wait.until(EC.element_to_be_clickable(Locators.VALIDATE_BUTTON)).click()

        self.wait.until(EC.visibility_of_element_located(Locators.VALIDATE_FILE_SUCCESS_MESSAGE_POPUP)).is_displayed()
        self.wait.until(EC.element_to_be_clickable(Locators.CHECK_BACK_LATER_BUTTON)).click()

        self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located(Locators.INTERNAL_SCREEN)).is_displayed()
        self.wait.until(EC.visibility_of_element_located(Locators.INTERNAL_TABLE)).is_displayed()

        # validate and click the uploaded file
        # file_loc = Path(file_path)
        # excel_file_name = file_loc.name
        # today_date = date.today().strftime("%m/%d/%Y")
        #
        # UPLOADED_FILE_LOCATOR = (By.XPATH,f"""//div[@role='row'  and .//*[contains(normalize-space(.),'{self.today_date}')]  and .//*[contains(normalize-space(.),'AWX_Bank_Transfer_testing_v3_Latest.xlsx')]  and .//*[contains(normalize-space(.),'VALIDATED')]]"""
        #
        #
        # UPLOADED_FILE_ROW =self.wait.until(EC.visibility_of_element_located(UPLOADED_FILE_LOCATOR))
        # if UPLOADED_FILE_ROW.is_displayed():
        #     UPLOADED_FILE_ROW.click()
        # else:
        #     self.logger.error("UPLOADED_FILE_ROW is not displayed")
        #     assert False

        file_loc = Path(file_path)
        excel_file_name = file_loc.name

        today_date = date.today().strftime("%m/%d/%y")  # IMPORTANT

        UPLOADED_FILE_LOCATOR = (
            By.XPATH,
            f"""
            //div[@role='row'
              and .//*[contains(., '{today_date}')]
              and .//*[contains(., '{excel_file_name}')]
              and .//*[contains(., 'VALIDATED')]
            ]
            """
        )

        UPLOADED_FILE_ROW = self.wait.until(
            EC.visibility_of_element_located(UPLOADED_FILE_LOCATOR)
        )
        if UPLOADED_FILE_ROW.is_displayed():
            UPLOADED_FILE_ROW.click()
            self.logger.info(f"Uploaded file: {excel_file_name} is clicked")
        else:
            self.logger.error("UPLOADED_FILE_ROW is not displayed")
            assert False
            # status_cell = self.wait.until(EC.visibility_of_element_located(Locators.STATUS_CELL)).text
            # file_name_cell = self.wait.until(EC.visibility_of_element_located(Locators.FILE_NAME_CELL)).text
            # file_name = Locators.FILE_NAME.lower()
            #
            # if status_cell.lower() == 'validated' and file_name_cell.lower() == file_name:
            #     self.driver.find_element(*Locators.FILE_NAME_CELL).click()
            #     print("found file ")
            # elif status_cell == 'Submitted' and file_name_cell == file_name:
            #     self.driver.refresh()
            #     print("file is already Submitted to the processor ")
            # else:
            #     print("file not found")


    def validate_total_amounts(self, excel_path):
        # ---------- UI ELEMENTS ----------
        total_payment_element = self.wait.until(EC.visibility_of_element_located(Locators.TOTAL_PAYMENT_AMOUNT_LABEL))
        total_invoice_element = self.wait.until(EC.visibility_of_element_located(Locators.TOTAL_INVOICE_AMOUNT_LABEL))
        total_payment_transactions = self.wait.until(
            EC.visibility_of_element_located(Locators.TOTAL_PAYMENT_TRANSACTION_LABEL))
        total_invoice_transactions = self.wait.until(
            EC.visibility_of_element_located(Locators.TOTAL_INVOICE_TRANSACTIONS_LABEL))

        # ---------- UI TEXT ----------
        ui_payment_text = total_payment_element.text
        ui_invoice_text = total_invoice_element.text
        ui_payment_txn_text = total_payment_transactions.text
        ui_invoice_txn_text = total_invoice_transactions.text

        # # ---------- PARSE UI AMOUNTS ----------
        ui_payment = float(
            re.search(r"\$([\d,]+\.\d{2})", ui_payment_text)
            .group(1)
            .replace(",", "")
        )
        ui_invoice = float(
            re.search(r"\$([\d,]+\.\d{2})", ui_invoice_text)
            .group(1)
            .replace(",", "")
        )

        # # ---------- PARSE UI TRANSACTION COUNTS ----------
        ui_payment_count = int(re.search(r"(\d+)", ui_payment_txn_text).group(1))
        ui_invoice_count = int(re.search(r"(\d+)", ui_invoice_txn_text).group(1))

        # ---------- EXCEL VALUES ----------
        excel_payment, excel_invoice = read_excel_totals(excel_path)
        df = pd.read_excel(excel_path, header=2)
        excel_transactions = len(df)

        # ---------- VALIDATION ----------
        if ui_payment == excel_payment and ui_invoice == excel_invoice and ui_payment_count == excel_transactions and ui_invoice_count == excel_transactions:
            print(" Amounts & transaction counts matched")
            assert ui_payment == excel_payment, "Payment amount mismatch"
            assert ui_invoice == excel_invoice, "Invoice amount mismatch"
            assert ui_payment_count == excel_transactions, "Transaction count mismatch"
            print(f"UI Payment Amount: {ui_payment}, Excel: {excel_payment}")
            print(f"UI Invoice Amount: {ui_invoice}, Excel: {excel_invoice}")
            print(f"UI Payment Txns: {ui_payment_count}, Excel: {excel_transactions}")
            print(f"UI Invoice Txns: {ui_invoice_count}, Excel: {excel_transactions}")
            self.wait.until(EC.element_to_be_clickable(Locators.FINALIZE_SUBMISSION_BUTTON)).click()
            self.wait.until(EC.element_to_be_clickable(Locators.CONTINUE_SUBMISSION_BUTTON)).click()
            self.wait.until(EC.visibility_of_element_located(Locators.CHECK_BACK_LATER_BUTTON)).click()
            print("file submitted successfully")
            return True
        else:
            print(" Amounts & transaction counts NOT matched")
            print("Validation failed")
            print(f"UI Payment Amount: {ui_payment}, Excel: {excel_payment}")
            print(f"UI Invoice Amount: {ui_invoice}, Excel: {excel_invoice}")
            print(f"UI Payment Txns: {ui_payment_count}, Excel: {excel_transactions}")
            print(f"UI Invoice Txns: {ui_invoice_count}, Excel: {excel_transactions}")
            return False
