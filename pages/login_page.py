from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.elements_locators import Locators
# from utilities.readProperties import ReadConfig
from utilities.customLogger import LogMaker



class LoginPage:
    # # ========= UAT CREDENTIALS ========
    # USERNAME_UAT = ReadConfig.UAT_USERNAME
    # PASSWORD_UAT = ReadConfig.UAT_PASSWORD
    # URL_UAT = ReadConfig.UAT_URL
    # # ======= DEV CREDENTIALS =============
    # USERNAME_DEV = ReadConfig.DEV_USERNAME
    # PASSWORD_DEV = ReadConfig.DEV_PASSWORD
    # URL_DEV = ReadConfig.DEV_URL

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = LogMaker.log_gen()

    def login(self, url, username, password):
        self.logger.info("******** Navigating to Login URL ********")
        self.driver.get(url)

        self.logger.info("******** Entering Username ********")
        userName = self.wait.until(EC.visibility_of_element_located(Locators.USERNAME_INPUT))
        userName.click()
        userName.send_keys(username)

        self.logger.info("******** Entering Password ********")
        password_txt_field = self.wait.until(EC.visibility_of_element_located(Locators.PASSWORD_INPUT))
        password_txt_field.click()
        password_txt_field.send_keys(password)

        self.logger.info("******** Clicking Sign In Button ********")
        sign_in = self.wait.until(EC.element_to_be_clickable(Locators.SIGN_IN_BUTTON))
        sign_in.click()

        self.logger.info("******** Login Action Completed ********")

