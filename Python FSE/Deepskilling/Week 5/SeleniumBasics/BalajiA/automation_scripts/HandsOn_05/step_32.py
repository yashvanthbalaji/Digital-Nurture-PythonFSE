# step32
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.testmuai.com/selenium-playground/simple-form-demo/")

# 1) By ID - fastest and most reliable, use this whenever it exists
by_id = driver.find_element(By.ID, "user-message")
print("Found by ID:", by_id.is_displayed())

# 2) By NAME - NOT POSSIBLE here .
# This particular input has NO "name" attribute at all (only id and
# class). not every element has
# every attribute. When name is missing, we cannot use
# By.NAME for that element and must pick a different strategy.
print("By.NAME skipped: this input has no 'name' attribute in the HTML")

# 3) By CLASS_NAME - this element has MULTIPLE classes:
#    "border border-gray-550 w-full h-35 rounded px-10"
# By.CLASS_NAME only accepts ONE class name at a time, and that class
# is likely reused by many other elements on the page - so this is
# risky. We try "rounded" here:
by_class = driver.find_element(By.CLASS_NAME, "rounded")
print("Found by CLASS_NAME 'rounded':", by_class.is_displayed())

# 4) By TAG_NAME - locates the FIRST tag on the ENTIRE page,
by_tag = driver.find_element(By.TAG_NAME, "input")
print("Found by TAG_NAME (first on page):", by_tag.is_displayed())
print("  id of the element TAG_NAME actually found:", by_tag.get_attribute("id"))

# 5) By XPATH - absolute path (counts every parent from  down)
by_xpath_absolute = driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/main/div/section[2]/div/div/div/div[1]/div[2]/div/div[1]/input"
)
print("Found by absolute XPATH:", by_xpath_absolute.is_displayed())

# 6) By XPATH - relative path using an attribute, much safer than
#    absolute because it does not care WHERE the element sits in the
#    page structure, only that it has this exact id
by_xpath_relative = driver.find_element(By.XPATH, '//*[@id="user-message"]')
print("Found by relative XPATH:", by_xpath_relative.is_displayed())

time.sleep(5)
driver.quit()