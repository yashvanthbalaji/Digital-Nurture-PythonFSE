from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# "driver" here matches the fixture name in conftest.py exactly -
# pytest sees this parameter and automatically injects the browser
def test_simple_form_submission(driver):
    driver.get("https://www.testmuai.com/selenium-playground/simple-form-demo/")

    message_box = driver.find_element(By.ID, "user-message")
    message_box.send_keys("Hello Selenium")

    submit_button = driver.find_element(
        By.XPATH, "//button[contains(text(),'Get Checked Value')]"
    )
    submit_button.click()

    # Wait for the displayed message to actually appear, then read it
    # result = WebDriverWait(driver, 10).until(
    #   EC.visibility_of_element_located((By.ID, "message")) -- i used this but the text has no width & height only <p> tag 
    # so i am using here to check the text directly
    #)
    # assert result.text == "Hello Selenium"

    #SO USING THE BELOW METHOD 

    # This wait just returns True/False, NOT the element itself
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "message"), "Hello Selenium")
    )
    # Now that we KNOW the text is there, fetch the actual element to read it
    message_element = driver.find_element(By.ID, "message")
    assert message_element.text == "Hello Selenium"


#step 43
def test_checkbox_demo(driver):
    driver.get("https://www.testmuai.com/selenium-playground/checkbox-demo/")

    first_checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")

    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False



# step 49

def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo/")

    dropdown_element = driver.find_element(By.ID, "select-demo")

    # Select() wraps a normal <select> element and gives you safe
    # methods to choose an option properly, instead of clicking blindly
    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text("Wednesday")

    selected_option = dropdown.first_selected_option
    assert selected_option.text == "Wednesday"