# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# scope='function' means: run this fixture fresh for EVERY test function.
# Each test gets its OWN new browser, so tests can't interfere with
# each other's leftover state.
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    browser.implicitly_wait(10)

    # everything BEFORE yield = setup, runs before the test starts
    yield browser

    # everything AFTER yield = teardown, runs after the test finishes
    # (even if the test FAILED - this always runs)
    browser.quit()



#step 46

# This is a pytest "hook" - special function pytest calls automatically
# after every test phase (setup, the test itself, teardown)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only act when the actual TEST BODY finished (not setup/teardown),
    # and only if it failed
    if report.when == "call" and report.failed:
        # "item" represents the currently running test. If it used the
        # driver fixture, we can grab that same browser instance back
        driver_instance = item.funcargs.get("driver")
        if driver_instance:
            test_name = item.name.replace("[", "_").replace("]", "")
            driver_instance.save_screenshot(f"{test_name}_failure.png")
            print(f"\nScreenshot saved: {test_name}_failure.png")




#STEP 48

# scope="session" means this runs ONCE for the entire pytest run,
# not once per test - a plain constant doesn't need to be recreated
# every single test
@pytest.fixture(scope="session")
def base_url():
    return "https://www.testmuai.com/selenium-playground/"