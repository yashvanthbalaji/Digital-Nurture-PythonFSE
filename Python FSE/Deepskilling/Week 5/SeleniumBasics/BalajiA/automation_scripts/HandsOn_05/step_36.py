# step36
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

# Locate the button by its VISIBLE TEXT, since there's no id on this site
success_button = driver.find_element(By.XPATH, "//button[contains(text(),'Normal Success Message')]")
success_button.click()

# WebDriverWait keeps checking, up to 10 seconds, until the condition
# is true - here, until the .alert-success element is visible
alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
)

print("Alert text was:", alert.text)
assert "success" in alert.text.lower()
print("Test passed: alert appeared and mentions success")

driver.quit()