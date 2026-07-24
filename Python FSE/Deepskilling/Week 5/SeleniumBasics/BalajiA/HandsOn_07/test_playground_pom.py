# test_playground_pom.py
#STEP 55
from pages.simple_form_page_step_51_52 import SimpleFormPage
#step 56 import function
from pages.checkbox_page_step_53 import CheckboxPage
from pages.dropdown_page_step_54 import DropdownPage

#STEP 57
from pages.input_form_page_step_57 import InputFormPage


def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"

#STEP 56
def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")

    page.check_option(0)
    assert page.is_option_checked(0) is True

    page.uncheck_option(0)
    assert page.is_option_checked(0) is False


def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo/")

    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


 #STEP 57
def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo/")

    page.fill_form(
        name="Balaji",
        email="balaji@example.com",
        password="Test@1234",
        company="Cognizant",
        website="https://example.com",
        country="India",   
        city="Chennai",
        address1="Saveetha nagar",
        address2="Thandalam",
        state="Tamil Nadu",
        zip_code="607001",
    )
    page.submit_form()

    assert "thanks for contacting us" in page.get_success_message().lower()