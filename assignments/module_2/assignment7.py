"""
Assignment 7: Page Object Model (POM) Restructure.

POM pattern in a single file:
- BasePage: common helpers
- LoginPage: locators + actions
- InventoryPage: locators + actions
- TestLogin: assertions only

Run: python assignment7_pom.py
"""

import os
import time
import unittest
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# BASE PAGE (common helpers)

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

    def screenshot(self, name):
        os.makedirs("screenshots", exist_ok=True)
        path = f"screenshots/{name}_{datetime.now().strftime('%H%M%S')}.png"
        self.driver.save_screenshot(path)
        print(f"Screenshot saved: {path}")



# LOGIN PAGE

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



# INVENTORY PAGE

class InventoryPage(BasePage):
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")

    def is_loaded(self):
        return "/inventory.html" in self.get_url()

    def add_backpack(self):
        self.click(self.ADD_BACKPACK)

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)



# TESTS (assertions only — no locators here)

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

    def test_valid_login(self):
        try:
            self.login_page.open()
            time.sleep(2)
            self.login_page.login("standard_user", "secret_sauce")
            time.sleep(3)
            self.assertTrue(self.inventory_page.is_loaded())
            print("PASSED: Valid login")
        except AssertionError:
            self.login_page.screenshot("valid_login_fail")
            raise

    def test_invalid_login(self):
        self.login_page.open()
        time.sleep(2)
        self.login_page.login("wrong_user", "wrong_pass")
        time.sleep(2)
        self.assertIn("do not match", self.login_page.get_error())
        print("PASSED: Invalid login error shown")

    def test_add_to_cart(self):
        self.login_page.open()
        time.sleep(2)
        self.login_page.login("standard_user", "secret_sauce")
        time.sleep(3)
        self.inventory_page.add_backpack()
        time.sleep(2)
        self.assertEqual(self.inventory_page.get_cart_count(), "1")
        print("PASSED: Item added to cart")


if __name__ == "__main__":
    unittest.main(verbosity=2)
