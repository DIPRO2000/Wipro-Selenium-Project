from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.w3schools.com/html/html_tables.asp")
time.sleep(5)

table = driver.find_element(By.ID, "customers")
headers = table.find_elements(By.TAG_NAME, "th")
header_names = [h.text.strip() for h in headers]
print("Headers:", header_names)

contact_index = header_names.index("Contact")
print("Contact column index:", contact_index)

rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
if not rows:
    rows = table.find_elements(By.TAG_NAME, "tr")

found = False

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if not cells:
        continue

    row_name = cells[0].text.strip()
    print("Row:", row_name)

    # Match a real company name from this table
    if row_name == "Ernst Handel":
        value = cells[contact_index].text.strip()
        print("Ernst Handel -> Contact =", value)
        found = True
        break

if found:
    print("PASSED: Row extracted")
else:
    print("FAILED: Row not found")

time.sleep(3)
driver.quit()
