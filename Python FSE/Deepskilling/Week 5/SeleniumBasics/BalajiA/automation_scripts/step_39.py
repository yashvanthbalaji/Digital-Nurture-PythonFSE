# step39_fluent_wait.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://www.testmuai.com/selenium-playground/table-sort-search-demo/")

# FluentWait: WebDriverWait with 2 extra dials turned on:
# - poll_frequency: check every 0.5 seconds
# - ignored_exceptions: don't crash if the element isn't there YET,
#   just quietly try again on the next poll, until the timeout runs out
fluent_wait = WebDriverWait(
    driver,
    timeout=10,
    poll_frequency=0.5,
    ignored_exceptions=[NoSuchElementException],
)

# Wait for the first row inside the table body to actually appear
first_row = fluent_wait.until(
    lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr")
)
print("Table row appeared:", first_row.text)

driver.quit()