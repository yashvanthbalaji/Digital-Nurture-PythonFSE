import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# This decorator says: "run the function below 3 separate times,
# each time filling the 'message' parameter with one of these values"
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, message):
    driver.get("https://www.testmuai.com/selenium-playground/simple-form-demo/")

    message_box = driver.find_element(By.ID, "user-message")
    message_box.send_keys(message)

    submit_button = driver.find_element(
        By.XPATH, "//button[contains(text(),'Get Checked Value')]"
    )
    submit_button.click()

    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )

    assert result.text == message