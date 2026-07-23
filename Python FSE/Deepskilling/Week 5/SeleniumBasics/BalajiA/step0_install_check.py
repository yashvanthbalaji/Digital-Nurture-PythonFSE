# step0_install_check.py
# Just checks that selenium and webdriver-manager are installed correctly.
import selenium
from webdriver_manager.chrome import ChromeDriverManager

print("Selenium version installed:", selenium.__version__)

# This line downloads the matching ChromeDriver the first time it runs
path = ChromeDriverManager().install()
print("ChromeDriver downloaded at:", path)
print("Setup done, you can move to Step 24")