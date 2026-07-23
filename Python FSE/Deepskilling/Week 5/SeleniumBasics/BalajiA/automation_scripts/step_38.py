# step38_element_to_be_clickable.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://www.testmuai.com/selenium-playground/bootstrap-alert-messages-demo/")

# Wait until the button is clickable, THEN click it
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Normal Success Message')]"))
)
button.click()
print("Button was clickable, and we clicked it")

driver.quit()

# Difference between the two conditions (just notes):
# - visibility_of_element_located: element exists in the DOM AND has a
#   size greater than zero (you could SEE it if you looked at the page).
#   It does NOT check if it's enabled or clickable.
# - element_to_be_clickable: everything visibility_of_element_located
#   checks, PLUS the element must be enabled (not disabled) AND not
#   covered by another element on top of it. This is the safer choice
#   right before calling .click() on something.