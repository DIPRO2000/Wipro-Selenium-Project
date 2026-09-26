from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://the-internet.herokuapp.com/javascript_alerts")
time.sleep(2)

# ---- 1. Alert (Accept) ----
driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
time.sleep(2)
alert = driver.switch_to.alert
print("Alert says:", alert.text)
alert.accept()
time.sleep(1)
print("Result:", driver.find_element(By.ID, "result").text)

# ---- 2. Confirm (Dismiss) ----
driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
time.sleep(2)
confirm = driver.switch_to.alert
print("Confirm says:", confirm.text)
confirm.dismiss()
time.sleep(1)
print("Result:", driver.find_element(By.ID, "result").text)

# ---- 3. Prompt (Send keys + Accept) ----
driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
time.sleep(2)
prompt = driver.switch_to.alert
print("Prompt says:", prompt.text)
prompt.send_keys("Hello Selenium")
time.sleep(1)
prompt.accept()
time.sleep(1)
print("Result:", driver.find_element(By.ID, "result").text)

time.sleep(3)
driver.quit()
