from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
link.click()

assert "simple-form-demo" in driver.current_url
print("Passed: we are on the Simple Form Demo page")
print("Current URL:", driver.current_url)

driver.back()
print("Went back. Current URL now:", driver.current_url)

driver.quit()