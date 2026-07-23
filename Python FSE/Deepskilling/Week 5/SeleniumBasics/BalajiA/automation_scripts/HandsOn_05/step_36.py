# step36
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alerts")

# Click the button that triggers the success alert
success_button = driver.find_element(By.ID, "success-alert")
success_button.click()

# WebDriverWait keeps checking, up to 10 seconds, until the condition
# is true - here, until the .alert-success element is visible
alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
)

assert "successfully" in alert.text
print("Alert text was:", alert.text)
print("Test passed: alert appeared and contains 'successfully'")

driver.quit()