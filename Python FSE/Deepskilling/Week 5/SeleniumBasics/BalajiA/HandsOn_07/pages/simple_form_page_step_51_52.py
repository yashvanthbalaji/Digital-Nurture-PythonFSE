# pages/simple_form_page.py
from selenium.webdriver.common.by import By
from pages.base_page_step_50 import BasePage


class SimpleFormPage(BasePage):
    """Handles everything on the Simple Form Demo page."""

    # Locators live here, as class-level constants - NOT inside methods.
    # If the real id ever changes, this is the ONLY line to update.
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Get Checked Value')]")
    DISPLAYED_MESSAGE = (By.ID, "message")

#STEP 52 IS BELOW

    def enter_message(self, text):
        message_box = self.driver.find_element(*self.MESSAGE_INPUT)
        message_box.send_keys(text)

    def click_submit(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit_button.click()

    def get_displayed_message(self):
        # Waits for the message to actually appear, then reads it -
        # NO assert here, just returns the text for the test to check
        element = self.wait_for_element(self.DISPLAYED_MESSAGE)
        return element.text