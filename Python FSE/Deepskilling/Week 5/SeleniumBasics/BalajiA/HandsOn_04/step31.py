# step31_window_size.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

size = driver.get_window_size()
print("Current window size:", size)

driver.set_window_size(1280, 800)
print("Window resized to 1280x800")

driver.quit()