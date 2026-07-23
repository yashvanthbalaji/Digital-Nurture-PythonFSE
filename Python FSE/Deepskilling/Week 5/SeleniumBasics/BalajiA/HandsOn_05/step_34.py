# step34
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")

# text() -> matches the EXACT visible text of the element
option_1 = driver.find_element(By.XPATH, "//label[text()='Option 1']")
print("Found exact label:", option_1.text)

# contains() -> matches if the text CONTAINS the given word anywhere
# find_elements (plural) returns a LIST of all matches, not just one
all_options = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
print("Number of labels containing 'Option':", len(all_options))
for label in all_options:
    print(" -", label.text)

driver.quit()