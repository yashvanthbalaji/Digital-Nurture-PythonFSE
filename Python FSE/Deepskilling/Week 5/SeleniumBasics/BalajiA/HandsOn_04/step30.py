from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

driver.execute_script('window.open("https://www.google.com");')
all_tabs = driver.window_handles
driver.switch_to.window(all_tabs[1])

driver.switch_to.window(all_tabs[0])
print("Back to original tab, title is:", driver.title)

driver.save_screenshot("playground_screenshot.png")
print("Screenshot saved as playground_screenshot.png")

driver.quit()