# pages/input_form_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page_step_50 import BasePage


class InputFormPage(BasePage):
    """Handles everything on the Input Form Submit page (testmuai.com)."""

    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "inputEmail4")
    PASSWORD_INPUT = (By.ID, "inputPassword4")
    COMPANY_INPUT = (By.ID, "company")
    WEBSITE_INPUT = (By.ID, "websitename")
    COUNTRY_SELECT = (By.NAME, "country")   # this one is a <select>, not a text box
    CITY_INPUT = (By.ID, "inputCity")
    ADDRESS1_INPUT = (By.ID, "inputAddress1")
    ADDRESS2_INPUT = (By.ID, "inputAddress2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_INPUT = (By.ID, "inputZip")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # This <p> exists in the page from the start, but has class "hidden"
    # until the form is submitted successfully - visibility_of_element_located
    # will correctly wait for it to actually become visible, not just exist
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "p.success-msg")

    def fill_form(self, name, email, password, company, website,
                  country, city, address1, address2, state, zip_code):
        self.driver.find_element(*self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.COMPANY_INPUT).send_keys(company)
        self.driver.find_element(*self.WEBSITE_INPUT).send_keys(website)

        # Country is a dropdown, so it needs Select, not send_keys
        country_dropdown = Select(self.driver.find_element(*self.COUNTRY_SELECT))
        country_dropdown.select_by_visible_text(country)

        self.driver.find_element(*self.CITY_INPUT).send_keys(city)
        self.driver.find_element(*self.ADDRESS1_INPUT).send_keys(address1)
        self.driver.find_element(*self.ADDRESS2_INPUT).send_keys(address2)
        self.driver.find_element(*self.STATE_INPUT).send_keys(state)
        self.driver.find_element(*self.ZIP_INPUT).send_keys(zip_code)

    def submit_form(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)

    # Scroll the button into the middle of the screen first - this avoids
    # it being hidden behind floating widgets (like the chat bubble) or
    # sitting just outside the visible viewport
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", submit_button
        )

        try:
            submit_button.click()
        except Exception:
            # Fallback: if Selenium's native click still fails, force the
            # click through JavaScript instead - bypasses whatever is
            # blocking normal interaction
            self.driver.execute_script("arguments[0].click();", submit_button)

    def get_success_message(self):
        element = self.wait_for_element(self.SUCCESS_MESSAGE)
        return element.text