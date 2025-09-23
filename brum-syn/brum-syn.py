import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# This package is for local development only. Comment out before uploading to AppDynamics.
from chromedriver_py import binary_path
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Helper Functions ---
# A consolidated function for finding elements with explicit waits.
def find_element_with_wait(by_locator, locator_value, timeout=10):
    """
    Finds a single element using WebDriverWait to ensure it is clickable.
    
    Args:
        by_locator (By): The Selenium `By` object (e.g., `By.ID`, `By.CSS_SELECTOR`).
        locator_value (str): The value of the locator.
        timeout (int): The maximum time to wait for the element.
    
    Returns:
        WebElement: The found element.
    
    Raises:
        TimeoutException: If the element is not found or clickable within the timeout.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by_locator, locator_value))
        )
    except TimeoutException as e:
        logger.error(f"Timed out waiting for element located by {by_locator}: '{locator_value}'")
        raise e
    except NoSuchElementException as e:
        logger.error(f"Element not found by {by_locator}: '{locator_value}'")
        raise e

# --- Main Test Script ---
try:
    logger.info("Starting Selenium test...")
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    
    # Example usage of the consolidated function
    logger.info("Entering username...")
    username_field = find_element_with_wait(By.ID, "user-name")
    username_field.send_keys("")    ##enter username or use synthetic vault key

    logger.info("Entering password...")
    password_field = find_element_with_wait(By.ID, "password")
    password_field.send_keys("")    #enter password or use synthetic vault key

    logger.info("Screenshot before clicking Login.")
    driver.get_screenshot_as_file("login-screen.png")

    logger.info("Clicking login button...")
    login_button = find_element_with_wait(By.ID, "login-button")
    login_button.click()

    logger.info("Verifying successful login by finding the 'Add to cart' button.")
    add_to_cart_button = find_element_with_wait(By.ID, "add-to-cart-sauce-labs-backpack")
    
    logger.info("Test successful! Taking a screenshot.")
    driver.get_screenshot_as_file("success.png")

except TimeoutException as ex:
    logger.error("TimeoutException: A page element did not load in time.")
    driver.get_screenshot_as_file("timeout.png")
    raise Exception("Test failed due to TimeoutException.")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
    driver.get_screenshot_as_file("error.png")
    raise

finally:
    # Ensure the browser is closed regardless of success or failure
    if 'driver' in locals() and driver:
        driver.quit()