import logging
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils.screenshot import take_screenshot

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects. Wraps common WinAppDriver interactions."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # ------------------------------------------------------------------
    # Element finders
    # ------------------------------------------------------------------

    def find_by_name(self, name: str):
        return self.driver.find_element(AppiumBy.NAME, name)

    def find_by_id(self, automation_id: str):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, automation_id)

    def find_by_xpath(self, xpath: str):
        return self.driver.find_element(AppiumBy.XPATH, xpath)

    def find_by_class(self, class_name: str):
        return self.driver.find_element(AppiumBy.CLASS_NAME, class_name)

    # ------------------------------------------------------------------
    # Waits
    # ------------------------------------------------------------------

    def wait_for_element(self, by: str, value: str, timeout: int = 10):
        """Wait until an element is visible and return it."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logger.error("Element not found within %ss — by=%s value=%s", timeout, by, value)
            take_screenshot(self.driver, f"timeout_{value}")
            raise

    def wait_for_element_by_id(self, automation_id: str, timeout: int = 10):
        return self.wait_for_element(AppiumBy.ACCESSIBILITY_ID, automation_id, timeout)

    def wait_for_element_by_name(self, name: str, timeout: int = 10):
        return self.wait_for_element(AppiumBy.NAME, name, timeout)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def click(self, element):
        element.click()
        logger.debug("Clicked element: %s", element)

    def send_keys(self, element, text: str):
        element.clear()
        element.send_keys(text)
        logger.debug("Typed '%s' into element: %s", text, element)

    def get_text(self, element) -> str:
        text = element.text
        logger.debug("Got text '%s' from element: %s", text, element)
        return text

    def is_element_present(self, by: str, value: str) -> bool:
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def take_screenshot(self, name: str = "screenshot"):
        return take_screenshot(self.driver, name)
