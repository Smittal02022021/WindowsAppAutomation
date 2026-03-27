import os
import logging
from datetime import datetime
from config.settings import SCREENSHOT_DIR

logger = logging.getLogger(__name__)


def take_screenshot(driver, name: str = "screenshot") -> str:
    """
    Save a screenshot and return its file path.

    Args:
        driver: Active Appium WebDriver instance.
        name:   Base filename (timestamp appended automatically).

    Returns:
        Absolute path to the saved screenshot, or empty string on failure.
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    try:
        driver.save_screenshot(filepath)
        logger.info("Screenshot saved: %s", filepath)
        return filepath
    except Exception as exc:
        logger.warning("Could not take screenshot: %s", exc)
        return ""
