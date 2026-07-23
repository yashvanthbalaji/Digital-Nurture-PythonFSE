# step37
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())


def test_with_sleep():
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://www.testmuai.com/selenium-playground/bootstrap-alert-messages-demo/")

    start = time.time()
    driver.find_element(By.XPATH, "//button[contains(text(),'Normal Success Message')]").click()

    # BAD: always waits the full 3 seconds, no matter what
    time.sleep(3)
    alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
    elapsed = time.time() - start

    print("sleep() version took:", round(elapsed, 2), "seconds")
    driver.quit()


def test_with_explicit_wait():
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://www.testmuai.com/selenium-playground/bootstrap-alert-messages-demo/")

    start = time.time()
    driver.find_element(By.XPATH, "//button[contains(text(),'Normal Success Message')]").click()

    # GOOD: stops waiting the MOMENT the element becomes visible
    alert = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    elapsed = time.time() - start

    print("explicit wait version took:", round(elapsed, 2), "seconds")
    driver.quit()


test_with_sleep()
test_with_explicit_wait()

# Comment: on a fast machine the alert may appear in well under 1 second,
# so sleep(3) wastes roughly 2+ seconds every single run. On a SLOW
# machine or network, if the alert takes longer than 3 seconds, the
# sleep() version fails outright - while the explicit wait version
# keeps checking up to its full 10-second budget and still passes.