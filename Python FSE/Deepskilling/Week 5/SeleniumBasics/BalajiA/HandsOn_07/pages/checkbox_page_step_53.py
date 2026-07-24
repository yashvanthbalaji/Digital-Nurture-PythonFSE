# pages/checkbox_page.py
from selenium.webdriver.common.by import By
from pages.base_page_step_50 import BasePage


class CheckboxPage(BasePage):
    """Handles everything on the Checkbox Demo page."""

    ALL_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")

    def _get_checkbox(self, index):
        # Private helper (underscore prefix = "internal use only",
        # not meant to be called directly from test files)
        checkboxes = self.driver.find_elements(*self.ALL_CHECKBOXES)
        return checkboxes[index]

    def check_option(self, index):
        checkbox = self._get_checkbox(index)
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, index):
        checkbox = self._get_checkbox(index)
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index):
        checkbox = self._get_checkbox(index)
        return checkbox.is_selected()