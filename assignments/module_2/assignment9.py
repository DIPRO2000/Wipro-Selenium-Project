"""
Assignment 9: PyTest Integration with HTML Reporting.

- Uses a pytest fixture for driver setup/teardown
- Screenshot on test failure
- Generates HTML report with screenshots of failed tests

Run:
    pytest assignment9_pytest_html.py -v --html=report.html --self-contained-html
"""

import os
import time
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By



# FIXTURE: driver setup + screenshot on failure

@pytest.fixture
def driver(request):
    d = webdriver.Chrome()
    d.maximize_window()
    d.get("https://www.saucedemo.com/")
    time.sleep(2)

    yield d

    # Screenshot if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        path = f"screenshots/{request.node.name}_{datetime.now().strftime('%H%M%S')}.png"
        d.save_screenshot(path)
        print(f"\nScreenshot saved: {path}")

    time.sleep(1)
    d.quit()



# HOOK: tells the fixture if the test failed

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)



# TESTS

def test_valid_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    time.sleep(3)
    assert "/inventory.html" in driver.current_url


def test_locked_out_user(driver):
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    time.sleep(2)
    error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    assert "locked out" in error


def test_intentional_failure(driver):
    """Fails on purpose to demo screenshot on failure."""
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    time.sleep(3)
    assert "THIS_TEXT_NEVER_EXISTS" in driver.page_source
