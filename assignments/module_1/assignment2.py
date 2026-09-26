from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
time.sleep(2)

# Click Start button
driver.find_element(By.CSS_SELECTOR, "#start button").click()
print("Clicked Start button...")

# Explicit wait - NO time.sleep() here
wait = WebDriverWait(driver, 15)
text_element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
)

text = text_element.text
print("Text found:", text)

if text == "Hello World!":
    print("PASSED: Dynamic content loaded")
else:
    print("FAILED: Unexpected text")

time.sleep(3)
driver.quit()
