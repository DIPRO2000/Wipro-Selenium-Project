"""
Assignment 1: Selenium Python + Behave BDD Setup.

Runs a simple BDD-style login scenario using Selenium.
BDD concepts: Given / When / Then structure (as functions).
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def given_open_login_page(driver):
    """GIVEN: Open the SauceDemo login page."""
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)
    print("GIVEN: Opened SauceDemo login page")


def when_enter_credentials(driver, username, password):
    """WHEN: Enter username and password."""
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    print(f"WHEN: Entered credentials ({username})")


def when_click_login(driver):
    """WHEN: Click the login button."""
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    time.sleep(3)
    print("WHEN: Clicked login button")


def then_should_be_on_inventory(driver):
    """THEN: Verify we land on the inventory page."""
    assert "/inventory.html" in driver.current_url, \
        f"FAILED: expected inventory page, got {driver.current_url}"
    print("THEN: On inventory page - PASSED")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Scenario: Successful login
    given_open_login_page(driver)
    when_enter_credentials(driver, "standard_user", "secret_sauce")
    when_click_login(driver)
    then_should_be_on_inventory(driver)

    print("\nScenario PASSED: Successful login")
    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
