# All Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# --- Start of Reusable Page Object Code ---
class BasePage:
    """A base class that provides a generic find_element method."""
    def __init__(self, driver):
        self.driver = driver
        
    def find_element(self, by_type, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by_type, locator))
            )
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Element with locator '{locator}' not found within {timeout} seconds.")
            raise Exception(f"Failed to find element with locator '{locator}'.")

class LoginPage:
    """Page object for the login page."""
    
    def __init__(self, driver):
        self.driver = driver
        self.USER_NAME_INPUT = (By.ID, "user-name")
        self.PASSWORD_INPUT = (By.ID, "password")
        self.LOGIN_BUTTON = (By.ID, "login-button")
        self.ERROR_MESSAGE = (By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
    
    def navigate_to_login_page(self, url):
        self.driver.get(url)
    
    def login(self, username, password):
        self.driver.find_element(*self.USER_NAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        
    def get_error_message(self):
        return BasePage(self.driver).find_element(*self.ERROR_MESSAGE).text

class ProductsPage:
    """Page object for the products page."""

    def __init__(self, driver):
        self.driver = driver
        self.BACKPACK_ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.BACKPACK_REMOVE_BUTTON = (By.ID, "remove-sauce-labs-backpack")
        self.SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
        self.FLEECE_JACKET_LINK = (By.LINK_TEXT, "Sauce Labs Fleece Jacket")
        self.ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")

    def add_backpack_to_cart(self):
        BasePage(self.driver).find_element(*self.BACKPACK_ADD_TO_CART_BUTTON).click()
    
    def get_remove_button_text(self):
        return BasePage(self.driver).find_element(*self.BACKPACK_REMOVE_BUTTON).text

    def click_fleece_jacket(self):
        BasePage(self.driver).find_element(*self.FLEECE_JACKET_LINK).click()

    def add_fleece_jacket_to_cart(self):
        BasePage(self.driver).find_element(*self.ADD_TO_CART_BUTTON).click()

    def navigate_to_cart(self):
        BasePage(self.driver).find_element(*self.SHOPPING_CART_BADGE).click()

class CartPage:
    """Page object for the cart page."""
    
    def __init__(self, driver):
        self.driver = driver
        self.CHECKOUT_BUTTON = (By.ID, "checkout")

    def click_checkout(self):
        BasePage(self.driver).find_element(*self.CHECKOUT_BUTTON).click()

class CheckoutPage:
    """Page object for the checkout page."""
    
    def __init__(self, driver):
        self.driver = driver
        self.FIRST_NAME_INPUT = (By.ID, "first-name")
        self.LAST_NAME_INPUT = (By.ID, "last-name")
        self.POSTAL_CODE_INPUT = (By.ID, "postal-code")
        self.CONTINUE_BUTTON = (By.ID, "continue")
        self.FINISH_BUTTON = (By.ID, "finish")

    def enter_details(self, first_name, last_name, postal_code):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
    
    def click_continue(self):
        BasePage(self.driver).find_element(*self.CONTINUE_BUTTON).click()

    def click_finish(self):
        BasePage(self.driver).find_element(*self.FINISH_BUTTON).click()
        
    def get_complete_container_id(self):
        return BasePage(self.driver).find_element(By.ID, "checkout_complete_container")

# --- End of Reusable Page Object Code ---

# Comment out the following lines when running in AppDynamics.
from chromedriver_py import binary_path  # Provides the path to the ChromeDriver executable.
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

driver = webdriver.Chrome()

# Set up logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    # Maximize the browser window.
    driver.maximize_window()
    
    # Instantiate page objects.
    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    logger.info("Navigating to the login page.")
    login_page.navigate_to_login_page("https://www.saucedemo.com/")
    
    logger.info("Attempting login with locked-out user.")
    login_page.login("", "") # use locked username, password combo or use from AppD Synthetic vault
    
    logger.info("Verifying error message.")
    assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."
    driver.get_screenshot_as_file("UserLoginError.png")
    
    logger.info("Successfully verified error. Refreshing and logging in with a valid user.")
    driver.refresh()
    login_page.login("", "") # use username, password combo, correct credentials or use from AppD Synthetic vault
    
    logger.info("Adding backpack to cart.")
    products_page.add_backpack_to_cart()
    assert products_page.get_remove_button_text() == "Remove"

    logger.info("Clicking on Fleece Jacket to view details.")
    products_page.click_fleece_jacket()
    
    # This assertion relies on the original script's logic. You may need a specific Page Object method for this.
    logger.info("Verifying Fleece Jacket price is $49.99.")
    assert driver.find_element(By.CLASS_NAME, "inventory_details_price").text == "$49.99"
    
    logger.info("Adding Fleece Jacket to cart.")
    products_page.add_fleece_jacket_to_cart()
    
    logger.info("Navigating to the cart.")
    products_page.navigate_to_cart()
    
    logger.info("Clicking checkout.")
    cart_page.click_checkout()
    
    logger.info("Entering first, last name, and postal code.")
    checkout_page.enter_details("Test", "Test", "00000")
    checkout_page.click_continue()
    
    logger.info("Clicking on Finish Button.")
    checkout_page.click_finish()
    
    logger.info("Verifying order completion.")
    checkout_page.get_complete_container_id()
    driver.get_screenshot_as_file("success.png")

except TimeoutException as ex:
    logging.error(f"Timeout Exception: {str(ex)}")
    driver.get_screenshot_as_file("timeout.png")
    raise Exception("Failed with a TimeoutException")
except Exception as e:
    logging.error(f"Exception: {str(e)}")
    driver.get_screenshot_as_file("error.png")
    raise
finally:
    driver.quit()