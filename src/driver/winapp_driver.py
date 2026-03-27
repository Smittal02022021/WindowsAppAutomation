import logging
from selenium.webdriver.remote.webdriver import WebDriver as RemoteDriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.options import ArgOptions
from config.settings import WINAPPDRIVER_URL, IMPLICIT_WAIT

logger = logging.getLogger(__name__)


class _WinAppDriver(RemoteDriver):
    """Thin RemoteDriver subclass that sends legacy desiredCapabilities format.

    WinAppDriver 1.2 does not accept the W3C alwaysMatch/firstMatch format;
    it requires the older JSONWP desiredCapabilities envelope.
    """

    def __init__(self, command_executor: str, desired_capabilities: dict) -> None:
        self._desired_capabilities = desired_capabilities
        super().__init__(command_executor=command_executor, options=ArgOptions())

    def start_session(self, _capabilities) -> None:  # type: ignore[override]
        response = self.execute(Command.NEW_SESSION, {"desiredCapabilities": self._desired_capabilities})
        value = response.get("value") or {}
        self.session_id = value.get("sessionId") or response.get("sessionId")
        self.caps = value

    def _unwrap_value(self, value):
        # WinAppDriver returns the legacy JSONWP element key "ELEMENT" instead
        # of the W3C key. Translate it so Selenium creates a proper WebElement.
        if isinstance(value, dict) and "ELEMENT" in value:
            return self.create_web_element(value["ELEMENT"])
        return super()._unwrap_value(value)


def create_driver(app: str, **extra_caps) -> _WinAppDriver:
    """
    Create and return a WinAppDriver Remote session.

    Args:
        app: Application path or Windows App ID (e.g. 'C:\\...\\app.exe' or UWP app ID).
        **extra_caps: Additional capabilities to merge.

    Returns:
        Driver instance connected to WinAppDriver.
    """
    desired_caps = {
        "platformName": "Windows",
        "app": app,
        **extra_caps,
    }

    logger.info("Launching app: %s", app)
    driver = _WinAppDriver(
        command_executor=WINAPPDRIVER_URL,
        desired_capabilities=desired_caps,
    )
    driver.implicitly_wait(IMPLICIT_WAIT)
    logger.info("Session created: %s", driver.session_id)
    return driver


def quit_driver(driver: _WinAppDriver) -> None:
    """Safely quit a WinAppDriver session."""
    if driver:
        logger.info("Quitting session: %s", driver.session_id)
        driver.quit()
