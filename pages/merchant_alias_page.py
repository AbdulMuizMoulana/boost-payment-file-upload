import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.elements_locators import Locators
from utilities.customLogger import LogMaker


class MerchantAliasPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = LogMaker.log_gen()

    def click_kebab_for_supplier(self, supplier_name):
        """
        Robust kebab click for MuiDataGrid rows
        """
        self.logger.info(f"******** Clicking Kebab Menu for Supplier: {supplier_name} ********")

        kebab_locator = (
            By.XPATH,
            f"""
            //div[@role='row'] [.//div[contains(normalize-space(), "{supplier_name}")]]
            //button[@aria-label='options']
            """
        )

        kebab = self.wait.until(EC.visibility_of_element_located(kebab_locator))
        self.logger.info("******** Kebab Element Located ********")

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", kebab)
        kebab.is_displayed()

        self.driver.execute_script("arguments[0].click();", kebab)
        self.logger.info("******** Kebab Clicked Successfully ********")

    def wait_and_click_filtered_transaction(self, supplier_name):

        self.logger.info(f"******** Clicking Filtered Transaction Row for Supplier: {supplier_name} ********")

        transaction_locator = (
            By.XPATH,
            f"""//div[@role='row'] [.//div[contains(normalize-space(), '{supplier_name}')]]//a """
        )

        filtered_transaction = self.wait.until(
            EC.visibility_of_element_located(transaction_locator)
        )

        self.logger.info("******** Filtered Transaction Row Located ********")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            filtered_transaction
        )

        filtered_transaction.is_displayed()

        self.driver.execute_script("arguments[0].click();", filtered_transaction)
        self.logger.info("******** Filtered Transaction Row Clicked ********")

    def scroll_to_element(self, locator):

        self.logger.info(f"******** Scrolling To Element: {locator} ********")

        element = self.wait.until(EC.presence_of_element_located(locator))
        element.is_displayed()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        self.logger.info("******** Scroll Completed ********")
        return element

    def navigate_to_merchant_alias(self):

        self.logger.info("******** Navigating To Merchant Alias Screen ********")

        self.wait.until(EC.element_to_be_clickable(Locators.REF_DATA_TAB)).click()
        self.logger.info("******** Clicked REF DATA Tab ********")

        self.wait.until(EC.visibility_of_element_located(Locators.REFERENCE_DATA_DROPDOWN)).click()
        self.logger.info("******** Opened Reference Data Dropdown ********")

        self.scroll_to_element(Locators.MERCHANT_ALIAS_OPTION)

        self.wait.until(EC.visibility_of_element_located(Locators.MERCHANT_ALIAS_OPTION)).click()
        self.logger.info("******** Clicked Merchant Alias Option ********")

        self.wait.until(
            EC.visibility_of_element_located(Locators.MERCHANT_ALIAS_SCREEN)
        ).is_displayed()

        self.logger.info("******** Merchant Alias Screen Loaded Successfully ********")

    def filter_by_email(self, email):

        self.logger.info(f"******** Applying Filter For Email: {email} ********")

        self.wait.until(EC.element_to_be_clickable(Locators.FILTER_MERCHANT_ALIAS)).click()
        self.logger.info("******** Clicked Filter Button ********")

        self.wait.until(EC.element_to_be_clickable(Locators.COLUMN_NAME_DROPDOWN)).click()
        self.logger.info("******** Opened Column Dropdown ********")

        merchant_key = self.wait.until(
            EC.visibility_of_element_located(Locators.COLUMN_NAME_MERCHANT_KEY)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            merchant_key
        )

        merchant_key.is_displayed()
        self.driver.execute_script("arguments[0].click();", merchant_key)
        self.logger.info("******** Selected Merchant Key Column ********")

        filter_value_input = self.wait.until(
            EC.visibility_of_element_located(Locators.FILTER_VALUE)
        )

        filter_value_input.click()
        filter_value_input.send_keys(Keys.CONTROL + "a")
        filter_value_input.send_keys(Keys.BACKSPACE)
        filter_value_input.send_keys(email)

        self.logger.info("******** Entered Email In Filter Field ********")

        self.wait.until(EC.element_to_be_clickable(Locators.FILTER_BUTTON)).click()
        self.logger.info("******** Clicked Apply Filter ********")

        self.wait.until(
            EC.presence_of_element_located(Locators.GRID_ROWS)
        ).is_displayed()

        self.logger.info("******** Filtered Grid Loaded Successfully ********")

    def edit_and_update_gateway(self, supplier_name, gateway_supplier_id):

        self.logger.info(f"******** Starting Gateway Update For Supplier: {supplier_name} ********")

        # Click transaction row
        try:
            self.wait_and_click_filtered_transaction(supplier_name)
            self.logger.info("******** Filtered Grid Loaded Successfully and clicked  ********")
        except:
            self.wait.until(EC.element_to_be_clickable(Locators.RELOAD_DATA_BUTTON)).click()
            self.logger.info("******** Clicked Reload Data Button to load the transaction********")
            self.wait_and_click_filtered_transaction(supplier_name)
            self.logger.info("******** Filtered Grid Loaded Successfully and clicked  ********")



        # Open kebab for supplier
        self.click_kebab_for_supplier(supplier_name)

        # Click edit
        self.wait.until(
            EC.element_to_be_clickable(Locators.EDIT_EXISTING_RECORD)
        ).click()

        self.logger.info("******** Clicked Edit Existing Record ********")

        # -------- GATEWAY DROPDOWN --------
        self.wait.until(
            EC.element_to_be_clickable(Locators.GATEWAY_DROPDOWN)
        ).click()

        self.logger.info("******** Opened Gateway Dropdown ********")

        gateway_option = self.wait.until(
            EC.visibility_of_element_located(Locators.GATEWAY_OPTION_AIRWALLEX)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            gateway_option
        )

        self.driver.execute_script("arguments[0].click();", gateway_option)

        self.logger.info("******** Selected Gateway: Airwallex ********")

        # -------- PROCESSOR DROPDOWN --------
        self.wait.until(
            EC.element_to_be_clickable(Locators.PROCESSOR_DROPDOWN)
        ).click()

        self.logger.info("******** Opened Processor Dropdown ********")

        processor_option = self.wait.until(
            EC.visibility_of_element_located(Locators.PROCESSOR_OPTION_AIRWALLEX)
        )

        self.driver.execute_script("arguments[0].click();", processor_option)

        self.logger.info("******** Selected Processor: Airwallex ********")

        # -------- GATEWAY SUPPLIER ID --------
        gateway_field = self.wait.until(
            EC.visibility_of_element_located(Locators.GATEWAY_SUPPLIER_IDENTIFIER)
        )

        gateway_field.clear()
        gateway_field.send_keys(gateway_supplier_id)

        self.logger.info(f"******** Entered Gateway Supplier ID: {gateway_supplier_id} ********")

        # -------- CONFIRM --------

        # Wait until button is visible (not clickable)
        confirm_btn = self.wait.until(
            EC.presence_of_element_located(Locators.CONFIRM_CHANGES)
        )

        # Scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            confirm_btn
        )

        # Extra scroll (fix sticky headers)
        self.driver.execute_script("window.scrollBy(0, 200);")

        # Allow rendering to stabilize
        time.sleep(1)

        # JS click (bypasses overlay issues)
        self.driver.execute_script("arguments[0].click();", confirm_btn)

        self.logger.info("******** Clicked Confirm Changes ********")


        # -------- SUCCESS POPUP --------
        self.wait.until(
            EC.visibility_of_element_located(Locators.SUCCESS_MSG_POPUP)
        )

        self.logger.info("******** Success Popup Displayed ********")

        self.wait.until(
            EC.element_to_be_clickable(Locators.SUCCESS_MSG_CLOSE_BTN)
        ).click()

        self.logger.info("******** Closed Success Popup ********")

        # Go back to list
        self.driver.back()
        self. wait.until(EC.visibility_of_element_located(Locators.MERCHANT_ALIAS_SCREEN))

        self.logger.info("******** Returned Back To Merchant Alias List ********")
