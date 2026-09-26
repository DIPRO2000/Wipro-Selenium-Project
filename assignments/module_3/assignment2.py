"""
Assignment 2: Test Data Driven Automation in Behave Framework.

Reads test data from testdata.json and runs the login scenario
for each combination. Loops through success and error cases.
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def load_test_data(filepath="testdata.json"):
    """Load test cases from JSON file."""
    with open(filepath) as f:
        return json.load(f)


def run_scenario(driver, username, password, expected):
    """Run one BDD-style scenario."""
    # Clear any leftover session from previous scenario
    driver.delete_all_cookies()
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    time.sleep(2)

    if expected == "success":
        assert "/inventory.html" in driver.current_url, \
            f"FAILED: {username} should succeed"
        print(f"PASSED: {username} -> login success")
    else:
        time.sleep(1)
        error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        assert len(error) > 0, f"FAILED: {username} should show error"
        print(f"PASSED: {username} -> error shown: {error[:50]}...")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    test_data = load_test_data()
    print(f"Loaded {len(test_data)} scenarios from testdata.json\n")

    for i, row in enumerate(test_data, 1):
        print(f"--- Scenario {i}: {row['username']} ---")
        run_scenario(driver, row["username"], row["password"], row["expected"])
        print()

    print("All BDD scenarios completed.")
    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
