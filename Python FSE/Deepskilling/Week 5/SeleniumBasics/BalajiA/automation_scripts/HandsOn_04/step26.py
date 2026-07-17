from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Wait up to 10 sec for ANY element before failing
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")
print("Page title is:", driver.title)

driver.quit()

# Why implicit wait is NOT best practice :
# - Applies to EVERY find_element call, even ones that don't need 10 sec
# - Can't wait for a SPECIFIC condition like "until clickable"
# - Mixing it with explicit wait (Hands-On 5) causes confusing timeouts
# - Explicit waits let us wait for the EXACT condition, only where needed