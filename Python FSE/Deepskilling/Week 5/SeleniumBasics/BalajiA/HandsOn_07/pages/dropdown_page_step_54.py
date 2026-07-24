# pages/dropdown_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page_step_50 import BasePage


class DropdownPage(BasePage):
    """Handles everything on the Select Dropdown Demo page."""

    DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name):
        dropdown_element = self.driver.find_element(*self.DROPDOWN)
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text(day_name)

    def get_selected_day(self):
        dropdown_element = self.driver.find_element(*self.DROPDOWN)
        dropdown = Select(dropdown_element)
        return dropdown.first_selected_option.text