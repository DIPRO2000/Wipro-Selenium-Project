"""
Assignment 3: Selenium Page Object Model in the Behave Framework.

Combines POM architecture (BasePage, LoginPage) with BDD-style
functions for the given/when/then flow.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------------------------------------
# POM: Base Page
# ---------------------------------------------------------
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.find(locator).click()

    def type_text(self, locator, text):
        self.find(locator).send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def get_url(self):
        return self.driver.current_url


# ---------------------------------------------------------
# POM: Login Page
# ---------------------------------------------------------
class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.XPATH, "//input[@id='login-button']")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    URL = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_error(self):
        return self.get_text(self.ERROR_MSG)

    def is_logged_in(self):
        return "/inventory.html" in self.get_url()


# ---------------------------------------------------------
# BDD Scenarios (Gherkin-style)
# ---------------------------------------------------------
def scenario_valid_login(driver, login_page):
    """Scenario: Login with valid credentials."""
    print("Scenario: Login with valid credentials")
    print("  Given I open the login page")
    login_page.open()
    time.sleep(2)

    print('  When I login with "standard_user" and "secret_sauce"')
    login_page.login("standard_user", "secret_sauce")
    time.sleep(3)

    print("  Then I should be on the inventory page")
    assert login_page.is_logged_in(), "Expected inventory page"
    print("  PASSED\n")


def scenario_locked_out_user(driver, login_page):
    """Scenario: Login with locked out user."""
    print("Scenario: Login with locked out user")
    print("  Given I open the login page")
    # Clear cookies so we start fresh
    driver.delete_all_cookies()
    login_page.open()
    time.sleep(2)

    print('  When I login with "locked_out_user" and "secret_sauce"')
    login_page.login("locked_out_user", "secret_sauce")
    time.sleep(2)

    print("  Then I should see an error message")
    error = login_page.get_error()
    assert len(error) > 0, "Expected error message"
    print(f"  PASSED: {error[:50]}...\n")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    login_page = LoginPage(driver)

    scenario_valid_login(driver, login_page)
    scenario_locked_out_user(driver, login_page)

    print("All POM + BDD scenarios completed.")
    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
