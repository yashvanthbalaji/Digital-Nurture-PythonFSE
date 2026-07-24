# test_playground.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#step 48 without using direct url 
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")


    message_box = driver.find_element(By.ID, "user-message")
    message_box.send_keys("Hello Selenium")

    submit_button = driver.find_element(
        By.XPATH, "//button[contains(text(),'Get Checked Value')]"
    )
    submit_button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "message"), "Hello Selenium")
    )
    message_element = driver.find_element(By.ID, "message")
    assert message_element.text == "Hello Selenium"

#step 48 url change
def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")

    first_checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")

    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False