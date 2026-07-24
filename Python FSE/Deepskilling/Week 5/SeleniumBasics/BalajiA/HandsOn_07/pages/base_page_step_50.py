from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Parent class - holds abilities every page shares.
    Other page classes will inherit from this instead of repeating code."""

    def __init__(self, driver):
        # Store the driver so every method in this class (and any
        # class that inherits from it) can use self.driver
        self.driver = driver

    def navigate_to(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def wait_for_element(self, locator, timeout=10):
        # locator is expected to be a tuple like (By.ID, "user-message")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )