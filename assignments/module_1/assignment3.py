from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()

# ---- Part A: Checkboxes ----
driver.get("https://the-internet.herokuapp.com/checkboxes")
time.sleep(2)

checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

# Select first checkbox if not selected
if not checkboxes[0].is_selected():
    checkboxes[0].click()
    print("Checkbox 1 clicked")
time.sleep(1)

# Verify using .is_selected()
print("Checkbox 1 selected?", checkboxes[0].is_selected())
print("Checkbox 2 selected?", checkboxes[1].is_selected())

time.sleep(2)

# ---- Part B: Autocomplete Dropdown ----
driver.get("https://jqueryui.com/autocomplete/")
time.sleep(2)

# Switch into the iframe
iframe = driver.find_element(By.CSS_SELECTOR, ".demo-frame")
driver.switch_to.frame(iframe)
time.sleep(1)

# Type "Ja" into the autocomplete field
input_box = driver.find_element(By.ID, "tags")
input_box.send_keys("Ja")
time.sleep(2)

# Get all suggestions and click "Java"
suggestions = driver.find_elements(By.CSS_SELECTOR, "ul.ui-autocomplete li")
for item in suggestions:
    print("Suggestion:", item.text)
    if "Java" in item.text:
        item.click()
        print("Selected Java")
        break

time.sleep(3)
driver.quit()
