# step33
import time 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")

# CSS Selector 1: by ID -> use a # symbol before the id
by_id_css = driver.find_element(By.CSS_SELECTOR, "#user-message")
print("CSS by ID found:", by_id_css.is_displayed())

# CSS Selector 2: by attribute -> [attribute='value']
#by_attr_css = driver.find_element(By.CSS_SELECTOR, "[placeholder='Please enter your Message']")
#print("CSS by attribute found:", by_attr_css.is_displayed())
# this wont work because no name attribute 

by_attr_css = driver.find_element(By.CSS_SELECTOR, "[placeholder='Please enter your Message']")
print("CSS by attribute found:", by_attr_css.is_displayed())

# CSS Selector 3: by parent > child relationship
# ">" means "direct child"
by_parent_child_css = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
print("CSS by parent-child found:", by_parent_child_css.is_displayed())

time.sleep(3)
driver.quit()