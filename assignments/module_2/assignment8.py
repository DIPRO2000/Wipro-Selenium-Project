"""
Assignment 8: Data-Driven Automation (DDT).

Reads test cases from testdata.csv and loops through them.
Each row = one login attempt with expected outcome.

Run: python assignment8_ddt.py
"""

import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def load_csv(filepath="testdata.csv"):
    """Read all rows from CSV into a list of dicts."""
    rows = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def run_test(driver, username, password, expected):
    """Execute one test case."""
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)

    if username:
        driver.find_element(By.ID, "user-name").send_keys(username)
    if password:
        driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    time.sleep(2)

    if expected == "success":
        assert "/inventory.html" in driver.current_url, \
            f"FAILED for '{username}': expected success"
        print(f"PASSED: {username or '(blank)'} -> success")
    else:
        error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        assert len(error) > 0, f"FAILED for '{username}': expected error message"
        print(f"PASSED: {username or '(blank)'} -> error shown")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    test_data = load_csv()
    print(f"Loaded {len(test_data)} test cases\n")

    for row in test_data:
        run_test(driver, row["username"], row["password"], row["expected"])

    print("\nAll data-driven tests completed.")
    driver.quit()


if __name__ == "__main__":
    main()
