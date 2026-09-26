from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.saucedemo.com/")
time.sleep(2)

# Username using By.ID
driver.find_element(By.ID, "user-name").send_keys("standard_user")
time.sleep(3)

# Password using By.NAME
driver.find_element(By.NAME, "password").send_keys("secret_sauce")
time.sleep(3)

# Login button using By.XPATH
driver.find_element(By.XPATH, "//input[@id='login-button']").click()
time.sleep(3)

# Validation
current_url = driver.current_url
print("Current URL:", current_url)

if "/inventory.html" in current_url:
    print("PASSED: Login successful")
else:
    print("FAILED: URL does not contain /inventory.html")

time.sleep(3)
driver.quit()
