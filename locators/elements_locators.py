from selenium.webdriver.common.by import By

class Locators:

    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")

    SIGN_IN_BUTTON = (By.XPATH, "//button[contains(text(), 'Sign in')]")

    REF_DATA_TAB = (By.ID,"nav-tab-3")
    REFERENCE_DATA_DROPDOWN = (By.XPATH, "//button[text()='Reference Data']")
    MERCHANT_ALIAS_OPTION =(By.XPATH, "//li[contains(text(),'Merchant Alias')]")
    MERCHANT_ALIAS_SCREEN =(By.XPATH,"//div[@class='MuiContainer-root css-ur2jdm-MuiContainer-root']")

    FILTER_MERCHANT_ALIAS = (By.XPATH,"//button[@id='filter-container-btn']")
    GRID_ROWS = (By.XPATH,"//div[@role='row']")
    COLUMN_NAME_DROPDOWN =(By.XPATH, "//div[@aria-label='Without label']")
    COLUMN_NAME_MERCHANT_KEY = (By.XPATH, "//li[@name='Merchant Key']")
    FILTER_VALUE =(By.XPATH, "//input[@placeholder='Filter Value']")

    FILTER_BUTTON = (By.ID,"filter")

    # ROW_TRANSACTION = (By.XPATH, "//div[@role='row']//a")
    # ROW_TRANSACTION = (By.XPATH, "//div[@role='row'] [.//div[contains(normalize-space(), '{supplier_name}')]]//a")

    # ME_SVG_KEBAB =(By.XPATH, "//button[@aria-label='options']//*[name()='svg']")
    ME_SVG_KEBAB = (By.XPATH, "//button[@aria-label='options']")

    EDIT_EXISTING_RECORD =(By.XPATH, "//li[normalize-space()='Edit Existing Record']")

    GATEWAY_DROPDOWN = (By.XPATH,"//div[@id='input-field-gateway']")
    GATEWAY_OPTION_AIRWALLEX =(By.XPATH, "//li[contains(text(),'Airwallex')]")

    PROCESSOR_DROPDOWN =(By.XPATH, "//div[@id='input-field-processor']")
    PROCESSOR_OPTION_AIRWALLEX =(By.XPATH, "//li[contains(text(),'Airwallex')]")

    GATEWAY_SUPPLIER_IDENTIFIER =(By.XPATH, "//input[@id='input-field-gatewaySupplierIdentifier']")
    # CONFIRM_CHANGES =(By.XPATH, "//button[normalize-space()='Confirm Changes']")

    CONFIRM_CHANGES =(By.XPATH, "// button[contains(text(), 'Confirm')]")


    SUCCESS_MSG_POPUP =(By.XPATH, "//h3[@id='confirmation-modal']")
    SUCCESS_MSG_CLOSE_BTN = (By.XPATH, "//*[name()='path' and contains(@d,'M25.6134 0')]")
    CANCEL_BTN_MSG = (By.XPATH, "//*[name()='path' and contains(@d,'M25.6134 0')]")
    CANCEL_POPUP_MSG =(By.XPATH,"//h3[@id='cancel-changes']")

    EDIT_FILTER = (By.XPATH, "//button[@id='filter-container-btn']")
    RELOAD_DATA_BUTTON = (By.XPATH, "//button[@aria-label='Reload Data']")

    # DASHBOARD_TAB = (By.XPATH, "//button[@id='nav-tab-0']")
    DASHBOARD_TAB = (By.XPATH, "//button[contains(normalize-space(),'Dashboard')]")


    SOURCES_DROPDOWN =(By.XPATH, "//button[normalize-space()='Sources']")
    SOURCES_OPTION_INTERNAL =(By.XPATH, "//li[normalize-space()='Internal']")

    NEW_INTERNAL_BATCH = (By.XPATH, "//button[normalize-space()='New Internal Batch']")

    TEMPLATE_DROPDOWN =(By.XPATH, "//div[@id='templates']")
    INTERNATIONAL_PAYMENTS_TEMPLATE_OPTION = (By.XPATH, "//li[@name='Template International Payments']")

    UPLOAD_FILE =(By.XPATH,"//input[@type='file' and contains(@accept,'.xls')]")

    VALIDATE_BUTTON= (By.XPATH, "//button[normalize-space()='Validate']")

    VALIDATE_FILE_SUCCESS_MESSAGE_POPUP =(By.XPATH, "//div[contains(text(),'We’re validating your file!')]")

    CHECK_BACK_LATER_BUTTON =(By.XPATH, "//button[normalize-space()='Check back later']")


    INTERNAL_SCREEN =(By.XPATH, "//h3[normalize-space()='Internal']")
    INTERNAL_TABLE =(By.XPATH, "//div[@class='MuiDataGrid-main css-204u17-MuiDataGrid-main']")

    # FILE_NAME = (By.XPATH, "//div[@aria-label='AWX_Bank_Transfer_testing_v3_Latest (1).xlsx']")



    # FILE_NAME_CELL = (By.XPATH, "//body//div[@id='root']//div[@role='presentation']//div[@role='presentation']//div[@role='rowgroup']//div[1]//div[6]")
    #
    # STATUS_CELL = (By.XPATH, "//body//div[@id='root']//div[@role='presentation']//div[@role='presentation']//div[@role='rowgroup']//div[1]//div[5]")

    TOTAL_PAYMENT_AMOUNT_LABEL = (By.XPATH, "//span[contains(text(),'Total Payments Amount')]")
    TOTAL_INVOICE_AMOUNT_LABEL = (By.XPATH, "//span[contains(text(),'Total Invoice Amount')]")
    TOTAL_PAYMENT_TRANSACTION_LABEL = (By.XPATH, "//span[contains(text(),'Total Payments:')]")
    TOTAL_INVOICE_TRANSACTIONS_LABEL = (By.XPATH, "//span[contains(text(),'Total Invoices:')]")

    f"""// div[ @ role = "row"][div[contains(normalize - space(.), 'AWX_Bank_Transfer_testing_v3_Latest (1).xlsx')] and div[
        contains(normalize - space(.), '02/12/26')] and div[contains(normalize - space(.), 'VALIDATED')]] """

    FINALIZE_SUBMISSION_BUTTON = (By.XPATH, "//li[@id='action_item_finalize_submission']")
    CONTINUE_SUBMISSION_BUTTON = (By.XPATH, "//button[normalize-space()='Continue Submission']")

    DISCARD_BATCH_BUTTON = (By.XPATH, "//li[@id='action_item_discard_batch']")
    GO_TO_PAYMENTS_BUTTON = (By.XPATH, "//li[@id='action_item_go_to_payments']")



    FILE_NAME = "AWX_Bank_Transfer_testing_v3_Latest (1).xlsx"





