from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()

# ---- Part A: Iframe ----
driver.get("https://the-internet.herokuapp.com/iframe")
time.sleep(3)

iframe = driver.find_element(By.ID, "mce_0_ifr")
driver.switch_to.frame(iframe)
time.sleep(1)

# Just append text without clearing (simpler)
body = driver.find_element(By.ID, "tinymce")
body.send_keys(" - Added by Selenium!")
print("Typed inside iframe")

driver.switch_to.default_content()
print("Back to main page")
time.sleep(2)

# ---- Part B: New Tab ----
driver.get("https://the-internet.herokuapp.com/windows")
time.sleep(2)

main_window = driver.current_window_handle

driver.find_element(By.LINK_TEXT, "Click Here").click()
time.sleep(3)

for window in driver.window_handles:
    if window != main_window:
        driver.switch_to.window(window)
        break

print("New tab title:", driver.title)
time.sleep(2)

driver.close()
driver.switch_to.window(main_window)
print("Back to main window:", driver.title)

time.sleep(3)
driver.quit()
